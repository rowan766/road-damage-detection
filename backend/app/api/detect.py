from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import uuid
import base64
import json

from app.services.detection_service import DetectionService
from app.services.storage_service import StorageService
from app.schemas.damage import DamageDetectionResponse, DamageCreate

router = APIRouter()
detection_service = DetectionService()
storage_service = StorageService()


@router.post("/detect", response_model=DamageDetectionResponse)
async def detect_damage(file: UploadFile = File(...)):
    """
    检测道路病害
    
    Args:
        file: 上传的图片文件
        
    Returns:
        识别结果和病害列表
    """
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="只支持图片文件")
    
    # 读取文件
    image_bytes = await file.read()
    
    # 保存图片
    image_id = str(uuid.uuid4())
    image_path = await storage_service.save_image(image_id, image_bytes)
    
    # AI 识别
    ai_result = await detection_service.detect(image_bytes)
    
    # 存储识别结果到数据库
    damage_record = DamageCreate(
        id=image_id,
        image_path=image_path,
        ai_result=ai_result
    )
    await storage_service.save_detection(damage_record)
    
    # 存储图像向量
    await storage_service.save_embedding(image_id, image_bytes, ai_result)
    
    return DamageDetectionResponse(
        id=image_id,
        image_url=f"/uploads/{image_id}.jpg",
        damages=ai_result.get("damages", []),
        risk_level=ai_result.get("riskLevel", "未知")
    )


@router.get("/similar/{damage_id}")
async def find_similar_damages(damage_id: str, limit: int = 5):
    """
    查找相似病害案例
    
    Args:
        damage_id: 病害记录ID
        limit: 返回数量
        
    Returns:
        相似病害列表
    """
    similar_cases = await storage_service.find_similar(damage_id, limit)
    return {
        "damage_id": damage_id,
        "similar_cases": similar_cases
    }

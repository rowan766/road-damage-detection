from fastapi import APIRouter, HTTPException
from app.schemas.damage import DamageFeedback
from app.services.storage_service import StorageService

router = APIRouter()
storage_service = StorageService()


@router.post("/feedback")
async def submit_feedback(feedback: DamageFeedback):
    """
    提交用户修正数据
    
    Args:
        feedback: 修正后的病害信息
        
    Returns:
        保存状态
    """
    try:
        await storage_service.save_correction(
            damage_id=feedback.damage_id,
            corrected_data=feedback.corrected
        )
        
        # 检查是否需要触发重训练
        correction_count = await storage_service.get_correction_count()
        
        message = "反馈已保存"
        if correction_count % 100 == 0:
            message = f"已收集 {correction_count} 条修正数据，可触发模型优化"
        
        return {
            "success": True,
            "message": message,
            "correction_count": correction_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_statistics():
    """获取统计数据"""
    stats = await storage_service.get_statistics()
    return stats

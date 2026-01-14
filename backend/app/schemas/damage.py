from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class DamageInfo(BaseModel):
    """单个病害信息"""
    type: str
    severity: str
    location: str
    size: str
    suggestAction: str
    confidence: float = 0.0


class DamageDetectionResponse(BaseModel):
    """病害检测响应"""
    id: str
    image_url: str
    damages: List[DamageInfo]
    risk_level: str


class DamageCreate(BaseModel):
    """创建病害记录"""
    id: str
    image_path: str
    ai_result: Dict[str, Any]


class DamageCorrectedData(BaseModel):
    """修正后的病害数据"""
    type: Optional[str] = None
    severity: Optional[str] = None
    location: Optional[str] = None
    size: Optional[str] = None


class DamageFeedback(BaseModel):
    """用户反馈"""
    damage_id: str
    corrected: DamageCorrectedData

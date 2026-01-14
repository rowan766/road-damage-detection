from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "ollama": settings.OLLAMA_BASE_URL,
        "model": settings.OLLAMA_MODEL
    }

import asyncpg
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


async def init_db():
    """初始化数据库表结构"""
    try:
        conn = await asyncpg.connect(settings.DATABASE_URL)
        
        # 创建 pgvector 扩展
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # 创建病害记录表
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS damages (
                id VARCHAR(36) PRIMARY KEY,
                image_path TEXT NOT NULL,
                damage_type VARCHAR(50),
                severity VARCHAR(20),
                location VARCHAR(200),
                ai_result JSONB,
                user_corrected JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            );
        """)
        
        # 创建索引
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_damages_type 
            ON damages(damage_type);
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_damages_created 
            ON damages(created_at DESC);
        """)
        
        # 创建修正记录表
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS damage_corrections (
                id SERIAL PRIMARY KEY,
                damage_id VARCHAR(36) REFERENCES damages(id),
                corrected_data JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 创建图像向量表 (如果需要在 PostgreSQL 中存储)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS damage_vectors (
                id SERIAL PRIMARY KEY,
                damage_id VARCHAR(36) REFERENCES damages(id),
                embedding vector(512),
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        await conn.close()
        logger.info("数据库初始化成功")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

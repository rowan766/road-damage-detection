import os
import json
from datetime import datetime
from pathlib import Path
import asyncpg
from chromadb import HttpClient
from app.core.config import settings


class StorageService:
    def __init__(self):
        self.db_pool = None
        self.chroma_client = HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT
        )
        self.collection = None
    
    async def init_db(self):
        """初始化数据库连接池"""
        if not self.db_pool:
            self.db_pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=2,
                max_size=10
            )
        
        # 初始化 ChromaDB collection
        if not self.collection:
            self.collection = self.chroma_client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION
            )
    
    async def save_image(self, image_id: str, image_bytes: bytes) -> str:
        """保存图片文件"""
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        image_path = upload_dir / f"{image_id}.jpg"
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        
        return str(image_path)
    
    async def save_detection(self, damage_record):
        """保存检测记录到 PostgreSQL"""
        await self.init_db()
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO damages (
                    id, image_path, damage_type, severity, 
                    location, ai_result, created_at
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT (id) DO NOTHING
            """,
                damage_record.id,
                damage_record.image_path,
                damage_record.ai_result.get("damages", [{}])[0].get("type", "未知"),
                damage_record.ai_result.get("damages", [{}])[0].get("severity", "未知"),
                damage_record.ai_result.get("damages", [{}])[0].get("location", ""),
                json.dumps(damage_record.ai_result, ensure_ascii=False),
                datetime.now()
            )
    
    async def save_embedding(self, damage_id: str, image_bytes: bytes, ai_result: dict):
        """保存图像向量到 ChromaDB"""
        await self.init_db()
        
        # 这里简化处理，实际应该用 CLIP 模型生成 embedding
        # 当前使用文本描述作为向量
        text_desc = json.dumps(ai_result, ensure_ascii=False)
        
        self.collection.add(
            documents=[text_desc],
            metadatas=[{
                "damage_id": damage_id,
                "type": ai_result.get("damages", [{}])[0].get("type", "未知"),
                "severity": ai_result.get("damages", [{}])[0].get("severity", "未知"),
                "created_at": datetime.now().isoformat()
            }],
            ids=[damage_id]
        )
    
    async def find_similar(self, damage_id: str, limit: int = 5) -> list:
        """查找相似病害"""
        await self.init_db()
        
        # 从 ChromaDB 获取原始记录
        result = self.collection.get(ids=[damage_id])
        if not result["documents"]:
            return []
        
        # 相似度搜索
        query_text = result["documents"][0]
        similar = self.collection.query(
            query_texts=[query_text],
            n_results=limit + 1  # +1 因为会包含自己
        )
        
        # 过滤掉自己
        similar_ids = [
            id for id in similar["ids"][0] 
            if id != damage_id
        ][:limit]
        
        # 从 PostgreSQL 获取详细信息
        async with self.db_pool.acquire() as conn:
            records = await conn.fetch(
                "SELECT * FROM damages WHERE id = ANY($1)",
                similar_ids
            )
        
        return [dict(r) for r in records]
    
    async def save_correction(self, damage_id: str, corrected_data: dict):
        """保存用户修正数据"""
        await self.init_db()
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE damages 
                SET user_corrected = $1, updated_at = $2
                WHERE id = $3
            """,
                json.dumps(corrected_data, ensure_ascii=False),
                datetime.now(),
                damage_id
            )
            
            # 记录到修正历史表
            await conn.execute("""
                INSERT INTO damage_corrections (
                    damage_id, corrected_data, created_at
                )
                VALUES ($1, $2, $3)
            """,
                damage_id,
                json.dumps(corrected_data, ensure_ascii=False),
                datetime.now()
            )
    
    async def get_correction_count(self) -> int:
        """获取修正数据数量"""
        await self.init_db()
        
        async with self.db_pool.acquire() as conn:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM damage_corrections"
            )
        return count
    
    async def get_statistics(self) -> dict:
        """获取统计数据"""
        await self.init_db()
        
        async with self.db_pool.acquire() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM damages")
            corrected = await conn.fetchval(
                "SELECT COUNT(*) FROM damages WHERE user_corrected IS NOT NULL"
            )
            by_type = await conn.fetch("""
                SELECT damage_type, COUNT(*) as count 
                FROM damages 
                GROUP BY damage_type
            """)
        
        return {
            "total_detections": total,
            "total_corrections": corrected,
            "by_type": {r["damage_type"]: r["count"] for r in by_type}
        }


# 全局实例
storage_service = StorageService()

import base64
import json
from langchain_ollama import ChatOllama
from app.core.config import settings


ROAD_DAMAGE_PROMPT = """你是专业的道路养护专家。分析图片中的路面病害，返回JSON格式：

{
  "damages": [
    {
      "type": "坑槽|裂缝|网裂|沉陷|滑坡|坍塌",
      "severity": "轻微|中等|严重|危险",
      "location": "描述具体位置",
      "size": "估算尺寸(长x宽x深cm)",
      "suggestAction": "修复建议",
      "confidence": 0.95
    }
  ],
  "riskLevel": "低|中|高|紧急",
  "summary": "整体评估"
}

判断标准：
1. 坑槽：深度>5cm为严重，>10cm为危险
2. 裂缝：宽度>3mm需处理，>10mm为严重
3. 滑坡/坍塌：直接标记危险
4. 网裂：覆盖面积>2m²为严重

只返回JSON，不要其他文字。"""


class DetectionService:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1
        )
    
    async def detect(self, image_bytes: bytes) -> dict:
        """
        使用 AI 模型检测道路病害
        
        Args:
            image_bytes: 图片字节数据
            
        Returns:
            识别结果字典
        """
        try:
            # 转换为 base64
            img_b64 = base64.b64encode(image_bytes).decode()
            
            # 调用 AI 模型
            result = await self.llm.ainvoke([
                {"type": "text", "text": ROAD_DAMAGE_PROMPT},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{img_b64}"
                }
            ])
            
            # 解析结果
            content = result.content.strip()
            
            # 清理可能的 markdown 标记
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            ai_result = json.loads(content.strip())
            
            return ai_result
            
        except json.JSONDecodeError as e:
            # 如果 JSON 解析失败，返回错误结构
            return {
                "damages": [],
                "riskLevel": "未知",
                "summary": f"识别失败: {str(e)}",
                "error": str(e)
            }
        except Exception as e:
            raise Exception(f"检测失败: {str(e)}")

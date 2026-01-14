# 道路病害智能识别系统

基于 FastAPI + AI 视觉模型的道路病害自动识别与管理系统

## 功能特性

- 🔍 AI 智能识别道路病害（坑槽、裂缝、滑坡、坍塌等）
- 📝 自动生成结构化表单数据
- ✏️ 用户修正与数据闭环
- 📊 识别历史与统计分析
- 🔄 持续学习优化模型
- 🎯 相似病害检索

## 技术栈

- **后端框架**: FastAPI
- **AI 模型**: Qwen2-VL / Ollama
- **数据库**: PostgreSQL + pgvector
- **向量存储**: ChromaDB
- **容器化**: Docker + Docker Compose

## 快速开始

### 1. 环境要求

```bash
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+ (可选，用于前端)
```

### 2. 克隆项目

```bash
git clone https://github.com/rowan766/road-damage-detection.git
cd road-damage-detection
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入必要配置
```

### 4. 启动服务

```bash
# 启动所有服务
docker-compose up -d

# 下载 AI 模型
docker exec -it road-damage-ollama ollama pull qwen2-vl:7b

# 查看日志
docker-compose logs -f
```

### 5. 访问服务

- API 文档: http://localhost:8000/docs
- 前端界面: frontend/index.html

## 项目结构

```
road-damage-detection/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务逻辑
│   │   └── utils/       # 工具函数
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # 前端示例
├── docker-compose.yml
├── .env.example
└── README.md
```

## API 文档

### 识别病害

```bash
POST /api/detect
Content-Type: multipart/form-data

# 参数
- file: 图片文件

# 返回
{
  "id": "uuid",
  "damages": [
    {
      "type": "坑槽",
      "severity": "严重",
      "location": "估算位置",
      "size": "30x20x5cm",
      "confidence": 0.92
    }
  ]
}
```

### 提交修正

```bash
POST /api/feedback
Content-Type: application/json

{
  "damage_id": "uuid",
  "corrected": {
    "type": "裂缝",
    "severity": "中等"
  }
}
```

## 开发指南

### 本地开发

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 部署

详见 [快速开始文档](./docs/quickstart.md)

## License

MIT License

---

**项目特色**

✅ 基于 AI 大模型的智能识别  
✅ 完整的数据闭环优化  
✅ Docker 一键部署  
✅ 向量数据库支持相似检索  
✅ RESTful API 设计  

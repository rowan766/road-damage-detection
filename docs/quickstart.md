# 快速开始指南

## 环境准备

### 1. 安装 Docker

**Windows**:
- 下载 Docker Desktop: https://www.docker.com/products/docker-desktop
- 安装并启动 Docker Desktop
- 确保 WSL2 已启用

**macOS**:
```bash
brew install --cask docker
```

**Linux**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. 验证安装

```bash
docker --version
docker-compose --version
```

---

## 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/rowan766/road-damage-detection.git
cd road-damage-detection
```

### 2. 启动所有服务

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

### 3. 下载 AI 模型

```bash
# 进入 Ollama 容器
docker exec -it road-damage-ollama bash

# 下载 Qwen2-VL 模型(约 4GB)
ollama pull qwen2-vl:7b

# 验证模型
ollama list

# 退出容器
exit
```

### 4. 初始化数据库

数据库会在首次启动时自动初始化。可以通过以下命令验证:

```bash
docker exec -it road-damage-postgres psql -U road_user -d road_damage -c "\dt"
```

应该看到:
- damages (病害记录表)
- damage_corrections (修正记录表)
- damage_vectors (向量表)

---

## 访问服务

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/health
- **ChromaDB**: http://localhost:8001
- **PostgreSQL**: localhost:5432

---

## 测试 API

### 使用 curl

```bash
# 上传图片检测
curl -X POST "http://localhost:8000/api/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@road_damage.jpg"
```

### 使用 Postman

1. 打开 Postman
2. 新建 POST 请求: `http://localhost:8000/api/detect`
3. Body 选择 `form-data`
4. 添加字段: `file` (类型选 File)
5. 选择图片文件
6. 发送请求

### 使用 Python

```python
import requests

url = "http://localhost:8000/api/detect"
files = {"file": open("road_damage.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

---

## 常用命令

### 服务管理

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启服务
docker-compose restart backend

# 查看日志
docker-compose logs -f backend

# 查看服务状态
docker-compose ps
```

### 数据库操作

```bash
# 连接数据库
docker exec -it road-damage-postgres psql -U road_user -d road_damage

# 查看表
\dt

# 查看病害记录
SELECT id, damage_type, severity, created_at FROM damages LIMIT 10;

# 退出
\q
```

### 清理数据

```bash
# 停止并删除容器
docker-compose down

# 删除所有数据(包括数据库和上传文件)
docker-compose down -v

# 重新开始
docker-compose up -d
```

---

## 故障排查

### 问题1: Ollama 模型未下载

**症状**: API 返回错误 "model not found"

**解决**:
```bash
docker exec -it road-damage-ollama ollama pull qwen2-vl:7b
```

### 问题2: 数据库连接失败

**症状**: "connection refused"

**检查**:
```bash
# 查看 PostgreSQL 状态
docker logs road-damage-postgres

# 等待数据库完全启动(需要 10-30 秒)
docker-compose up -d
sleep 30
docker-compose restart backend
```

### 问题3: 端口被占用

**症状**: "port is already allocated"

**解决**:
```bash
# 修改 docker-compose.yml 中的端口映射
# 例如将 8000:8000 改为 8080:8000
```

---

## 下一步

- [完整文档](../README.md)
- [API 文档](http://localhost:8000/docs)

# 部署指南

## GitHub 仓库管理

### 克隆和运行

其他人克隆你的项目:

```bash
# 克隆
git clone https://github.com/rowan766/road-damage-detection.git
cd road-damage-detection

# 启动
docker-compose up -d

# 下载模型
docker exec -it road-damage-ollama ollama pull qwen2-vl:7b

# 访问
open http://localhost:8000/docs
```

---

## 项目结构

```
road-damage-detection/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库初始化
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── services/       # 业务逻辑
│   │   └── main.py         # 应用入口
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # 前端示例
│   └── index.html
├── docs/                   # 文档
│   ├── quickstart.md       # 快速开始
│   └── deployment.md       # 部署指南
├── docker-compose.yml      # Docker 编排
├── .env.example            # 环境变量示例
├── .gitignore
├── README.md
├── LICENSE
└── test_api.py            # API 测试脚本
```

---

## 更新代码

```bash
# 查看状态
git status

# 添加更改
git add .

# 提交
git commit -m "feat: 新功能描述"

# 推送
git push
```

---

## 版本发布

```bash
# 打标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0

# 或推送所有标签
git push --tags
```

---

## 生产环境部署建议

### 1. 安全配置

- 修改默认数据库密码
- 配置 HTTPS/SSL
- 设置防火墙规则
- 使用环境变量管理敏感信息

### 2. 性能优化

- 使用 Nginx 反向代理
- 配置 Redis 缓存
- 启用 gzip 压缩
- 设置日志轮转

### 3. 监控与备份

- 配置应用监控(Prometheus/Grafana)
- 设置数据库定期备份
- 配置错误日志告警
- 监控磁盘和内存使用

---

## 常见问题

### 1. 推送被拒绝

```bash
# 先拉取远程更改
git pull origin main --rebase

# 再推送
git push
```

### 2. 端口冲突

```bash
# 修改 docker-compose.yml 中的端口映射
# 例如将 8000:8000 改为 8080:8000
```

### 3. 模型下载慢

```bash
# 使用代理
docker exec -it road-damage-ollama bash
export http_proxy=http://your-proxy:port
ollama pull qwen2-vl:7b
```

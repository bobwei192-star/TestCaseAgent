# 安全策略

## 沙盒执行安全

本项目的核心功能是自动生成并执行测试代码。LLM 生成的代码在沙盒中执行，
当前支持以下安全措施：

### 已有安全措施
1. **语法校验**: 执行前进行 `ast.parse()` 语法检查
2. **内容校验**: 检查代码是否包含 pytest 测试函数、subprocess.run 等关键调用
3. **临时目录执行**: PytestStrategy 使用 tempfile 创建临时目录执行
4. **策略隔离**: Docker 策略将代码运行在容器内

### 建议的安全加固
1. **不要在生产环境使用 PytestStrategy**: 它直接在本机执行，恶意代码可逃逸
2. **使用 Docker 沙盒**: 优先使用 `LocalDockerPytestStrategy` 或远程 SSH Docker
3. **seccomp/AppArmor 限制**: 生产 Docker 容器应启用安全配置
4. **网络隔离**: 沙盒执行时启用 `block_network=True`
5. **资源限制**: 设置 CPU/内存限制，防止资源耗尽

## API 鉴权

当通过 LangGraph Platform (langgraph dev) 部署时：
1. 设置 `TEST_CASE_AGENT_API_KEY` 环境变量启用 API Key 鉴权
2. 客户端需在 HTTP header 中携带 `Authorization: Bearer <API_KEY>`
3. 开发环境可通过 `LANGFUSE_AUTH_DISABLED=true` 跳过鉴权

## Docker Compose 密码管理

所有密码通过 `.env` 文件配置：
- `POSTGRES_PASSWORD`: PostgreSQL 密码
- `REDIS_PASSWORD`: Redis 密码
- `MINIO_USER` / `MINIO_PASSWORD`: MinIO 凭证
- `NEXTAUTH_SECRET`: Langfuse NextAuth 密钥
- `ENCRYPTION_KEY`: Langfuse 加密密钥

生产环境请使用强密码，不要使用 docker-compose.yml 中的默认值。

## 报告安全问题

请通过 GitHub Issues 报告安全问题，标记为 "security"。

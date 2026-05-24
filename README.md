# TestCaseAgent

基于 **LangGraph + LangChain + DeepAgents** 构建的智能体，自动生成、执行、修复测试用例。

## 项目定位

输入自然语言（或自然语言 + 一段代码 / 报错信息），Agent 自动生成或者更新修复一个可执行的 pytest 测试用例文件。

### 商业价值

| 维度 | 描述 |
|------|------|
| **降本** | 手写一个 用例需数小时，Agent 一句话自动闭环，效率提升 10 倍以上 |
| **提质** | RAG 知识库保障用例贴合官方规范、风格统一、语法可校验，团队知识沉淀为可执行资产 |
| **提效** | Agent 自动接管"生成 → 执行 → 失败修复"全流程，端到端验证从天级压缩至分钟级 |
| **增值** | Agent 可并行批量生成用例，测试覆盖率随版本快速规模化 |

## 核心功能

1. **生成测试用例** — 用户以自然语言描述测试需求，Agent 生成 pytest 格式可执行代码
2. **生成并执行** — 自动调用 AIDevOps Agent（or Tools） 执行生成的用例并返回结果
3. **结果驱动修复** — AIDevOps（or Tools） 返回失败后自动分析原因并修复用例（最多 3 轮重试）
4. **用户驱动修复** — 用户描述用例问题，Agent 分析并修复



## 技术栈

| 技术 | 用途 | 作用   |
|------|------|---------|
| **LangGraph** | Agent 编排引擎 | StateGraph 有状态图 + Checkpointer 多轮记忆 + InMemoryStore 长期记忆 + `graph.stream()` 节点级流式事件 |
| **DeepAgents** | Agent 框架 | `create_deep_agent()` 一行代码出 agent，内置 Filesystem 中间件 + Subagent 调度 + HITL 中断机制 |
| **MCP** (Model Context Protocol) | 外部工具接入 | HuggingFace 官方 MCP Server 的标准协议集成，npx 动态加载 `hub_repo_search` / `hub_repo_details` |
| **RAG** (Chroma + HuggingFace) | 上下文检索 | `InMemoryVectorStore`（对齐 LangChain 官方模式） + `sentence-transformers/all-MiniLM-L6-v2` + 268 篇文档索引 |
| **Langfuse** | 可观测性 | 自部署 Docker 容器，全链路 Trace + Token 用量追踪 + 可视化调试 |
| **Typer + Rich** | CLI 工具 | Rich `Live` 实时节点执行树 + `Tree/Panel` 代码渲染 + HITL 终端确认 |
| **HITL** | 人工审批 | CLI `Confirm.ask()` 计划审批 + Graph `interrupt_on` 工具中断（写文件前确认） |
| **LangChain** | LLM 调用层 | `ChatOpenAI` 多 provider（DeepSeek/AMD/OpenAI）+ `StructuredTool` 工具封装 |
| **HuggingFace Hub** | 模型验证 | MCP 工具确认 HF 模型是否存在及可下载，禁止凭记忆假设 |
| **input_filter** | 输入清洗 | 控制字符过滤 + 重复字符折叠 + 全重复行去重 + Unicode NFC 规范化 + 垃圾检测 |
| **Pytest** | 测试框架 | 单元 / 集成测试分离（`tests/unit/` + `tests/integration/`），冒烟测试自动 skip 缺密钥场景 |
| **Makefile** | 自动化 | `make test` / `make serve` / `make smoke` / `make lint` 一行命令 |
| **Chroma** | 向量库 | `PersistentClient` 本地落盘 + `collection.get()` 批量加载到内存 |
| **python-dotenv** | 配置管理 | `.env` 多 provider 配置，`load_dotenv()` 统一入口 |


## 核心流程

```
用户需求
   │
   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  requirement  │ → │   context    │ → │   planner    │
│   _parser    │    │  _retriever  │    │  (LLM 节点)  │
└──────────────┘    └──────────────┘    └──────────────┘
                                                │
                  ┌─────────────────────────────┘
                  ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  generator   │ → │  execution   │ → │  dry_run     │
│  (LLM 节点)  │    │   _planner   │    │  _executor   │
└──────────────┘    └──────────────┘    └──────────────┘
       ↑                    │
       │              ┌─────┘
       │              ▼
       │        ┌──────────────┐    ┌──────────────┐
       │        │   result     │ → │   repairer   │
       │        │   _parser    │    │  (LLM 节点)  │
       │        └──────────────┘    └──────────────┘
       │                                    │
       │                              ┌─────┘
       │                              ▼
       │                        ┌──────────────┐
       └────────────────────────│  finalizer   │
                                └──────────────┘
                                       │
                                       ▼
                                    完成 ✅
```




## 快速开始

### 环境要求

- Python >= 3.12
- Git
- LLM API Key（DeepSeek / OpenAI 兼容接口）

### 一键安装

```bash
git clone https://github.com/bobwei192-star/TestCaseAgent.git
cd TestCaseAgent
bash install.sh
```

脚本会自动完成：
1. 创建 Python 虚拟环境
2. 安装项目依赖（LangGraph、LangChain、DeepAgents、Langfuse 等）
3. 安装项目包
4. 克隆 DeployAgent 并部署

### 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入 LLM API Key 和 Langfuse 配置
```

### 启动开发服务器

```bash
source .venv/bin/activate
langgraph dev
```

访问：
- LangGraph API：http://localhost:2024
- Langfuse Tracing UI（需另行部署 Langfuse）：http://localhost:3000

### 本地调试

```bash
source .venv/bin/activate
python test_debug.py
```

## 知识库

Agent 挂载 RAG 知识库，确保生成的用例贴合官方规范：

| 知识来源 | 内容 |
|---------|------|
| ROCm 官方文档 | API 签名、参数约束、数据类型、性能基线 |
| vLLM 文档 | 启动参数、模型支持列表、benchmark 方式 |
| 社区 Issue 归档 | `etc/rocm_issues/` 中 100+ 已知问题及修复方案 |
| 现存用例仓库 | 社区已有 pytest 用例，作为风格和结构参考 |

## A2A 通信

Test Case Agent 与 AIDevOps Agent 之间通过 **A2A 协议**通信：

- Test Case Agent 通过 A2A 向 AIDevOps 发起任务委托（提交用例 → 请求环境执行）
- AIDevOps 执行完成后通过 A2A 回传结果（pass / fail + 日志 + 性能数据）
- AIDevOps 不可达时可降级为仅本地产出用例，不阻塞流程

## 工具集

| 工具 | 用途 |
|------|------|
| `save_to_file` | 将生成的代码保存到文件 |
| `read_file` | 读取文件内容 |
| RAG 检索 | 从知识库获取 ROCm 规范 |
| A2A 任务委托 | 向 AIDevOps 提交执行请求 |
| A2A 结果接收 | 获取 AIDevOps 回传的执行结果 |

## 可观测性

通过 **Langfuse** 实现全链路 Tracing：

- 每次生成 / 执行 / 修复的链路自动上报
- Token 用量监控与成本分析
- 失败分析与回溯

## Docker 部署

```bash
# 1. 构建并启动全部服务（agent + langfuse + postgres + clickhouse + redis + minio）
docker-compose up -d

# 2. 只启动 agent（依赖外部 langfuse）
docker-compose up -d agent

# 3. 查看日志
docker-compose logs -f agent

# 4. 停止
docker-compose down
```

| 服务 | 端口 | 说明 |
|------|------|------|
| agent | `2024` | LangGraph API（`langgraph dev`） |
| langfuse | `3000` | 可观测性 Tracing UI |
| postgres | `5432` | 持久化存储（仅 localhost 可访问） |
| clickhouse | `8123` / `9000` | 分析数据库（仅 localhost 可访问） |
| redis | `6379` | 缓存与队列（仅 localhost 可访问） |
| minio | `9090` | S3 兼容对象存储（仅 localhost 可访问） |

**首次启动后配置 Langfuse：**

1. 打开 `http://localhost:3000` → 注册账号
2. Settings → API Keys → Create API Key
3. 将 `Public Key` / `Secret Key` 填入 `.env`：
   ```
   LANGFUSE_PUBLIC_KEY="pk-lf-..."
   LANGFUSE_SECRET_KEY="sk-lf-..."
   LANGFUSE_BASE_URL="http://langfuse:3000"
   ```
4. 重启 agent：`docker-compose restart agent`

## 里程碑

| 阶段 | 目标 | 核心产出 |
|------|------|---------|
| **P0** | 基础生成 | 知识库搭建 → CLI 对话 → 自然语言生成 pytest 用例 → 文件落盘 |
| **P1** | 对接执行 | A2A 集成 → 生成用例后自动提交 AIDevOps 执行 → 接收并展示结果 |
| **P2** | 自动修复 | 失败分析 → 用例修复 → 自动重提交（最多 3 轮重试循环） |
| **P3** | 闭环迭代 | 用例仓库管理 → Web 界面 → CI 自动触发 → 失败自动修复 → 人工兜底 |

## 非功能需求

| 维度 | 要求 |
|------|------|
| 可靠性 | 生成用例通过 AST 语法校验，不可包含不可执行代码 |
| 容错 | AIDevOps 不可达时降级为仅生成本地用例，不阻塞流程 |
| 可追溯 | 每次生成 / 执行 / 修复记录通过 Langfuse 全链路追踪 |
| Token 控制 | Prompt 优化 + 分层模型 + 用量监控与限制 |
| 稳定性 | 多 API 备份 + 请求重试 + 降级处理 |

## 开发路线图

1. 环境搭建 + 冒烟测试（`smoke_test.py`）→ 确认 LangGraph UI 和 Langfuse Tracing 可用
2. 开发 Planning 层 → 线性工作流
3. 开发 State、Node、Edge 组装（至少 1 个 LLM 节点）
4. 测试最小智能体
5. 开发 Function Calling 工具层
6. 开发上下文与 Memory
7. 集成 rtk-ai/rtk 工具
8. 开发评估工具
9. 交付第一版

## License

见 [LICENSE](LICENSE) 文件。
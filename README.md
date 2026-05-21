# TestCaseAgent

基于 **LangGraph + LangChain + DeepAgents** 构建的智能体，自动生成、执行、修复 AMD ROCm 及 AI Model 的 pytest 测试用例。

## 项目定位

输入自然语言（或自然语言 + 一段代码 / 报错信息），Agent 自动处理并输出一个可执行的 pytest 测试用例文件。

### 商业价值

| 维度 | 描述 |
|------|------|
| **降本** | 手写一个 ROCm 用例需数小时，Agent 一句话自动闭环，效率提升 10 倍以上 |
| **提质** | RAG 知识库保障用例贴合官方规范、风格统一、语法可校验，团队知识沉淀为可执行资产 |
| **提效** | Agent 自动接管"生成 → 执行 → 失败修复"全流程，端到端验证从天级压缩至分钟级 |
| **增值** | Agent 可并行批量生成用例，测试覆盖率随版本快速规模化 |

## 核心功能

1. **生成测试用例** — 用户以自然语言描述测试需求，Agent 生成 pytest 格式可执行代码
2. **生成并执行** — 自动调用 AIDevOps Agent 执行生成的用例并返回结果
3. **结果驱动修复** — AIDevOps 返回失败后自动分析原因并修复用例（最多 3 轮重试）
4. **用户驱动修复** — 用户描述用例问题，Agent 分析并修复

### 覆盖范围

- ROCm 底层算子：rocBLAS、MIOpen、rocSOLVER、rocFFT、rocRAND、RCCL 等
- AI Model 推理：PyTorch / vLLM / ONNX Runtime / JAX / TensorFlow / llama.cpp
- 系统环境：ROCm 安装验证、GPU 拓扑、内核驱动、WSL 工具链

## 技术栈

| 层级 | 选型 |
|------|------|
| Agent 编排 | LangGraph |
| LLM 调用 | LangChain + OpenAI 兼容接口 |
| Agent 框架 | DeepAgents（`create_deep_agent`） |
| 可观测性 | Langfuse（Tracing / 监控） |
| Agent 间通信 | A2A (Agent-to-Agent Protocol) |
| 用例格式 | pytest（`.py`） |
| 外部依赖 | AIDevOps Agent（通过 A2A 协议对接） |
| 项目管理 | pyproject.toml + setuptools |

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

**9 个 LangGraph 节点**：

| 节点 | 职责 |
|------|------|
| `requirement_parser` | 解析用户需求，提取测试目标 |
| `context_retriever` | 从知识库 / Store 检索上下文和参考用例 |
| `planner` | LLM 节点，拆解测试点，生成结构化用例计划 |
| `generator` | LLM 节点，根据计划生成 pytest 代码 |
| `execution_planner` | 规划执行方式（本地 / AIDevOps / Docker / skip） |
| `dry_run_executor` | Dry-run 执行收集反馈 |
| `result_parser` | 解析执行结果，判断通过 / 失败 |
| `repairer` | LLM 节点，分析失败原因并自动修复（最多 3 轮） |
| `finalizer` | 输出最终用例并落盘 |

## 项目结构

```
TestCaseAgent/
├── src/agent/
│   ├── app.py          # LangGraph Studio 入口（langgraph dev 加载）
│   ├── graph.py        # StateGraph 构建与节点编排
│   ├── state.py        # AgentState 与 AgentContext 定义
│   ├── nodes.py        # 各节点实现
│   ├── tools.py        # 工具函数（文件读写等）
│   ├── model.py        # LLM 模型初始化
│   ├── tracing.py      # Langfuse 可观测性配置
│   └── runner.py       # 本地运行入口
├── etc/
│   └── rocm_issues/    # ROCm 社区已知问题知识库（100+ Issue）
├── doc/
│   ├── 01_需求与用例.md
│   ├── 02_架构与工具设计.md
│   └── 03_开发运行与观测.md
├── scripts/            # 辅助脚本
├── pyproject.toml      # 项目配置与依赖
├── requirements.txt    # pip 依赖
├── langgraph.json      # LangGraph CLI 配置
├── install.sh          # 一键安装脚本
├── test_debug.py       # 调试入口
├── .env.example        # 环境变量模板
└── README.md
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

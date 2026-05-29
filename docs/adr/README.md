# 架构决策记录 (ADR)

> `docs/adr/` — Architecture Decision Records
> 
> 记录 TestCaseAgent 项目的重要架构决策及其上下文。

---

## ADR-001: 选择 LangGraph StateGraph 作为编排引擎

**状态**: 已采纳 | **日期**: 2026-03

**决策**:
使用 LangGraph 的 `StateGraph` 作为 Agent 编排引擎，以 TypedDict 定义共享状态，通过条件边实现节点间的动态路由。

**上下文**:
项目需要将多个 LLM 调用节点串联为一个完整的工作流（需求解析 → 计划生成 → 代码生成 → 沙盒执行），并在失败时自动回到 planner 重新规划。

**方案对比**:

| 方案 | 优点 | 缺点 |
|------|------|------|
| **LangGraph StateGraph** | 有状态图、Checkpointer 多轮记忆、条件路由、社区活跃 | 学习曲线、LangChain 生态依赖 |
| 自定义 Python 脚本 | 完全控制、无框架依赖 | 状态管理需手写、复杂条件路由难维护 |
| CrewAI/AG2 | 更高层抽象 | 灵活度不足、调试困难 |

**后果**:
- ✅ 状态管理由框架负责，开发者只需定义节点和边
- ✅ Checkpointer 实现多轮对话记忆
- ✅ 条件路由实现"执行失败 → 重新规划"的闭环修复
- ⚠️ 深度依赖 LangChain/LangGraph 生态，版本升级需适配

---

## ADR-002: 使用策略模式处理沙盒执行多意图

**状态**: 已采纳 | **日期**: 2026-04

**决策**:
在 `sandbox_executor` 节点中使用**策略模式**，根据解析出的意图类型（GENERATE/ENV_BUILD/DIAGNOSE/...）选择不同的执行策略。

**上下文**:
Agent 支持 9 种意图类型：
- 测试代码类（GENERATE/APPEND/UPDATE/REFACTOR）→ 执行 pytest
- 环境构建类（ENV_BUILD）→ 执行 docker build
- 查询类（DIAGNOSE/COVERAGE/PROBE）→ 跳过执行

**方案对比**:

| 方案 | 优点 | 缺点 |
|------|------|------|
| **策略模式** | 可扩展、新意图只需加策略、单元测试友好 | 类略多 |
| if-else 分支 | 简单直接 | 9 种意图时复杂度 O(n²) |
| 命令模式 | 更灵活 | 过度设计 |

**后果**:
- ✅ `StrategyFactory` 根据意图动态选择策略
- ✅ 添加新意图类型只需新增一个 Strategy 子类
- ✅ 查询类意图跳过沙盒执行，节省资源

---

## ADR-003: 合并 planner 和 execution_planner

**状态**: 已采纳 | **日期**: 2026-05-29

**决策**:
将 `node_execution_planner.py` 的功能合并到 `node_planner.py` 中，由 planner 在一次 LLM 调用中同时输出 `case_plan` 和 YAML 格式的 `execution_plan`。

**上下文**:
- `node_execution_planner.py` 从未被接入 graph，是死代码
- 两个节点的功能高度相关，分开调用增加一次 LLM API 调用
- 合并后减少延迟和成本

**后果**:
- ✅ planner 输出包含 `execution_plan`（YAML 解析为结构化 dict）
- ✅ 三层降级解析：合法 YAML → raw 文本 → 默认值
- ✅ 消除 123 行死代码
- ✅ 减少一次 LLM 调用，降低成本和延迟

---

## ADR-004: LLM 生成代码的安全审查

**状态**: 已采纳 | **日期**: 2026-05-29

**决策**:
在 `generator` 节点中，代码生成后立即执行安全审查（`code_security.review_code()`），拦截包含危险调用（eval/exec/os.system 等）的代码。

**上下文**:
- LLM 可能生成包含 `eval()`、`exec()`、`os.system()` 等危险调用的代码
- 代码将在沙盒中执行，但多层防护优于单层

**审查规则**:
- **关键拦截**: eval/exec/compile/os.system/os.popen → 直接拒绝
- **沙盒模式警告**: 非白名单模块的 import → 记录警告
- **网络阻断**: 沙盒模式下禁止 socket/http 请求

**后果**:
- ✅ `security_review` quality_gate 在 validation 之前执行
- ✅ 拦截的代码不会写入文件
- ⚠️ 白名单需要持续维护以适应新的测试场景

---

## ADR-005: 消息类型统一为 LangChain BaseMessage

**状态**: 已采纳 | **日期**: 2026-05

**决策**:
所有节点统一使用 `HumanMessage` 调用 LLM 和 `AIMessage` 返回结果，使用 `add_messages` reducer 进行消息追加。

**上下文**:
- 早期代码中混用 dict 和 BaseMessage
- 混用导致 Checkpointer 反序列化时出现类型错误
- add_messages reducer 是 LangGraph 标准模式

**后果**:
- ✅ 消息类型完全统一
- ✅ Checkpointer 存储和恢复正确
- ✅ 与 LangGraph Runtime 完全兼容

---

## ADR-006: Checkpointer/Store 自动选择策略

**状态**: 已采纳 | **日期**: 2026-05

**决策**:
通过 `_build_checkpointer()` 和 `_build_store()` 自动选择存储后端：有 PostgreSQL 连接则用持久化存储，否则使用内存存储。

**方案**:
- 开发/测试环境: MemorySaver + InMemoryStore（零配置）
- 生产环境: 设置 `TEST_CASE_AGENT_POSTGRES_URL` 自动切换 PostgreSQL

**后果**:
- ✅ 开发环境零配置启动
- ✅ 生产环境一键切换持久化
- ✅ 连接失败自动降级，不阻塞启动

"""Agent 状态定义模块 - 定义 LangGraph 各节点共享的运行时状态和长期记忆上下文。

本文件定义了两个核心数据结构：
- AgentState: 图运行时各节点共享的状态字典（TypedDict）
- AgentContext: 长期记忆上下文，通过 LangGraph Runtime 自动注入节点

调用的框架/库：
- typing: Python 类型注解（Annotated、TypedDict）
- operator: 提供 operator.add 用于状态字段的累加合并策略
- dataclasses: 用于定义 AgentContext 数据类
- langgraph.graph.message: 标准消息合并 reducer
"""

import operator
from dataclasses import dataclass
from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """LangGraph 图运行时各节点共享的状态字典。

    字段说明：
    - messages: 对话消息列表，使用 add_messages reducer（标准 BaseMessage 追加合并）
    - requirement: 用户原始需求文本
    - parsed_requirement: 经 LLM 解析后的结构化需求
    - context: RAG 检索到的上下文信息
    - case_plan: 测试计划文本
    - code / generated_code: 生成的测试代码
    - explanation: LLM 回复中的非代码文字说明
    - execution_result: 沙盒执行结果
    - sandbox_*: 沙盒执行循环相关字段
    """

    messages: Annotated[list[BaseMessage], add_messages]  # 对话消息，标准合并
    requirement: str  # 用户原始需求
    parsed_requirement: str  # 解析后的结构化需求
    parsed_intent: str  # 解析后的意图类型
    intent: str  # 意图类型（兼容字段）
    intent_cluster: str  # 意图聚类
    cluster: str  # 意图聚类（兼容字段）
    template_name: str  # 提示词模板名称
    context: dict[str, Any]  # RAG 检索上下文
    case_plan: str  # 测试计划
    code: str  # 代码（兼容旧字段）
    generated_code: str  # 生成的测试代码
    explanation: str  # LLM 回复中的非代码文字说明
    validation_result: dict[str, Any]  # 静态代码校验结果
    execution_plan: dict[str, Any]  # 执行计划
    execution_result: dict[str, Any]  # 沙盒执行结果
    parsed_result: dict[str, Any]  # 解析后的执行结果
    repair_suggestion: str  # 修复建议
    final_report: dict[str, Any]  # 最终报告
    retry: Annotated[int, operator.add]  # 重试计数（累加）
    repair_count: Annotated[int, operator.add]  # 修复计数（累加）
    saved_filepath: str  # 保存的文件路径

    # 沙盒执行循环相关字段
    sandbox_config: dict[str, Any]  # 沙盒配置（provider、image、timeout 等）
    sandbox_id: str  # 当前沙盒实例 ID
    sandbox_retry_count: int  # 沙盒重试计数
    max_sandbox_retries: int  # 最大沙盒重试次数
    feedback: str  # 沙盒失败后的反馈信息，用于重新规划
    error_log: Annotated[list[str], operator.add]  # 错误日志（累加）
    session_id: str  # 会话 ID


@dataclass
class AgentContext:
    """长期记忆上下文，通过 LangGraph Runtime 自动注入节点。

    用途：
    - 隔离不同用户/项目的记忆存储命名空间
    - 由 LangGraph Runtime 在调用节点时自动传入

    Attributes:
        user_id: 用户唯一标识，用于隔离不同用户的记忆
        project_id: 可选的项目/仓库标识，用于在同一个用户下区分不同项目记忆
    """

    user_id: str = "anonymous"  # 默认值兼容 Chat UI 无 user_id 的场景
    project_id: str | None = None


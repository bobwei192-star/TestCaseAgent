import operator
from dataclasses import dataclass
from typing import Annotated, Any, TypedDict


class AgentState(TypedDict, total=False):
    """Runtime state shared by all phase-one LangGraph nodes."""

    messages: Annotated[list, operator.add]
    requirement: str
    context: dict[str, Any]
    case_plan: str
    code: str
    generated_code: str
    validation_result: dict[str, Any]
    execution_plan: dict[str, Any]
    execution_result: dict[str, Any]
    parsed_result: dict[str, Any]
    repair_suggestion: str
    final_report: dict[str, Any]
    retry: Annotated[int, operator.add]
    repair_count: Annotated[int, operator.add]

    # ❌ 移除以下字段，改为 Store 长期记忆
    # user_profile: dict
    # historical_cases: list
    # repair_history: list


@dataclass
class AgentContext:
    """长期记忆上下文，通过 LangGraph Runtime 自动注入节点。

    Attributes:
        user_id: 用户唯一标识，用于隔离不同用户的记忆。
        project_id: 可选的项目/仓库标识，用于在同一个用户下区分不同项目记忆。
    """
    user_id: str
    project_id: str | None = None
"""Schema 级别的输入/输出验证模块（#13）。

提供 Pydantic 模型对各节点关键输出进行运行时校验：
- RequirementParserOutput: 需求解析节点输出
- PlannerOutput: 规划节点输出
- GeneratorOutput: 代码生成节点输出
- ExecutionOutput: 沙盒执行节点输出

用法：
    from .state_validator import validate_parser_output
    result = requirement_parser(state)
    validated = validate_parser_output(result)  # 返回 Pydantic 模型或抛出 ValidationError
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, ValidationError


class RequirementParserOutput(BaseModel):
    """需求解析节点的预期输出结构。"""

    parsed_requirement: str = Field(min_length=1, description="解析后的结构化需求文本")
    parsed_intent: str = Field(default="GENERATE", description="意图类型")
    intent: str = Field(default="GENERATE")
    intent_cluster: str = Field(default="create")
    cluster: str = Field(default="create")
    template_name: str = Field(default="template_a")


class PlannerOutput(BaseModel):
    """规划节点的预期输出结构。"""

    case_plan: str = Field(min_length=1, description="测试计划文本")
    execution_plan: dict[str, Any] = Field(default_factory=dict, description="执行计划")


class GeneratorOutput(BaseModel):
    """代码生成节点的预期输出结构。"""

    generated_code: str = Field(default="")
    code: str = Field(default="")
    explanation: str = Field(default="")
    validation_result: dict[str, Any] = Field(default_factory=dict)
    saved_filepath: str | None = Field(default=None)


class ExecutionOutput(BaseModel):
    """沙盒执行节点的预期输出结构。"""

    execution_result: dict[str, Any] = Field(description="执行结果，至少包含 status")
    feedback: str = Field(default="", description="失败反馈")
    sandbox_retry_count: int = Field(default=0, ge=0)
    error_log: list[str] = Field(default_factory=list)


def validate_parser_output(output: dict[str, Any]) -> RequirementParserOutput:
    """校验需求解析节点输出。"""
    return RequirementParserOutput(
        parsed_requirement=output.get("parsed_requirement", ""),
        parsed_intent=output.get("parsed_intent", "GENERATE"),
        intent=output.get("intent", "GENERATE"),
        intent_cluster=output.get("intent_cluster", "create"),
        cluster=output.get("cluster", "create"),
        template_name=output.get("template_name", "template_a"),
    )


def validate_planner_output(output: dict[str, Any]) -> PlannerOutput:
    """校验规划节点输出。"""
    return PlannerOutput(
        case_plan=output.get("case_plan", ""),
        execution_plan=output.get("execution_plan", {}),
    )


def validate_generator_output(output: dict[str, Any]) -> GeneratorOutput:
    """校验代码生成节点输出。"""
    return GeneratorOutput(
        generated_code=output.get("generated_code", ""),
        code=output.get("code", ""),
        explanation=output.get("explanation", ""),
        validation_result=output.get("validation_result", {}),
        saved_filepath=output.get("saved_filepath"),
    )


def validate_execution_output(output: dict[str, Any]) -> ExecutionOutput:
    """校验沙盒执行节点输出。"""
    return ExecutionOutput(
        execution_result=output.get("execution_result", {}),
        feedback=output.get("feedback", ""),
        sandbox_retry_count=output.get("sandbox_retry_count", 0),
        error_log=output.get("error_log", []),
    )

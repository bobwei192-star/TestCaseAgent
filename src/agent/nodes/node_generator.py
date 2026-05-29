"""测试代码生成节点 —— 使用底层 model 避免 HITL

根据 guide/09_promot优化.md 设计：
- 支持多种意图：GENERATE/APPEND/UPDATE/REFACTOR/EXECUTE_EXTERNAL/DIAGNOSE/COVERAGE/PROBE/ENV_BUILD
- 根据意图选择不同的提示词模板
- ENV_BUILD 意图生成 Dockerfile，其他意图生成测试代码
- 生成代码后自动进行安全审查（#40）
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.runtime import Runtime

from ..prompts import get_generator_prompt, get_prompt_by_template
from ..state import AgentState, AgentContext
from ..code_output import parse_llm_response
from ..code_security import review_code
from ..intent_router import IntentType
from ..logging_config import get_logger
from .utils import (
    _validate_real_test_code,
    _looks_like_python_code,
)

_logger = get_logger("nodes.generator")


def get_llm(model: Any = None) -> Any:
    """Module-level LLM accessor — patchable in tests."""
    return model


def get_memory_manager(runtime: Any = None) -> Any:
    """Module-level MemoryManager accessor — patchable in tests."""
    if runtime is None:
        return None
    from ..memory_manager import MemoryManager
    return MemoryManager(runtime)

OUTPUT_DIR = os.environ.get(
    "TEST_CASE_OUTPUT_DIR",
    str(Path(__file__).resolve().parents[3] / "test_case"),
)


def _save_test_file(code: str) -> str:
    """保存测试代码到文件，返回文件路径。"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_generated_{timestamp}.py"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    _logger.info("test_file_saved", filepath=filepath)
    return filepath


def generator(state: AgentState, runtime: Any = None, model: Any = None) -> dict:
    """
    使用底层 ChatOpenAI model 直接调用，避免 Agent 的 HITL 拦截。

    根据意图选择不同的生成策略：
    - GENERATE/APPEND/UPDATE/REFACTOR: 生成测试代码
    - ENV_BUILD: 生成 Dockerfile
    - EXECUTE_EXTERNAL: 生成外部执行脚本
    - DIAGNOSE/COVERAGE/PROBE: 查询类，不生成代码

    Args:
        model: 底层 ChatOpenAI 实例（从 graph.py 传入）
    """
    memory = get_memory_manager(runtime)

    # 获取意图信息
    parsed_intent: IntentType = state.get("parsed_intent", "GENERATE")
    template_name = state.get("template_name", "template_a")

    _logger.info(
        "generator_start",
        intent=parsed_intent,
        template=template_name,
        plan_len=len(state.get("case_plan", "")),
    )

    # 检查状态完整性
    if not state.get("case_plan"):
        _logger.warning("generator_empty_plan", state_keys=list(state.keys()))

    # 意图特定的记忆搜索
    memories = []
    memory_hints = ""
    if memory is not None:
        if parsed_intent == "ENV_BUILD":
            memories = memory.search("env_builds", query=state.get("case_plan", ""), limit=2)
        else:
            memories = memory.search("generations", query=state.get("case_plan", ""), limit=2)
        raw_hints = memory.format_hints(memories)
        memory_hints = raw_hints if isinstance(raw_hints, str) else ""
        _logger.debug("generator_memories", count=len(memories))

    # ========== 历史代码处理（修改/追加模式） ==========
    _MAX_PREVIOUS_CODE_CHARS = 5000
    previous_code = state.get("generated_code") or state.get("code", "")
    previous_code_hint = ""

    # 根据意图确定操作模式
    intent_to_action = {
        "APPEND": ("补充/追加", "保留所有历史测试函数，在其下方追加新函数"),
        "UPDATE": ("修改", "保留所有未修改的测试函数，只修改指定的部分"),
        "REFACTOR": ("重构", "保留测试逻辑，优化代码结构"),
    }

    action_desc, keep_desc = intent_to_action.get(parsed_intent, ("修改或补充", "保留所有历史测试函数，根据需求修改或追加"))

    if previous_code:
        truncated = previous_code
        if len(previous_code) > _MAX_PREVIOUS_CODE_CHARS:
            truncated = (
                previous_code[:_MAX_PREVIOUS_CODE_CHARS]
                + "\n# ... (已截断，上述代码太长)"
            )

        previous_code_hint = (
            f"\n\n【历史代码 - 必须在此基础上{action_desc}】\n"
            f"```python\n{truncated}\n```\n"
            f"注意：用户要求对代码进行{action_desc}操作。你必须输出修改后的**完整文件**，不要只返回差异或新增部分。\n"
            f"注意：{keep_desc}。禁止删除已有的测试函数。\n"
            f"注意：必须保持原始测试目标不变。如果原始代码测试的是 rocm-smi，修改后仍然必须测试 rocm-smi，"
            f"禁止把测试目标改成测试 helper 函数或内部封装。\n"
        )

    # 根据意图选择提示词模板
    if parsed_intent == "ENV_BUILD":
        # 使用 ENV_BUILD 专用模板
        prompt = get_prompt_by_template(
            template_name,
            intent=parsed_intent,
            case_plan=state.get("case_plan", ""),
            memory_hints=memory_hints,
        )
    elif parsed_intent in ["DIAGNOSE", "COVERAGE", "PROBE"]:
        # 查询类意图，使用简化模板
        prompt = get_prompt_by_template(
            template_name,
            intent=parsed_intent,
            case_plan=state.get("case_plan", ""),
        )
    else:
        # 测试代码生成意图
        prompt = get_generator_prompt(
            case_plan=state.get("case_plan", ""),
            memory_hints=memory_hints,
            previous_code_hint=previous_code_hint,
        )

    # ========== 直接调用底层 model ==========
    _logger.info("generator_invoke_model")
    try:
        effective_model = get_llm(model)
        if effective_model is None:
            raise RuntimeError("generator 需要传入底层 model 实例")

        response = effective_model.invoke([HumanMessage(content=prompt)])

        if hasattr(response, "content"):
            reply = response.content
        else:
            reply = str(response)

        _logger.debug("generator_model_response", chars=len(reply))

    except Exception as exc:
        _logger.exception("generator_model_failed", error=str(exc))
        return {
            "code": "",
            "generated_code": "",
            "explanation": f"Error: {exc}",
            "validation_result": {"status": "failed", "errors": [str(exc)]},
            "messages": [AIMessage(content=f"生成失败: {exc}")],
        }

    # 使用 Pydantic 友好的解析器（优先 JSON，失败回退正则）
    generated_code, explanation, extraction_status = parse_llm_response(reply)
    _logger.debug("generator_code_extracted", code_len=len(generated_code), status=extraction_status)

    # 安全审查（#40）：检查生成代码中的危险调用
    security_result = review_code(generated_code, sandbox_mode=True)
    if security_result.severity == "critical":
        _logger.warning(
            "generator_security_blocked",
            issues=security_result.issues,
        )
        return {
            "code": "",
            "generated_code": "",
            "explanation": f"代码安全审查未通过: {'; '.join(security_result.issues)}",
            "validation_result": {
                "status": "failed",
                "quality_gate": "security_review",
                "errors": security_result.issues,
            },
            "messages": [AIMessage(content=f"安全审查拦截: {'; '.join(security_result.issues)}")],
        }

    # 验证新代码
    if not generated_code:
        validation_result = {
            "status": "failed",
            "quality_gate": "real_pytest_code",
            "errors": ["LLM did not return valid Python code block."],
        }
    else:
        quality_issues = _validate_real_test_code(generated_code)
        validation_result = {
            "status": "failed" if quality_issues else "passed",
            "quality_gate": "real_pytest_code",
            "errors": quality_issues,
        }

    # 验证失败时保留上一轮有效代码
    old_code = state.get("generated_code") or state.get("code", "")
    final_code = generated_code

    if validation_result["status"] == "failed":
        if old_code and _looks_like_python_code(old_code)[0]:
            _logger.warning(
                "generator_validation_failed_keep_old",
                new_len=len(generated_code),
                old_len=len(old_code),
            )
            final_code = old_code
            validation_result["errors"].insert(
                0,
                f"New generation failed ({extraction_status}). Kept previous {len(old_code)} chars code.",
            )
        else:
            _logger.warning("generator_validation_failed_no_old")

    # 保存文件
    saved_filepath = None
    if final_code:
        saved_filepath = _save_test_file(final_code)
    else:
        _logger.warning("generator_no_valid_code")

    # 写入记忆
    if memory is not None:
        memory_key = memory.save_generation(
            requirement=state.get("requirement", ""),
            code=final_code,
            saved_filepath=saved_filepath,
        )
        # Also call save_memory for backward compatibility
        if hasattr(memory, "save_memory"):
            memory.save_memory(data=final_code, key=memory_key)
        _logger.info("generator_memory_saved", key=memory_key)

    return {
        "code": final_code,
        "generated_code": final_code,
        "explanation": explanation,
        "validation_result": validation_result,
        "saved_filepath": saved_filepath,
        "messages": [AIMessage(content=reply)],
    }
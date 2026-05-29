"""结构化代码输出模型 - 使用 Pydantic 替代手写正则提取"""

from typing import Optional
from pydantic import BaseModel, Field


class CodeGenerationOutput(BaseModel):
    """LLM 代码生成的结构化输出模型。"""

    model_config = {"extra": "ignore"}

    code: str = Field(description="生成的 pytest 测试代码")
    explanation: str = Field(description="代码的说明和注释", default="")
    status: str = Field(description="生成状态: success 或 failed", default="success")


def parse_llm_response(response: str) -> tuple[str, str, str]:
    """解析 LLM 响应，返回 (code, explanation, status)。

    优先尝试 JSON 解析，失败时回退到正则提取。

    Args:
        response: LLM 返回的原始文本

    Returns:
        (code, explanation, status) 元组
    """
    import json
    import re

    # 尝试从 JSON 中提取
    json_patterns = [
        r"```json\s*(.*?)\s*```",
        r"```JSON\s*(.*?)\s*```",
    ]

    for pattern in json_patterns:
        matches = re.findall(pattern, response, re.DOTALL)
        if matches:
            try:
                data = json.loads(matches[0].strip())
                if isinstance(data, dict):
                    code = data.get("code", "")
                    explanation = data.get("explanation", "")
                    status = data.get("status", "success")
                    return code, explanation, status
            except json.JSONDecodeError:
                pass

    # 尝试直接解析 JSON 对象
    for start in ["{", "\n{"]:
        json_start = response.find(start)
        if json_start >= 0:
            try:
                json_str = response[json_start:]
                brace_count = 0
                json_end = 0
                for i, char in enumerate(json_str):
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break
                if json_end > 0:
                    data = json.loads(json_str[:json_end])
                    if isinstance(data, dict):
                        code = data.get("code", "")
                        explanation = data.get("explanation", "")
                        status = data.get("status", "success")
                        return code, explanation, status
            except json.JSONDecodeError:
                pass

    # 回退到正则提取 Markdown 代码块
    return _fallback_regex_extract(response)


def _fallback_regex_extract(text: str) -> tuple[str, str, str]:
    """回退的正则提取逻辑。"""
    import re
    import ast

    if not text.strip():
        return "", "", "空回复"

    candidates = []

    # 提取 python 代码块
    python_blocks = re.findall(r"```python\s*(.*?)\s*```", text, re.DOTALL)
    candidates.extend(block.strip() for block in python_blocks)

    if not candidates:
        generic_blocks = re.findall(r"```\s*(.*?)\s*```", text, re.DOTALL)
        candidates.extend(block.strip() for block in generic_blocks)

    best_code = ""
    best_status = "未找到有效代码块"

    for candidate in candidates:
        is_valid = _validate_python_code(candidate)
        if is_valid:
            best_code = candidate
            best_status = "成功提取有效代码"
            break
        else:
            if best_status == "未找到有效代码块":
                best_code = candidate
                best_status = "代码块提取成功但验证失败"

    if not best_code:
        is_valid = _validate_python_code(text.strip())
        if is_valid:
            best_code = text.strip()
            best_status = "成功提取有效代码（无围栏）"
        else:
            best_status = "无围栏代码验证失败"

    explanation = re.sub(
        r"```(?:python)?\s*.*?\s*```", "", text, flags=re.DOTALL
    ).strip()
    explanation = re.sub(r"```python\s*.*$", "", explanation, flags=re.DOTALL).strip()

    return best_code, explanation, best_status


def _validate_python_code(code: str) -> bool:
    """验证 Python 代码是否有效。"""
    import ast

    if not code:
        return False

    stripped = code.strip()
    if not any(kw in stripped for kw in ("import ", "def ", "class ")):
        return False
    if "def test_" not in stripped:
        return False

    try:
        ast.parse(stripped)
        return True
    except SyntaxError:
        return False
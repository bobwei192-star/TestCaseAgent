"""从 src/agent/promot/ 加载提示词模板并格式化。"""

from pathlib import Path

_PROMPT_DIR = Path(__file__).resolve().parent / "promot"


def _load_prompt_text(name: str) -> str:
    """读取 .md 文件并返回去除了首尾空白的文本。"""
    filepath = _PROMPT_DIR / name
    if not filepath.exists():
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
    return filepath.read_text(encoding="utf-8").strip()


def get_requirement_parser_prompt(raw_requirement: str) -> str:
    """格式 requirement_parser 节点的提示词。"""
    tmpl = _load_prompt_text("node_requirement_parser.md")
    return tmpl.replace("{raw_requirement}", raw_requirement)


def get_planner_prompt(
    requirement: str,
    context: dict[str, str],
    memory_hints: str,
) -> str:
    """格式 planner 节点的提示词。"""
    tmpl = _load_prompt_text("node_planner.md")
    return (
        tmpl.replace("{requirement}", requirement)
        .replace("{context}", str(context))
        .replace("{memory_hints}", memory_hints)
    )


def get_generator_prompt(
    case_plan: str,
    memory_hints: str,
    previous_code_hint: str,
) -> str:
    """格式 generator 节点的提示词。"""
    tmpl = _load_prompt_text("node_generator.md")
    return (
        tmpl.replace("{case_plan}", case_plan)
        .replace("{memory_hints}", memory_hints)
        .replace("{previous_code_hint}", previous_code_hint)
    )

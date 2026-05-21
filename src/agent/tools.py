from langchain_core.tools import tool

import os
from pathlib import Path

_OUTPUT_BASE = os.environ.get("TEST_CASE_OUTPUT_DIR", str(Path.cwd() / "output"))


def _sanitize_output_path(filepath: str) -> Path:
    """Redirect absolute /test_case/... paths to the configured output directory.

    LLMs tend to hallucinate paths like ``/test_case/suites/...`` which are
    not writable or don't exist.  This function rewrites them under the
    project-scoped output base so writes never fail with PermissionError.
    """
    path = Path(filepath)
    if path.is_absolute():
        output_base = Path(_OUTPUT_BASE)
        rel = path.relative_to(path.anchor) if path.anchor else path.relative_to("/")
        resolved = output_base / rel
        print(f"[save_to_file] Rewriting {filepath} -> {resolved}")
        return resolved
    return Path(_OUTPUT_BASE) / path


@tool
def save_to_file(content: str, filepath: str) -> str:
    """将生成的代码写入文件（仅允许写入项目输出目录或其子目录）。

    Args:
        content: 要保存的代码内容
        filepath: 目标文件路径（相对或绝对）
    """
    target = _sanitize_output_path(filepath)

    # 安全阀：即使经过 rewrite，也确保不越狱到输出目录之外
    try:
        target.resolve().relative_to(Path(_OUTPUT_BASE).resolve())
    except ValueError:
        return f"❌ 拒绝写入: {filepath} 不属于输出目录 {_OUTPUT_BASE}"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"✅ 已保存到 {target}"


@tool
def read_file(filepath: str) -> str:
    """读取文件内容。

    Args:
        filepath: 文件路径
    """
    from pathlib import Path

    path = Path(filepath)
    if not path.exists():
        return f"\u274c 文件不存在: {filepath}"
    return path.read_text(encoding="utf-8")


TOOLS = [save_to_file, read_file]
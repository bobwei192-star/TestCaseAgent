from langchain_core.tools import tool


@tool
def save_to_file(content: str, filepath: str) -> str:
    """将生成的代码写入文件。

    Args:
        content: 要保存的代码内容
        filepath: 目标文件路径
    """
    from pathlib import Path

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"\u2705 已保存到 {filepath}"


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

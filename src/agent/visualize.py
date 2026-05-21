from pathlib import Path
from typing import Any
from .graph import build_graph

def export_agent_graph(
    output_prefix: str = "agent_architecture",
    graph: Any | None = None,
    xray: bool = True,
    export_png: bool = True,
) -> dict[str, str | None]:
    """导出 Test Case Agent 的 LangGraph 架构图。

    Args:
        output_prefix: 输出文件前缀，不包含扩展名。
        graph: 可选的已编译 LangGraph。未传入时构建可视化用默认图。
        xray: 是否展开 subgraph 内部节点。
        export_png: 是否尝试导出 PNG。PNG 依赖 mermaid-cli 或 LangGraph
            可用的 Mermaid 渲染后端。

    Returns:
        包含 Mermaid 文本路径、PNG 路径和 PNG 错误信息的字典。
    """
    compiled_graph = graph or build_graph()
    drawable_graph = compiled_graph.get_graph(xray=xray)

    mermaid_path = Path(f"{output_prefix}.mmd")
    mermaid_text = drawable_graph.draw_mermaid()
    mermaid_path.write_text(mermaid_text, encoding="utf-8")

    png_path: Path | None = None
    png_error: str | None = None
    if export_png:
        try:
            png_path = Path(f"{output_prefix}.png")
            png_path.write_bytes(drawable_graph.draw_mermaid_png())
        except Exception as exc:  # PNG is optional; Mermaid text is the fallback.
            png_path = None
            png_error = str(exc)

    return {
        "mermaid": str(mermaid_path),
        "png": str(png_path) if png_path else None,
        "png_error": png_error,
    }


def visualize_agent(output_prefix: str = "agent_architecture") -> None:
    """一键导出 Agent 架构图，并打印可复制到 mermaid.live 的路径。"""
    result = export_agent_graph(output_prefix=output_prefix)

    if result["png"]:
        print(f"PNG saved: {result['png']}")
    else:
        print(f"PNG failed: {result['png_error']}")

    print(f"Mermaid saved: {result['mermaid']}")
    print("Paste the .mmd content to https://mermaid.live to render.")


if __name__ == "__main__":
    visualize_agent()
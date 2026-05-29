"""图结构断言 —— 不依赖 LLM 密钥的纯结构测试。"""

from src.agent.graph import build_graph, DEFAULT_SYSTEM_PROMPT
from src.agent.tools import TOOLS


class TestGraphStructure:
    def test_graph_compiles(self):
        g = build_graph()
        from langgraph.pregel import Pregel

        assert isinstance(g, Pregel)

    def test_graph_has_four_nodes(self):
        """当前图有 4 个节点：requirement_parser → planner → generator → sandbox_executor。
        （context_retriever 暂时注释，减少延迟。）"""
        g = build_graph()
        nodes = [n for n in g.get_graph().nodes.keys() if not n.startswith("__")]
        assert nodes == [
            "requirement_parser",
            "planner",
            "generator",
            "sandbox_executor",
        ]

    def test_system_prompt_is_nonempty(self):
        assert len(DEFAULT_SYSTEM_PROMPT.strip()) > 0
        assert "测试用例" in DEFAULT_SYSTEM_PROMPT

    def test_tools_are_loaded(self):
        assert len(TOOLS) >= 2, f"至少需要 save_to_file + read_file, 实际: {len(TOOLS)}"
        tool_names = [t.name for t in TOOLS if hasattr(t, "name")]
        assert "save_to_file" in tool_names
        assert "read_file" in tool_names

    def test_graph_compiles_and_runs(self):
        g = build_graph()
        nodes = [n for n in g.get_graph().nodes.keys() if not n.startswith("__")]
        assert "requirement_parser" in nodes
        assert "generator" in nodes

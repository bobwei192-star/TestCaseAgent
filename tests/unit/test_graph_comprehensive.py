"""图流程和状态管理测试 - 新增 20 条测试"""

import os
import sys
from unittest.mock import Mock, patch, MagicMock
import pytest
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Interrupt
from langchain_core.messages import HumanMessage, AIMessage

from src.agent.state import AgentState
from src.agent.graph import build_graph
from src.agent.cli.cli_runner import (
    _node_failed,
    _is_node_complete,
    _extract_summary,
)


class TestGraphStructure:
    """测试图结构 - 9 条"""
    
    def test_build_graph_returns_graph(self):
        """测试 build_graph 返回图"""
        graph = build_graph()
        assert graph is not None
    
    def test_build_graph_with_args(self):
        """测试带参数构建"""
        graph = build_graph(model=None, checkpointer=None)
        assert graph is not None
    
    def test_graph_has_requirement_parser_node(self):
        """测试有 requirement_parser 节点"""
        graph = build_graph()
        nodes = graph.nodes.keys()
        assert "requirement_parser" in nodes
    
    def test_graph_has_context_retriever_node(self):
        """测试有 context_retriever 节点"""
        graph = build_graph()
        nodes = graph.nodes.keys()
        assert "context_retriever" in nodes
    
    def test_graph_has_planner_node(self):
        """测试有 planner 节点"""
        graph = build_graph()
        nodes = graph.nodes.keys()
        assert "planner" in nodes
    
    def test_graph_has_generator_node(self):
        """测试有 generator 节点"""
        graph = build_graph()
        nodes = graph.nodes.keys()
        assert "generator" in nodes
    
    def test_graph_has_sandbox_executor_node(self):
        """测试有 sandbox_executor 节点"""
        graph = build_graph()
        nodes = graph.nodes.keys()
        assert "sandbox_executor" in nodes
    
    def test_graph_has_five_nodes(self):
        """测试有5个核心节点"""
        graph = build_graph()
        core_nodes = [
            "requirement_parser",
            "context_retriever",
            "planner",
            "generator",
            "sandbox_executor"
        ]
        for node in core_nodes:
            assert node in graph.nodes


class TestNodeFailureDetection:
    """测试节点失败检测 - 5 条"""
    
    def test_node_failed_sandbox_executor_success(self):
        """测试 sandox 成功的情况"""
        result = _node_failed(
            "sandbox_executor",
            {"execution_result": {"status": "success"}}
        )
        assert result is False
    
    def test_node_failed_sandbox_executor_failure(self):
        """测试 sandbox 失败的情况"""
        result = _node_failed(
            "sandbox_executor",
            {"execution_result": {"status": "failed"}}
        )
        assert result is True
    
    def test_node_failed_other_nodes(self):
        """测试其他节点（默认不失败）"""
        result = _node_failed("planner", {})
        assert result is False
    
    def test_node_failed_missing_execution_result(self):
        """测试缺少 execution_result"""
        result = _node_failed("sandbox_executor", {})
        assert result is False
    
    def test_node_failed_wrong_status_type(self):
        """测试 status 不是字符串"""
        result = _node_failed(
            "sandbox_executor",
            {"execution_result": {"status": 123}}
        )
        # 应该不会崩溃
        assert isinstance(result, bool)


class TestNodeCompletionDetection:
    """测试节点完成检测 - 10 条"""
    
    def test_node_complete_requirement_parser_has_parsed(self):
        """测试 requirement_parser 有 parsed_requirement"""
        result = _is_node_complete(
            "requirement_parser",
            {"parsed_requirement": "spec"}
        )
        assert result is True
    
    def test_node_complete_requirement_parser_missing_parsed(self):
        """测试 requirement_parser 缺少 parsed_requirement"""
        result = _is_node_complete("requirement_parser", {})
        assert result is False
    
    def test_node_complete_context_retriever_has_context(self):
        """测试 context_retriever 有 context"""
        result = _is_node_complete(
            "context_retriever",
            {"context": "some context"}
        )
        assert result is True
    
    def test_node_complete_planner_has_case_plan(self):
        """测试 planner 有 case_plan"""
        result = _is_node_complete(
            "planner",
            {"case_plan": "plan"}
        )
        assert result is True
    
    def test_node_complete_generator_has_generated_code(self):
        """测试 generator 有 generated_code"""
        result = _is_node_complete(
            "generator",
            {"generated_code": "code"}
        )
        assert result is True
    
    def test_node_complete_sandbox_has_execution_result(self):
        """测试 sandbox_executor 有 execution_result"""
        result = _is_node_complete(
            "sandbox_executor",
            {"execution_result": {"status": "done"}}
        )
        assert result is True
    
    def test_node_complete_unknown_node_defaults_true(self):
        """测试未知节点默认为完成"""
        result = _is_node_complete("unknown_node", {})
        assert result is True
    
    def test_node_complete_empty_output(self):
        """测试空输出"""
        result = _is_node_complete("planner", {})
        assert result is False
    
    def test_node_complete_all_fields_present(self):
        """测试所有字段都有"""
        state = {
            "parsed_requirement": "spec",
            "context": "ctx",
            "case_plan": "plan",
            "generated_code": "code",
            "execution_result": {"status": "ok"}
        }
        for node in [
            "requirement_parser",
            "context_retriever",
            "planner",
            "generator",
            "sandbox_executor"
        ]:
            result = _is_node_complete(node, state)
            assert result is True


class TestSummaryExtraction:
    """测试摘要提取 - 3 条"""
    
    def test_extract_summary_requirement_parser(self):
        """测试需求解析节点摘要提取"""
        summary = _extract_summary(
            "requirement_parser",
            {"parsed_requirement": "test spec"}
        )
        assert isinstance(summary, str)
    
    def test_extract_summary_planner(self):
        """测试计划节点摘要提取"""
        summary = _extract_summary(
            "planner",
            {"case_plan": "test plan"}
        )
        assert isinstance(summary, str)
    
    def test_extract_summary_generator(self):
        """测试生成节点摘要提取"""
        summary = _extract_summary(
            "generator",
            {"generated_code": "test code"}
        )
        assert isinstance(summary, str)


class TestStateFlow:
    """测试状态流动 - 5 条"""
    
    def test_state_can_hold_parsed_requirement(self):
        """测试状态可以保存解析需求"""
        state = AgentState()
        state["parsed_requirement"] = "test spec"
        assert state["parsed_requirement"] == "test spec"
    
    def test_state_can_hold_case_plan(self):
        """测试状态可以保存计划"""
        state = AgentState()
        state["case_plan"] = "test plan"
        assert state["case_plan"] == "test plan"
    
    def test_state_can_hold_generated_code(self):
        """测试状态可以保存生成代码"""
        state = AgentState()
        state["generated_code"] = "test code"
        assert state["generated_code"] == "test code"
    
    def test_state_can_hold_execution_result(self):
        """测试状态可以保存执行结果"""
        state = AgentState()
        state["execution_result"] = {"status": "success"}
        assert state["execution_result"]["status"] == "success"
    
    def test_state_chain_passing(self):
        """测试状态链式传递"""
        state = AgentState()
        state["parsed_requirement"] = "spec"
        state["case_plan"] = "plan"
        state["generated_code"] = "code"
        state["execution_result"] = {"status": "done"}
        
        assert len(state) >= 4

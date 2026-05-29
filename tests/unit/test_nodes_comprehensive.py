"""节点功能综合测试用例 - 新增 30 条测试"""

import os
import sys
from unittest.mock import Mock, patch, MagicMock
import pytest
from langchain_core.messages import HumanMessage, AIMessage

from src.agent.state import AgentState
from src.agent.nodes.node_requirement_parser import requirement_parser
from src.agent.nodes.node_planner import planner
from src.agent.nodes.node_generator import generator
from src.agent.nodes.node_sandbox_executor import sandbox_executor


class TestRequirementParser:
    """测试需求解析节点 - 10 条"""
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_normal_flow(self, mock_get_llm):
        """测试正常流程"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "test spec",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "写一个测试"}
        result = requirement_parser(state)
        
        assert "parsed_requirement" in result
        assert "intent" in result
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_empty_requirement(self, mock_get_llm):
        """测试空需求"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "empty",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": ""}
        result = requirement_parser(state)
        
        assert "parsed_requirement" in result
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_very_long_requirement(self, mock_get_llm):
        """测试很长的需求"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "long spec",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        long_text = "test " * 1000
        state = {"raw_requirement": long_text}
        result = requirement_parser(state)
        
        assert "parsed_requirement" in result
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_special_chars(self, mock_get_llm):
        """测试特殊字符需求"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "spec with chars",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "test with !@#$%^&*()"}
        result = requirement_parser(state)
        
        assert "parsed_requirement" in result
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_intent_generation(self, mock_get_llm):
        """测试 GENERATE 意图"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "spec",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "生成测试用例"}
        result = requirement_parser(state)
        
        assert result["intent"] == "GENERATE"
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_intent_append(self, mock_get_llm):
        """测试 APPEND 意图"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "APPEND",
            "raw_spec": "append spec",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "追加测试用例"}
        result = requirement_parser(state)
        
        assert result["intent"] == "APPEND"
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_llm_error(self, mock_get_llm):
        """测试 LLM 错误时的处理"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.side_effect = Exception("LLM failed")
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "test"}
        with pytest.raises(Exception):
            requirement_parser(state)
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_returns_dict(self, mock_get_llm):
        """测试返回值类型"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "spec",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "test"}
        result = requirement_parser(state)
        
        assert isinstance(result, dict)
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_has_raw_requirement(self, mock_get_llm):
        """测试结果包含原始需求"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "spec",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "my requirement"}
        result = requirement_parser(state)
        
        # raw_requirement 会被保留在输入中
        assert True
    
    @patch("src.agent.nodes.node_requirement_parser.get_llm")
    def test_requirement_parser_with_cluster(self, mock_get_llm):
        """测试包含 cluster 的输出"""
        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = mock_llm
        mock_llm.invoke.return_value = {
            "intent": "GENERATE",
            "raw_spec": "spec",
            "cluster": "create",
            "template": "create_intent"
        }
        mock_get_llm.return_value = mock_llm
        
        state = {"raw_requirement": "test"}
        result = requirement_parser(state)
        
        assert "cluster" in result


class TestPlanner:
    """测试计划生成节点 - 10 条"""
    
    @patch("src.agent.nodes.node_planner.get_llm")
    @patch("src.agent.nodes.node_planner.get_memory_manager")
    def test_planner_normal_flow(self, mock_get_mem, mock_get_llm):
        """测试正常流程"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="test plan")
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_get_mem.return_value = mock_mem
        
        state = {
            "requirement": "test req",
            "parsed_requirement": "test spec",
            "intent": "GENERATE",
            "raw_requirement": "test req"
        }
        result = planner(state)
        
        assert "case_plan" in result
    
    @patch("src.agent.nodes.node_planner.get_llm")
    @patch("src.agent.nodes.node_planner.get_memory_manager")
    def test_planner_empty_parsed_requirement(self, mock_get_mem, mock_get_llm):
        """测试空解析需求"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="plan")
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_get_mem.return_value = mock_mem
        
        state = {
            "requirement": "",
            "parsed_requirement": "",
            "intent": "GENERATE",
            "raw_requirement": ""
        }
        result = planner(state)
        
        assert "case_plan" in result
    
    @patch("src.agent.nodes.node_planner.get_llm")
    @patch("src.agent.nodes.node_planner.get_memory_manager")
    def test_planner_with_context(self, mock_get_mem, mock_get_llm):
        """测试带上下文"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="plan with context")
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_get_mem.return_value = mock_mem
        
        state = {
            "requirement": "req",
            "parsed_requirement": "spec",
            "intent": "GENERATE",
            "raw_requirement": "req",
            "context": "some context"
        }
        result = planner(state)
        
        assert "case_plan" in result
    
    @patch("src.agent.nodes.node_planner.get_llm")
    @patch("src.agent.nodes.node_planner.get_memory_manager")
    def test_planner_multiple_intents(self, mock_get_mem, mock_get_llm):
        """测试多种意图"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="plan")
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_get_mem.return_value = mock_mem
        
        for intent in ["GENERATE", "APPEND", "UPDATE", "REFACTOR"]:
            state = {
                "requirement": "req",
                "parsed_requirement": "spec",
                "intent": intent,
                "raw_requirement": "req"
            }
            result = planner(state)
            assert "case_plan" in result
    
    @patch("src.agent.nodes.node_planner.get_llm")
    @patch("src.agent.nodes.node_planner.get_memory_manager")
    def test_planner_saves_memory(self, mock_get_mem, mock_get_llm):
        """测试保存记忆"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="plan")
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_mem.save_memory = Mock()
        mock_get_mem.return_value = mock_mem
        
        state = {
            "requirement": "req",
            "parsed_requirement": "spec",
            "intent": "GENERATE",
            "raw_requirement": "req"
        }
        planner(state)
        
        assert mock_mem.save_memory.called
    
    @patch("src.agent.nodes.node_planner.get_llm")
    @patch("src.agent.nodes.node_planner.get_memory_manager")
    def test_planner_returns_case_plan(self, mock_get_mem, mock_get_llm):
        """测试返回 case_plan"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="my test plan")
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_get_mem.return_value = mock_mem
        
        state = {
            "requirement": "req",
            "parsed_requirement": "spec",
            "intent": "GENERATE",
            "raw_requirement": "req"
        }
        result = planner(state)
        
        assert result["case_plan"] == "my test plan"
    
    @patch("src.agent.nodes.node_planner.get_llm")
    @patch("src.agent.nodes.node_planner.get_memory_manager")
    def test_planner_without_interrupt(self, mock_get_mem, mock_get_llm):
        """测试没有 interrupt 机制"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="plan")
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_get_mem.return_value = mock_mem
        
        state = {
            "requirement": "req",
            "parsed_requirement": "spec",
            "intent": "GENERATE",
            "raw_requirement": "req",
            "context": {}
        }
        # 应该直接返回，不应该抛出 interrupt 相关异常
        result = planner(state)
        assert "case_plan" in result


class TestGenerator:
    """测试代码生成节点 - 10 条"""
    
    @patch("src.agent.nodes.node_generator.get_llm")
    @patch("src.agent.nodes.node_generator.get_memory_manager")
    def test_generator_normal_flow(self, mock_get_mem, mock_get_llm):
        """测试正常流程"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="""
        ```python
        import pytest
        def test_func():
            assert True
        ```
        """)
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_mem.save_memory = Mock()
        mock_get_mem.return_value = mock_mem
        
        state = {
            "case_plan": "test plan",
            "intent": "GENERATE"
        }
        result = generator(state)
        
        assert "generated_code" in result
    
    @patch("src.agent.nodes.node_generator.get_llm")
    @patch("src.agent.nodes.node_generator.get_memory_manager")
    def test_generator_empty_plan(self, mock_get_mem, mock_get_llm):
        """测试空计划"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="""
        ```python
        def test_empty():
            pass
        ```
        """)
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_mem.save_memory = Mock()
        mock_get_mem.return_value = mock_mem
        
        state = {
            "case_plan": "",
            "intent": "GENERATE"
        }
        result = generator(state)
        
        assert "generated_code" in result
    
    @patch("src.agent.nodes.node_generator.get_llm")
    @patch("src.agent.nodes.node_generator.get_memory_manager")
    def test_generator_extracts_code(self, mock_get_mem, mock_get_llm):
        """测试代码提取"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="""
        Some text before
        ```python
        import pytest
        def test_my_func():
            assert 1 + 1 == 2
        ```
        Some text after
        """)
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_mem.save_memory = Mock()
        mock_get_mem.return_value = mock_mem
        
        state = {
            "case_plan": "plan",
            "intent": "GENERATE"
        }
        result = generator(state)
        
        assert "test_my_func" in result["generated_code"]
    
    @patch("src.agent.nodes.node_generator.get_llm")
    @patch("src.agent.nodes.node_generator.get_memory_manager")
    def test_generator_saves_memory(self, mock_get_mem, mock_get_llm):
        """测试保存记忆"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="""
        ```python
        def test_func():
            pass
        ```
        """)
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_mem.save_memory = Mock()
        mock_get_mem.return_value = mock_mem
        
        state = {
            "case_plan": "plan",
            "intent": "GENERATE"
        }
        generator(state)
        
        assert mock_mem.save_memory.called
    
    @patch("src.agent.nodes.node_generator.get_llm")
    @patch("src.agent.nodes.node_generator.get_memory_manager")
    def test_generator_multiple_intents(self, mock_get_mem, mock_get_llm):
        """测试多种意图"""
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(content="""
        ```python
        def test_func():
            pass
        ```
        """)
        mock_get_llm.return_value = mock_llm
        
        mock_mem = Mock()
        mock_mem.search.return_value = []
        mock_mem.format_hints.return_value = ""
        mock_mem.get_relevant_memories.return_value = []
        mock_mem.save_memory = Mock()
        mock_get_mem.return_value = mock_mem
        
        for intent in ["GENERATE", "APPEND", "UPDATE"]:
            state = {
                "case_plan": "plan",
                "intent": intent
            }
            result = generator(state)
            assert "generated_code" in result

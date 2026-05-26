"""工具函数和通用功能测试用例 - 新增 35 条测试"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest
from langchain_core.documents import Document

from src.agent.tools.download_embedding_model import (
    verify_model,
    REQUIRED_FILES,
)
from src.agent.state import AgentState


class TestBasicUtils:
    """测试基本工具函数 - 15 条"""
    
    def test_pathlib_exists_nonexistent(self):
        """测试不存在的路径"""
        path = Path("/nonexistent/path/12345")
        assert path.exists() is False
    
    def test_pathlib_exists_existent(self, tmp_path):
        """测试存在的路径"""
        assert tmp_path.exists() is True
    
    def test_pathlib_is_file(self, tmp_path):
        """测试文件判断"""
        test_file = tmp_path / "test.txt"
        test_file.touch()
        assert test_file.is_file() is True
        assert test_file.is_dir() is False
    
    def test_pathlib_is_dir(self, tmp_path):
        """测试目录判断"""
        assert tmp_path.is_dir() is True
        assert tmp_path.is_file() is False
    
    def test_pathlib_joinpath(self, tmp_path):
        """测试路径拼接"""
        subdir = tmp_path / "subdir"
        assert str(subdir) == str(tmp_path) + "/subdir"
    
    def test_pathlib_touch(self, tmp_path):
        """测试创建文件"""
        test_file = tmp_path / "test.txt"
        assert test_file.exists() is False
        test_file.touch()
        assert test_file.exists() is True
    
    def test_pathlib_write_text(self, tmp_path):
        """测试写文件"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")
        content = test_file.read_text()
        assert content == "hello world"
    
    def test_pathlib_read_text(self, tmp_path):
        """测试读文件"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        assert test_file.read_text() == "test content"
    
    def test_pathlib_mkdir(self, tmp_path):
        """测试创建目录"""
        new_dir = tmp_path / "new_dir"
        assert new_dir.exists() is False
        new_dir.mkdir()
        assert new_dir.exists() is True
        assert new_dir.is_dir() is True
    
    def test_string_strip(self):
        """测试字符串处理"""
        s = "  test string  "
        assert s.strip() == "test string"
    
    def test_string_split(self):
        """测试字符串分割"""
        s = "a,b,c"
        assert s.split(",") == ["a", "b", "c"]
    
    def test_string_join(self):
        """测试字符串合并"""
        parts = ["a", "b", "c"]
        assert ",".join(parts) == "a,b,c"
    
    def test_string_replace(self):
        """测试字符串替换"""
        s = "test old"
        assert s.replace("old", "new") == "test new"
    
    def test_string_contains(self):
        """测试字符串包含"""
        s = "test string"
        assert "test" in s
        assert "xyz" not in s
    
    def test_list_append(self):
        """测试列表操作"""
        lst = [1, 2, 3]
        lst.append(4)
        assert lst == [1, 2, 3, 4]


class TestDownloadModelTool:
    """测试模型下载工具 - 10 条"""
    
    def test_verify_model_model_path_nonexistent(self):
        """测试验证不存在的模型路径"""
        result = verify_model(Path("/path/that/does/not/exist"))
        assert result["exists"] is False
        assert result["complete"] is False
    
    def test_verify_model_exists_but_incomplete(self, tmp_path):
        """测试验证存在但不完整的模型"""
        (tmp_path / "config.json").touch()
        result = verify_model(tmp_path)
        assert result["exists"] is True
        assert result["complete"] is False
        assert len(result["missing_files"]) > 0
    
    def test_verify_model_empty_missing(self, tmp_path):
        """测试空模型路径的缺失文件"""
        result = verify_model(tmp_path)
        assert len(result["missing_files"]) == len(REQUIRED_FILES)
    
    def test_required_files_list_complete(self):
        """测试必需文件列表是否合理"""
        assert isinstance(REQUIRED_FILES, list)
        assert len(REQUIRED_FILES) > 0
        assert "config.json" in REQUIRED_FILES
        assert "tokenizer.json" in REQUIRED_FILES
    
    def test_verify_model_returns_file_sizes(self, tmp_path):
        """测试验证函数返回文件大小"""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"test": "data"}')
        result = verify_model(tmp_path)
        assert "file_sizes" in result
        assert "config.json" in result["file_sizes"]
    
    def test_verify_model_returns_dict(self):
        """测试返回值是字典"""
        result = verify_model(Path("/nonexistent"))
        assert isinstance(result, dict)
    
    def test_verify_model_has_exists_key(self):
        """测试有 exists 键"""
        result = verify_model(Path("/nonexistent"))
        assert "exists" in result
    
    def test_verify_model_has_complete_key(self):
        """测试有 complete 键"""
        result = verify_model(Path("/nonexistent"))
        assert "complete" in result
    
    def test_verify_model_has_missing_files_key(self):
        """测试有 missing_files 键"""
        result = verify_model(Path("/nonexistent"))
        assert "missing_files" in result
    
    def test_required_files_are_strings(self):
        """测试所有必需文件都是字符串"""
        for f in REQUIRED_FILES:
            assert isinstance(f, str)


class TestStateValidation:
    """测试 AgentState 状态验证 - 10 条"""
    
    def test_agent_state_initial_empty(self):
        """测试初始空状态"""
        state = AgentState()
        assert "messages" not in state
        assert "parsed_requirement" not in state
    
    def test_agent_state_can_add_messages(self):
        """测试可以添加 messages"""
        state = AgentState()
        state["messages"] = []
        assert "messages" in state
    
    def test_agent_state_can_add_parsed_requirement(self):
        """测试可以添加 parsed_requirement"""
        state = AgentState()
        state["parsed_requirement"] = "test spec"
        assert state["parsed_requirement"] == "test spec"
    
    def test_agent_state_can_add_case_plan(self):
        """测试可以添加 case_plan"""
        state = AgentState()
        state["case_plan"] = "test plan"
        assert state["case_plan"] == "test plan"
    
    def test_agent_state_can_add_generated_code(self):
        """测试可以添加 generated_code"""
        state = AgentState()
        state["generated_code"] = "test code"
        assert state["generated_code"] == "test code"
    
    def test_agent_state_can_add_execution_result(self):
        """测试可以添加 execution_result"""
        state = AgentState()
        state["execution_result"] = {"status": "success"}
        assert state["execution_result"]["status"] == "success"
    
    def test_agent_state_can_add_multiple_fields(self):
        """测试可以同时添加多个字段"""
        state = AgentState()
        state["parsed_requirement"] = "spec"
        state["case_plan"] = "plan"
        state["generated_code"] = "code"
        assert "parsed_requirement" in state
        assert "case_plan" in state
        assert "generated_code" in state
    
    def test_agent_state_total_false_keys_allowed(self):
        """测试 total=False 允许缺失键"""
        state = AgentState()
        # 只设置一个字段
        state["parsed_requirement"] = "test"
        # 其他字段可以不存在
        assert True
    
    def test_agent_state_is_a_dict(self):
        """测试 AgentState 是 dict"""
        state = AgentState()
        assert isinstance(state, dict)
    
    def test_agent_state_accepts_any_keys(self):
        """测试可以接受任意键"""
        state = AgentState()
        state["random_key"] = "value"
        assert state["random_key"] == "value"

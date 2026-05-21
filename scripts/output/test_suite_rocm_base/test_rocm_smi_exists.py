"""
测试套件：ROCm 基础环境
========================
测试目标：验证 rocm-smi 工具是否存在且可执行
测试方式：真实调用 subprocess.run 执行 rocm-smi --help
"""

import shutil
import subprocess
import pytest


ROCM_SMI = "rocm-smi"


def _rocm_smi_path() -> str | None:
    """返回 rocm-smi 的完整路径，若不存在则返回 None。"""
    return shutil.which(ROCM_SMI)


def _rocm_smi_help() -> subprocess.CompletedProcess:
    """执行 rocm-smi --help 并返回 CompletedProcess。"""
    return subprocess.run(
        [ROCM_SMI, "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )


# ---------------------------------------------------------------------------
# 测试用例
# ---------------------------------------------------------------------------

def test_rocm_smi_in_path():
    """验证 rocm-smi 在 PATH 中可被找到。"""
    path = _rocm_smi_path()
    assert path is not None, (
        f"'{ROCM_SMI}' 未在 PATH 中找到。"
        f"请确认 ROCm 已正确安装且 {ROCM_SMI} 在 PATH 中。"
    )
    assert isinstance(path, str) and len(path) > 0


def test_rocm_smi_executable():
    """验证 rocm-smi 文件存在且具有可执行权限。"""
    path = _rocm_smi_path()
    if path is None:
        pytest.skip(f"'{ROCM_SMI}' 不在 PATH 中，跳过可执行性检查")
    assert shutil.os.access(path, shutil.os.X_OK), (
        f"'{path}' 存在但不可执行"
    )


def test_rocm_smi_help_exit_code():
    """验证 rocm-smi --help 返回码为 0。"""
    path = _rocm_smi_path()
    if path is None:
        pytest.skip(f"'{ROCM_SMI}' 不在 PATH 中，跳过帮助信息检查")
    result = _rocm_smi_help()
    assert result.returncode == 0, (
        f"'{ROCM_SMI} --help' 返回非零退出码 {result.returncode}\n"
        f"stderr: {result.stderr.strip()}"
    )


def test_rocm_smi_help_output_not_empty():
    """验证 rocm-smi --help 输出不为空。"""
    path = _rocm_smi_path()
    if path is None:
        pytest.skip(f"'{ROCM_SMI}' 不在 PATH 中，跳过输出内容检查")
    result = _rocm_smi_help()
    assert result.returncode == 0
    combined = (result.stdout + result.stderr).strip()
    assert len(combined) > 0, (
        f"'{ROCM_SMI} --help' 输出为空"
    )


def test_rocm_smi_help_contains_identifier():
    """验证 rocm-smi --help 输出包含 'rocm-smi' 标识。"""
    path = _rocm_smi_path()
    if path is None:
        pytest.skip(f"'{ROCM_SMI}' 不在 PATH 中，跳过标识检查")
    result = _rocm_smi_help()
    assert result.returncode == 0
    combined = (result.stdout + result.stderr).lower()
    assert "rocm-smi" in combined, (
        f"'{ROCM_SMI} --help' 输出中未找到 'rocm-smi' 标识\n"
        f"stdout: {result.stdout[:500]}"
    )


def test_rocm_smi_help_no_error_keywords():
    """验证 rocm-smi --help 输出中不包含 error/failed/traceback 等错误关键字。"""
    path = _rocm_smi_path()
    if path is None:
        pytest.skip(f"'{ROCM_SMI}' 不在 PATH 中，跳过错误关键字检查")
    result = _rocm_smi_help()
    assert result.returncode == 0
    combined = (result.stdout + result.stderr).lower()
    error_keywords = ["error", "failed", "traceback", "exception"]
    found = [kw for kw in error_keywords if kw in combined]
    assert len(found) == 0, (
        f"'{ROCM_SMI} --help' 输出中包含错误关键字: {found}\n"
        f"stderr: {result.stderr[:500]}"
    )

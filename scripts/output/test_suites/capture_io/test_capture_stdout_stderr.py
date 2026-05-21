"""
测试套件: capture_io — IO 捕获验证

验证 pytest 测试用例能够正确捕获被测试命令/脚本的 stdout 和 stderr 输出。
所有测试均通过 subprocess.run 真实调用目标脚本，无 mock、无硬编码成功输出。

测试策略:
  - 使用 tmp_path fixture 动态生成辅助脚本，避免依赖外部文件
  - 通过 subprocess.run(capture_output=True, text=True) 捕获输出
  - 断言 stdout 和 stderr 被正确分离捕获，互不污染
  - 平台兼容: 使用 shell=True 或纯 Python 脚本避免 shebang 依赖
"""

import subprocess
import sys
import textwrap

import pytest


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def echo_script(tmp_path):
    """动态生成一个可产生 stdout 和 stderr 的辅助脚本。

    脚本行为:
      - 向 stdout 输出 "STDOUT_MESSAGE"
      - 向 stderr 输出 "STDERR_MESSAGE"
      - 以 exit code 0 退出

    使用纯 Python 脚本以避免平台相关的 shebang 问题。
    """
    script = tmp_path / "echo_helper.py"
    script.write_text(
        textwrap.dedent(
            """\
        import sys

        sys.stdout.write("STDOUT_MESSAGE\\n")
        sys.stdout.flush()
        sys.stderr.write("STDERR_MESSAGE\\n")
        sys.stderr.flush()
        sys.exit(0)
        """
        ),
        encoding="utf-8",
    )
    return script


@pytest.fixture
def echo_script_error(tmp_path):
    """动态生成一个向 stderr 输出错误信息并以非零退出的脚本。

    脚本行为:
      - 向 stdout 输出 "STDOUT_OK"
      - 向 stderr 输出 "ERROR: something went wrong"
      - 以 exit code 1 退出
    """
    script = tmp_path / "echo_error.py"
    script.write_text(
        textwrap.dedent(
            """\
        import sys

        sys.stdout.write("STDOUT_OK\\n")
        sys.stdout.flush()
        sys.stderr.write("ERROR: something went wrong\\n")
        sys.stderr.flush()
        sys.exit(1)
        """
        ),
        encoding="utf-8",
    )
    return script


# ============================================================
# 测试用例: 正常输出捕获
# ============================================================


class TestCaptureStdout:
    """验证 stdout 捕获的正确性。"""

    def test_stdout_contains_expected_message(self, echo_script):
        """使用 subprocess.run 捕获 stdout，验证包含预期消息。"""
        result = subprocess.run(
            [sys.executable, str(echo_script)],
            capture_output=True,
            text=True,
        )
        assert "STDOUT_MESSAGE" in result.stdout, (
            f"stdout 应包含 'STDOUT_MESSAGE', 实际 stdout={result.stdout!r}"
        )

    def test_stdout_not_contaminated_by_stderr(self, echo_script):
        """验证 stdout 中不包含 stderr 的内容。"""
        result = subprocess.run(
            [sys.executable, str(echo_script)],
            capture_output=True,
            text=True,
        )
        assert "STDERR_MESSAGE" not in result.stdout, (
            f"stdout 不应包含 stderr 内容, 实际 stdout={result.stdout!r}"
        )


class TestCaptureStderr:
    """验证 stderr 捕获的正确性。"""

    def test_stderr_contains_expected_message(self, echo_script):
        """使用 subprocess.run 捕获 stderr，验证包含预期消息。"""
        result = subprocess.run(
            [sys.executable, str(echo_script)],
            capture_output=True,
            text=True,
        )
        assert "STDERR_MESSAGE" in result.stderr, (
            f"stderr 应包含 'STDERR_MESSAGE', 实际 stderr={result.stderr!r}"
        )

    def test_stderr_not_contaminated_by_stdout(self, echo_script):
        """验证 stderr 中不包含 stdout 的内容。"""
        result = subprocess.run(
            [sys.executable, str(echo_script)],
            capture_output=True,
            text=True,
        )
        assert "STDOUT_MESSAGE" not in result.stderr, (
            f"stderr 不应包含 stdout 内容, 实际 stderr={result.stderr!r}"
        )


class TestCaptureBothStreams:
    """验证 stdout 和 stderr 同时被正确捕获且互不污染。"""

    def test_both_streams_captured_separately(self, echo_script):
        """同时验证 stdout 和 stderr 的内容正确性。"""
        result = subprocess.run(
            [sys.executable, str(echo_script)],
            capture_output=True,
            text=True,
        )

        # stdout 验证
        assert result.stdout == "STDOUT_MESSAGE\n", (
            f"stdout 内容不匹配, 实际 stdout={result.stdout!r}"
        )
        # stderr 验证
        assert result.stderr == "STDERR_MESSAGE\n", (
            f"stderr 内容不匹配, 实际 stderr={result.stderr!r}"
        )
        # 互不污染验证
        assert "STDERR_MESSAGE" not in result.stdout, (
            f"stdout 被 stderr 污染, 实际 stdout={result.stdout!r}"
        )
        assert "STDOUT_MESSAGE" not in result.stderr, (
            f"stderr 被 stdout 污染, 实际 stderr={result.stderr!r}"
        )

    def test_returncode_zero_for_success(self, echo_script):
        """验证正常执行的脚本返回码为 0。"""
        result = subprocess.run(
            [sys.executable, str(echo_script)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"预期 returncode=0, 实际 returncode={result.returncode}, "
            f"stderr={result.stderr!r}"
        )


class TestCaptureErrorOutput:
    """验证错误场景下的输出捕获。"""

    def test_stderr_contains_error_on_failure(self, echo_script_error):
        """验证非零退出时 stderr 包含错误信息。"""
        result = subprocess.run(
            [sys.executable, str(echo_script_error)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"预期非零 returncode, 实际 returncode={result.returncode}"
        )
        assert "ERROR" in result.stderr, (
            f"stderr 应包含 'ERROR', 实际 stderr={result.stderr!r}"
        )

    def test_stdout_still_captured_on_failure(self, echo_script_error):
        """验证即使脚本失败，stdout 仍然被正确捕获。"""
        result = subprocess.run(
            [sys.executable, str(echo_script_error)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, (
            f"预期非零 returncode, 实际 returncode={result.returncode}"
        )
        assert "STDOUT_OK" in result.stdout, (
            f"即使失败 stdout 也应被捕获, 实际 stdout={result.stdout!r}"
        )


class TestCaptureEdgeCases:
    """验证边界场景。"""

    def test_empty_stdout(self, tmp_path):
        """验证脚本不产生 stdout 时 stdout 为空字符串。"""
        script = tmp_path / "no_stdout.py"
        script.write_text(
            textwrap.dedent(
                """\
            import sys
            sys.stderr.write("only stderr\\n")
            sys.exit(0)
            """
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
        )
        assert result.stdout == "", (
            f"预期 stdout 为空, 实际 stdout={result.stdout!r}"
        )
        assert "only stderr" in result.stderr

    def test_empty_stderr(self, tmp_path):
        """验证脚本不产生 stderr 时 stderr 为空字符串。"""
        script = tmp_path / "no_stderr.py"
        script.write_text(
            textwrap.dedent(
                """\
            import sys
            sys.stdout.write("only stdout\\n")
            sys.exit(0)
            """
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
        )
        assert result.stderr == "", (
            f"预期 stderr 为空, 实际 stderr={result.stderr!r}"
        )
        assert "only stdout" in result.stdout

    def test_large_output(self, tmp_path):
        """验证大量输出仍能被完整捕获（10000 行）。"""
        script = tmp_path / "large_output.py"
        script.write_text(
            textwrap.dedent(
                """\
            import sys
            for i in range(10000):
                sys.stdout.write(f"line {i}\\n")
            sys.stderr.write("DONE\\n")
            sys.exit(0)
            """
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
        )
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 10000, (
            f"预期 10000 行 stdout, 实际 {len(lines)} 行"
        )
        assert lines[0] == "line 0"
        assert lines[-1] == "line 9999"
        assert result.stderr == "DONE\n"

    def test_binary_output_handling(self, tmp_path):
        """验证二进制输出场景（不使用 text=True）仍能捕获。"""
        script = tmp_path / "binary_output.py"
        script.write_text(
            textwrap.dedent(
                """\
            import sys
            sys.stdout.buffer.write(b"\\x00\\x01\\x02\\n")
            sys.stdout.buffer.flush()
            sys.exit(0)
            """
            ),
            encoding="utf-8",
        )
        # 不使用 text=True，捕获 bytes
        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=False,
        )
        assert isinstance(result.stdout, bytes), (
            f"text=False 时 stdout 应为 bytes, 实际类型={type(result.stdout)}"
        )
        assert result.stdout == b"\x00\x01\x02\n", (
            f"stdout 内容不匹配, 实际 stdout={result.stdout!r}"
        )


class TestSubprocessApiUsage:
    """验证不同的 subprocess API 使用方式。"""

    def test_subprocess_run_with_shell_true(self, echo_script):
        """验证 shell=True 模式下仍能正确捕获输出。"""
        result = subprocess.run(
            f"{sys.executable} {echo_script}",
            shell=True,
            capture_output=True,
            text=True,
        )
        assert "STDOUT_MESSAGE" in result.stdout, (
            f"shell=True 模式下 stdout 捕获失败, 实际 stdout={result.stdout!r}"
        )
        assert "STDERR_MESSAGE" in result.stderr, (
            f"shell=True 模式下 stderr 捕获失败, 实际 stderr={result.stderr!r}"
        )

    def test_subprocess_popen_communicate(self, echo_script):
        """验证 subprocess.Popen + communicate() 也能正确捕获输出。"""
        with subprocess.Popen(
            [sys.executable, str(echo_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ) as proc:
            stdout, stderr = proc.communicate()

        assert "STDOUT_MESSAGE" in stdout, (
            f"Popen.communicate() stdout 捕获失败, 实际 stdout={stdout!r}"
        )
        assert "STDERR_MESSAGE" in stderr, (
            f"Popen.communicate() stderr 捕获失败, 实际 stderr={stderr!r}"
        )
        assert proc.returncode == 0

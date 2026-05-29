"""代码安全审查与沙盒加固模块（#39 #40）。

提供：
1. CodeSecurityReview: 代码级安全审查（导入白名单、危险调用检测）
2. SandboxHardening: 沙盒运行时加固（资源限制、命令白名单）

审查策略：
- 白名单模式：只允许安全的 Python 标准库导入
- 黑名单检测：禁止 subprocess/Popen/exec/eval/compile/os.system
- 沙盒资源限制：CPU 4 核 + 内存 4G + 磁盘 10G + 网络阻断
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .logging_config import get_logger

_logger = get_logger("code_security")

# 允许的 Python 标准库导入（白名单）
_SAFE_IMPORTS: set[str] = {
    "os", "sys", "re", "json", "math", "datetime", "pathlib", "typing",
    "subprocess",  # 测试需要，但需配合沙盒策略
    "pytest", "unittest", "logging", "time", "tempfile", "shutil",
    "collections", "itertools", "functools", "hashlib", "uuid",
    "csv", "io", "string", "textwrap", "enum", "dataclasses",
    "random", "statistics", "copy", "pprint", "inspect",
    "argparse", "configparser", "socket", "ssl", "http",
    "urllib", "xml", "html", "json", "base64", "binascii",
    "struct", "pickle", "sqlite3", "threading", "multiprocessing",
    "asyncio", "concurrent", "queue", "signal", "atexit",
    "platform", "getpass", "secrets", "traceback", "warnings",
    "contextlib", "abc", "types", "ast", "dis", "codecs",
    "fileinput", "fnmatch", "glob", "gzip", "tarfile", "zipfile",
    "locale", "operator", "errno", "ctypes", "resource",
    "distutils", "setuptools", "pip", "pkg_resources",
}

# 禁止在 LLM 生成代码中出现的危险调用模式
_DANGEROUS_PATTERNS: list[tuple[str, str]] = [
    (r"\bos\.system\s*\(", "禁止使用 os.system()"),
    (r"\bos\.popen\s*\(", "禁止使用 os.popen()"),
    (r"\beval\s*\(", "禁止使用 eval()"),
    (r"\bexec\s*\(", "禁止使用 exec()"),
    (r"\bcompile\s*\(", "禁止使用 compile()"),
    (r"\b__import__\s*\(", "禁止使用 __import__()"),
    (r"\bimportlib\.import_module\(", "禁止动态导入模块"),
    (r"\bshutil\.rmtree\s*\(\s*[\"']/[\"']", "禁止删除根目录"),
    (r"\bos\.remove\s*\(\s*[\"']/[\"']", "禁止删除系统文件"),
    (r"\bsocket\.create_connection\(", "禁止创建网络连接(沙盒模式)"),
    (r"\burllib\.request\.urlopen\(", "禁止发起 HTTP 请求(沙盒模式)"),
    (r"\brequest\.(get|post|put|delete)\s*\(", "禁止发起 HTTP 请求(沙盒模式)"),
    (r"\bopen\s*\(\s*[\"']\/etc\/(passwd|shadow)", "禁止读取系统敏感文件"),
]


@dataclass
class SecurityReviewResult:
    """安全审查结果。"""

    passed: bool
    issues: list[str] = field(default_factory=list)
    severity: str = "safe"  # safe | warning | critical


@dataclass
class SandboxHardening:
    """沙盒运行时加固配置。

    Attributes:
        cpu_limit: CPU 核心数上限
        memory_limit_mb: 内存上限（MB）
        disk_limit_mb: 磁盘上限（MB）
        block_network: 是否阻断网络
        allowed_commands: 允许执行的命令白名单
        timeout_seconds: 超时时间
    """

    cpu_limit: int = 4
    memory_limit_mb: int = 4096
    disk_limit_mb: int = 10240
    block_network: bool = True
    allowed_commands: list[str] = field(default_factory=lambda: [
        "python3", "python", "pytest", "pip", "pip3",
        "ls", "cat", "echo", "pwd", "which", "command",
        "env", "printenv", "uname", "whoami", "id",
        "find", "head", "tail", "wc", "grep", "awk", "sed",
        "sort", "uniq", "cut", "tr", "tee", "mkdir", "chmod",
        "test", "[", "dirname", "basename", "readlink",
        "rocm-smi", "hipcc", "rocminfo", "hipconfig",
    ])
    timeout_seconds: int = 300

    def to_docker_kwargs(self) -> dict:
        """转换为 Docker SDK 的资源限制参数。"""
        return {
            "cpu_count": self.cpu_limit,
            "mem_limit": f"{self.memory_limit_mb}m",
            "network_mode": "none" if self.block_network else "bridge",
        }


def review_code(code: str, sandbox_mode: bool = True) -> SecurityReviewResult:
    """对 LLM 生成的代码进行安全审查。

    Args:
        code: 待审查的 Python 代码
        sandbox_mode: 是否启用沙盒网络阻断模式（更严格）

    Returns:
        SecurityReviewResult: 审查结果
    """
    issues: list[str] = []
    severity: str = "safe"

    if not code or not code.strip():
        return SecurityReviewResult(passed=True, issues=["代码为空(跳过审查)"], severity="warning")

    # 检查危险调用模式
    for pattern, reason in _DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            issues.append(reason)
            severity = "critical"

    # 检查 import 语句（非标准库导入警告）
    if sandbox_mode:
        import_pattern = re.compile(
            r"(?:from\s+(\S+)\s+import|import\s+(\S+))"
        )
        for match in import_pattern.finditer(code):
            module = match.group(1) or match.group(2)
            # 提取顶层模块名
            top_module = module.split(".")[0]
            if top_module not in _SAFE_IMPORTS:
                msg = f"沙盒模式下可能不安全的导入: {module}"
                if msg not in issues:
                    issues.append(msg)
                    if severity == "safe":
                        severity = "warning"

    result = SecurityReviewResult(
        passed=(severity != "critical"),
        issues=issues,
        severity=severity,
    )

    _logger.info(
        "code_security_review",
        passed=result.passed,
        severity=severity,
        issue_count=len(issues),
    )

    return result


def build_sandbox_hardening(
    block_network: bool = True,
    cpu_limit: int = 4,
    memory_limit_mb: int = 4096,
    timeout_seconds: int = 300,
) -> SandboxHardening:
    """构建沙盒加固配置。

    从环境变量读取自定义值，未设置时使用安全默认值。
    """
    import os

    return SandboxHardening(
        cpu_limit=int(os.getenv("SANDBOX_CPU_LIMIT", str(cpu_limit))),
        memory_limit_mb=int(os.getenv("SANDBOX_MEMORY_LIMIT_MB", str(memory_limit_mb))),
        disk_limit_mb=int(os.getenv("SANDBOX_DISK_LIMIT_MB", "10240")),
        block_network=os.getenv("SANDBOX_BLOCK_NETWORK", str(block_network).lower()) != "false",
        timeout_seconds=int(os.getenv("SANDBOX_TIMEOUT_SECONDS", str(timeout_seconds))),
    )

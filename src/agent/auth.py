"""LangGraph Platform 鉴权模块 —— 简单 API Key / JWT 鉴权。

生产环境建议使用 OAuth2/OIDC 或 API Key。
开发/测试环境可通过环境变量 LANGFUSE_AUTH_DISABLED=true 跳过鉴权。
"""

import os
from typing import Optional


def auth(authorization: Optional[str] = None) -> str:
    """LangGraph Platform auth handler.

    Args:
        authorization: HTTP Authorization header value

    Returns:
        用户标识字符串

    Raises:
        Exception: 鉴权失败时抛出 401
    """
    # 测试/开发环境可跳过鉴权
    if os.environ.get("LANGFUSE_AUTH_DISABLED", "false").lower() == "true":
        return "anonymous"

    # API Key 鉴权
    api_key = os.environ.get("TEST_CASE_AGENT_API_KEY", "")
    if not api_key:
        # 未配置 API Key 时允许无鉴权（开发环境兼容）
        return "anonymous"

    if not authorization:
        raise Exception("Missing Authorization header")

    # Bearer token
    if authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        token = authorization

    if token != api_key:
        raise Exception("Invalid API key")

    return "authenticated_user"

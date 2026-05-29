"""LangGraph Platform 鉴权模块 —— 简单 API Key / JWT 鉴权。

生产环境建议使用 OAuth2/OIDC 或 API Key。
开发/测试环境可通过环境变量 LANGFUSE_AUTH_DISABLED=true 跳过鉴权。
"""

import os
from typing import Optional

from langgraph_sdk import Auth

auth = Auth()


@auth.authenticate
async def authenticate(authorization: Optional[str] = None) -> Auth.types.MinimalUserDict:
    """LangGraph Platform auth handler.

    Args:
        authorization: HTTP Authorization header value

    Returns:
        MinimalUserDict: 至少包含 identity 字段的字典

    Raises:
        Auth.exceptions.HTTPException: 鉴权失败时抛出 401
    """
    # 测试/开发环境可跳过鉴权
    if os.environ.get("LANGFUSE_AUTH_DISABLED", "false").lower() == "true":
        return {"identity": "anonymous"}

    # API Key 鉴权
    api_key = os.environ.get("TEST_CASE_AGENT_API_KEY", "")
    if not api_key:
        # 未配置 API Key 时允许无鉴权（开发环境兼容）
        return {"identity": "anonymous"}

    if not authorization:
        raise Auth.exceptions.HTTPException(
            status_code=401, detail="Missing Authorization header"
        )

    # Bearer token
    token = authorization.split(" ", 1)[-1] if " " in authorization else authorization

    if token != api_key:
        raise Auth.exceptions.HTTPException(
            status_code=401, detail="Invalid API key"
        )

    return {"identity": "authenticated_user"}

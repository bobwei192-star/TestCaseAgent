import ast
from .state import AgentState


def coder(state: AgentState, agent) -> dict:
    """调用 LLM Agent 生成测试代码。"""
    result = agent.invoke({"messages": state["messages"]})
    last_msg = result["messages"][-1]
    reply = last_msg.content

    code = ""
    if "```python" in reply:
        code = reply.split("```python")[1].split("```")[0].strip()
    elif "```" in reply:
        code = reply.split("```")[1].split("```")[0].strip()

    return {"messages": [{"role": "assistant", "content": reply}], "code": code}


def checker(state: AgentState) -> dict:
    """校验生成的 Python 代码语法。"""
    code = state.get("code", "")
    if not code:
        return {
            "messages": [{"role": "assistant", "content": "\u274c 未生成有效代码"}],
            "retry": 1,
        }
    try:
        tree = ast.parse(code)
        funcs = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        imports = [n.names[0].name if hasattr(n, "names") and n.names else "" for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
        details = f"\u2705 语法通过 | {len(funcs)} 个函数, {len(imports)} 个 import"
        return {"messages": [{"role": "assistant", "content": details}]}
    except SyntaxError as e:
        return {
            "messages": [{"role": "assistant", "content": f"\u274c 语法错误: {e}"}],
            "retry": 1,
        }


def router(state: AgentState) -> str:
    """决定下一步: 通过 / 重试 / 放弃。"""
    retry = state.get("retry", 0)
    last_content = str(state["messages"][-1]["content"])

    if retry >= 3:
        return "giveup"
    if "\u2705" in last_content or "\u2705" in last_content:
        return "ok"
    return "retry"

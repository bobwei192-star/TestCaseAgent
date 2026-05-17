# 初始化一个 pyproject.toml 文件（如果还没有）
uv init
# 使用 main 分支安装 langgraph-kit（包括你需要的 deepagents 和 anthropic 扩展）
uv add "langgraph-kit[deepagents,anthropic] @ git+https://github.com/allada-homelab/langgraph-kit.git"
# 现在应该可以正常找到 langgraph_kit.cli 模块了
python -m langgraph_kit.cli new Test_Case_Agent
pip install langgraph langchain-openai
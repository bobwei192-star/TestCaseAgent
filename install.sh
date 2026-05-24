#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }
log_step()  { echo -e "\n${BLUE}[STEP $1/$TOTAL_STEPS]${NC} $2"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
TOTAL_STEPS=7
log_info "Project root: $SCRIPT_DIR"

# ─────────────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────────────

_docker_ok() {
    if ! command -v docker >/dev/null 2>&1; then
        log_error "Docker 未安装，跳过容器部署。"
        log_info "安装 Docker: curl -fsSL https://get.docker.com | bash"
        return 1
    fi
    if docker compose version >/dev/null 2>&1; then
        DOCKER_COMPOSE="docker compose"
    elif command -v docker-compose >/dev/null 2>&1; then
        DOCKER_COMPOSE="docker-compose"
    else
        log_error "docker compose / docker-compose 都不可用，跳过容器部署。"
        return 1
    fi
    return 0
}

_container_running() {
    docker ps --format '{{.Names}}' 2>/dev/null | grep -q "$1"
}

# ─────────────────────────────────────────────────────
# Step 1-5: Python 环境
# ─────────────────────────────────────────────────────

log_step 1 "Create and activate project virtual environment"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    log_info "Created .venv"
else
    log_warn ".venv already exists, reuse it"
fi
source .venv/bin/activate
log_info "python: $(command -v python)"
log_info "VIRTUAL_ENV: ${VIRTUAL_ENV:-}"
python --version

log_step 2 "Upgrade pip & install project"
python -m pip install --upgrade pip -q

log_step 3 "Install project requirements (including RAG + CLI deps)"
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip install \
    typer rich \
    langchain-community langchain-text-splitters \
    langchain-huggingface langchain-chroma chromadb \
    sentence-transformers \
    torch --index-url https://download.pytorch.org/whl/cpu
pip install prompt_toolkit
log_step 4 "Install DeepAgents"
if [ -f "etc/deepagents/pyproject.toml" ] || [ -f "etc/deepagents/setup.py" ]; then
    python -m pip install -e etc/deepagents
else
    python -m pip install deepagents
fi

log_step 5 "Verify core dependencies"
python - <<'PY'
import importlib.util, sys
modules = {
    "langgraph": "langgraph",
    "langchain": "langchain",
    "langchain_openai": "langchain_openai",
    "langfuse": "langfuse",
    "deepagents": "deepagents",
    "typer": "typer",
    "rich": "rich",
}
missing = []
for label, name in modules.items():
    ok = importlib.util.find_spec(name) is not None
    print(f"  {label}: {'✅' if ok else '❌ NOT INSTALLED'}")
    if not ok:
        missing.append(label)
if missing:
    sys.exit(f"Missing: {', '.join(missing)}")
PY
pip install langchain-cli

if ! command -v langgraph >/dev/null 2>&1; then
    log_error "langgraph CLI is not available in .venv"
    exit 1
fi
langgraph --version

# ─────────────────────────────────────────────────────
# Step 6: Langfuse (Docker)
# ─────────────────────────────────────────────────────

log_step 6 "Deploy Langfuse (Docker Compose, http://localhost:3000)"
LF_REPO="https://github.com/langfuse/langfuse.git"
LF_DIR="$SCRIPT_DIR/etc/langfuse"

if _docker_ok; then
    if _container_running "langfuse"; then
        log_warn "Langfuse 容器已在运行，跳过部署。"
    else
        if [ ! -d "$LF_DIR" ]; then
            git clone --depth 1 "$LF_REPO" "$LF_DIR"
            log_info "Cloned langfuse -> $LF_DIR"
            cat > "$LF_DIR/.env" <<DOTENV
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=$(openssl rand -hex 32 2>/dev/null || echo "mysecret-changeme")
SALT=$(openssl rand -hex 16 2>/dev/null || echo "mysalt-changeme")
ENCRYPTION_KEY=$(openssl rand -hex 32 2>/dev/null || echo "0000000000000000000000000000000000000000000000000000000000000000")
TELEMETRY_ENABLED=true
LANGFUSE_ENABLE_EXPERIMENTAL_FEATURES=true
DOTENV
            log_info "Created .env (auto-generated secrets)"
        else
            log_warn "langfuse 源码已存在，重新启动..."
        fi
        cd "$LF_DIR"
        if [ -f "docker-compose.yml" ]; then
            $DOCKER_COMPOSE up -d
            log_info "Langfuse started. Access: http://localhost:3000"
        else
            log_error "docker-compose.yml not found in $LF_DIR"
        fi
        cd "$SCRIPT_DIR"
    fi
fi

# ─────────────────────────────────────────────────────
# Step 7: Chat UI (local pnpm)
# ─────────────────────────────────────────────────────

log_step 7 "Setup LangGraph Chat UI (local pnpm)"
UI_REPO="https://github.com/braincrew-lab/langgraph-chat-ui.git"
UI_DIR="$SCRIPT_DIR/etc/langgraph-chat-ui"

if ! command -v node >/dev/null 2>&1; then
    log_error "Node.js 未安装，Chat UI 需要 Node.js 22+。跳过。"
    log_info "安装: curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt install -y nodejs"
else
    log_info "Node.js: $(node -v)"
    if ! command -v pnpm >/dev/null 2>&1; then
        npm install -g pnpm
    fi
    log_info "pnpm: $(pnpm -v)"

    if [ ! -d "$UI_DIR" ]; then
        git clone "$UI_REPO" "$UI_DIR"
        log_info "Cloned langgraph-chat-ui -> $UI_DIR"
    else
        log_warn "chat-ui 源码已存在，跳过克隆"
    fi

    if [ ! -f "$UI_DIR/frontend/.env" ]; then
        cat > "$UI_DIR/frontend/.env" <<'DOTENV'
NEXT_PUBLIC_LANGGRAPH_API_URL=http://127.0.0.1:2024
NEXT_PUBLIC_ASSISTANT_ID=test_case_agent
NEXT_PUBLIC_AUTH_MODE=standalone
DOTENV
        log_info "Created frontend/.env (standalone mode)"
    fi

    cd "$UI_DIR/frontend"
    if [ -f "node_modules/.bin/next" ]; then
        log_warn "frontend dependencies 已存在，跳过安装"
    else
        rm -rf node_modules
        echo "onlyBuiltDependencies=esbuild" >> .npmrc
        pnpm install --ignore-workspace
        log_info "Frontend dependencies installed"
    fi
    cd "$SCRIPT_DIR"
fi

# ─────────────────────────────────────────────────────
# 完成提示
# ─────────────────────────────────────────────────────

echo ""
echo -e "${BLUE}================================================================================${NC}"
echo -e "${GREEN}                      安装完成 — TestCaseAgent${NC}"
echo ""
echo -e "${BLUE}┌─ 服务概览 ──────────────────────────────────────────────────────────────────┐${NC}"
printf "  %-28s %s\n" "LangGraph API"    "http://127.0.0.1:2024   (launch: langgraph dev)"
printf "  %-28s %s\n" "Langfuse"         "http://localhost:3000     (Docker)"
printf "  %-28s %s\n" "Chat UI"          "http://localhost:3001     (pnpm dev --port 3001)"
printf "  %-28s %s\n" "CLI"              "python -m src.agent.cli run/chat/status"
echo -e "${BLUE}└──────────────────────────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${YELLOW}┌─ 启动步骤 ──────────────────────────────────────────────────────────────────┐${NC}"
echo -e "  ${GREEN}1.${NC} Langfuse: ${GREEN}http://localhost:3000${NC} → 注册 → Settings → API Keys → 填入 .env"
echo -e "  ${GREEN}2.${NC} langgraph dev        ${BLUE}(终端1)${NC}"
echo -e "  ${GREEN}3.${NC} pnpm dev --port 3001   ${BLUE}(终端2, cd etc/langgraph-chat-ui/frontend)${NC}"
echo -e "  ${GREEN}4.${NC} Chat UI: ${GREEN}http://localhost:3001${NC}"
echo -e "  ${GREEN}5.${NC} CLI:     python -m src.agent.cli run \"提示词\""
echo -e "${YELLOW}└──────────────────────────────────────────────────────────────────────────────┘${NC}"

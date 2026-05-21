#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }
log_step() { echo -e "\n${BLUE}[STEP $1/6]${NC} $2"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_info "Project root: $SCRIPT_DIR"

log_step 1 "Create and activate project virtual environment"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    log_info "Created .venv"
else
    log_warn ".venv already exists, reuse it"
fi

# shellcheck disable=SC1091
source .venv/bin/activate

log_info "python: $(command -v python)"
log_info "pip: $(command -v pip)"
log_info "VIRTUAL_ENV: ${VIRTUAL_ENV:-}"
python --version

log_step 2 "Upgrade pip"
python -m pip install --upgrade pip

log_step 3 "Install project requirements"
python -m pip install -r requirements.txt

log_step 4 "Install DeepAgents"
if [ -f "etc/deepagents/pyproject.toml" ] || [ -f "etc/deepagents/setup.py" ]; then
    python -m pip install -e etc/deepagents
else
    python -m pip install deepagents
fi

log_step 5 "Install project package and verify LangGraph Studio dependencies"
python -m pip install -e .

python - <<'PY'
import importlib.util

required_modules = [
    "langgraph",
    "langchain",
    "langchain_openai",
    "langfuse",
    "deepagents",
]

missing = []
for name in required_modules:
    spec = importlib.util.find_spec(name)
    status = "OK" if spec else "NOT INSTALLED"
    print(f"{name}: {status}")
    if spec is None:
        missing.append(name)

if missing:
    raise SystemExit(f"Missing required modules: {', '.join(missing)}")
PY

if ! command -v langgraph >/dev/null 2>&1; then
    log_error "langgraph CLI is not available in .venv"
    exit 1
fi

langgraph --version

log_step 6 "Clone DeployAgent and run deployment"
cd "$SCRIPT_DIR"
if [ ! -d "DeployAgent" ]; then
    git clone https://github.com/bobwei192-star/DeployAgent.git
    log_info "Cloned DeployAgent"
else
    log_warn "DeployAgent already exists, reuse it"
fi
cd DeployAgent
sudo deploy all -Langfuse -autodetect_ip
cd "$SCRIPT_DIR"

echo ""
log_info "Install completed."
echo -e "Activate environment: ${YELLOW}source .venv/bin/activate${NC}"
echo -e "Start LangGraph Studio: ${YELLOW}langgraph dev${NC}"
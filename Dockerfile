FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip -q \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir deepagents \
    && pip install --no-cache-dir \
        typer rich \
        langchain-community langchain-text-splitters \
        langchain-huggingface langchain-chroma chromadb \
        sentence-transformers \
        torch --extra-index-url https://download.pytorch.org/whl/cpu

COPY . .
RUN pip install -e . --no-deps

ENV PYTHONUNBUFFERED=1
EXPOSE 2024

CMD ["langgraph", "dev", "--host", "0.0.0.0", "--port", "2024"]

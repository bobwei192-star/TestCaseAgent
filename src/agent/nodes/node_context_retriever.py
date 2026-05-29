"""RAG 上下文检索节点 —— 官方 LangChain 模式（InMemoryVectorStore + 懒加载 + 多源下载）

与官方 guide/06_官方rag.md 对齐：
- 向量库在首次检索时创建，避免 pytest collection 阶段加载重依赖
- 从 Chroma 持久化目录一次性加载到内存后，Chroma client 即关闭
- 所有查询走 InMemoryVectorStore，不存在连接断开问题
- 支持多源下载模型（10秒超时自动切换）
"""

import os
import time
import gc
from pathlib import Path
from typing import Any

from langchain_core.documents import Document  # noqa: E402
from langchain_core.vectorstores import InMemoryVectorStore  # noqa: E402
from ..state import AgentState  # noqa: E402

_CHROMA_DIR = Path(
    os.environ.get("TEST_CASE_AGENT_CHROMA_DIR", "./chroma_langchain_db")
)

# 本地模型缓存目录（优先使用 HOME 目录下的项目路径）
_LOCAL_MODEL_DIR = Path(os.environ.get(
    "TEST_CASE_AGENT_MODEL_DIR",
    str(Path.home() / "TestCaseAgent" / "llm_model")
))

# 模型名称
_EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# 嵌入模型实例（线程安全懒加载单例）
import threading

_embeddings: Any | None = None
_vectorstore: InMemoryVectorStore | None = None
_load_error: str | None = None
_lock = threading.Lock()


def _download_model_with_fallback() -> str | None:
    """
    下载 embedding 模型，支持多源阶梯下载（10秒超时自动切换）
    
    尝试顺序：
    1. 使用本地已缓存的模型
    2. 使用优化后的多源下载器下载模型
    3. 使用 HuggingFace 默认下载
    
    Returns:
        模型路径或模型名称，None 表示失败
    """
    local_model_path = _LOCAL_MODEL_DIR / "all-MiniLM-L6-v2"
    
    # 检查本地模型是否完整
    if local_model_path.exists():
        required_files = ["config.json", "pytorch_model.bin", "tokenizer.json"]
        if all((local_model_path / f).exists() for f in required_files):
            print(f"[RAG] ✅ 本地模型已存在: {local_model_path}")
            return str(local_model_path)
        else:
            print(f"[RAG] ⚠️ 本地模型不完整，需要重新下载")
    
    # 尝试使用优化后的下载器
    print(f"[RAG] 📥 尝试多源下载模型...")
    try:
        # 动态导入，避免模块导入时引入 torch
        from ..tools.download_embedding_model import download_model
        
        # 调用优化后的多源下载器（10秒超时自动切换）
        if download_model(
            model_name=_EMBEDDING_MODEL_NAME,
            local_dir=_LOCAL_MODEL_DIR,
            force=False  # 不强制下载，如果本地有部分文件会断点续传
        ):
            # 验证下载结果
            if local_model_path.exists():
                required_files = ["config.json", "pytorch_model.bin", "tokenizer.json"]
                if all((local_model_path / f).exists() for f in required_files):
                    print(f"[RAG] ✅ 多源下载成功: {local_model_path}")
                    return str(local_model_path)
        
        print(f"[RAG] ⚠️ 多源下载失败或文件不完整")
        
    except Exception as e:
        print(f"[RAG] ❌ 调用下载器失败: {type(e).__name__}: {e}")
    
    # 回退到直接使用 HuggingFace 默认下载
    print(f"[RAG] 🔄 回退到 HuggingFace 默认下载...")
    return _EMBEDDING_MODEL_NAME


def _get_embeddings() -> Any:
    """
    懒加载 HuggingFace embeddings，支持多源下载
    
    处理策略：
    1. 优先使用本地缓存
    2. 使用多源下载器（10秒超时自动切换）
    3. 回退到 HuggingFace 默认下载
    4. 添加重试机制处理临时网络问题
    """
    global _embeddings, _load_error

    if _embeddings is not None:
        return _embeddings

    # 导入 HuggingFace embeddings
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as exc:
        _load_error = (
            "缺少 RAG embedding 依赖，请安装: "
            "pip install langchain-huggingface sentence-transformers"
        )
        raise RuntimeError(_load_error) from exc

    # 获取模型路径（支持多源下载）
    model_to_use = _download_model_with_fallback()
    
    if model_to_use is None:
        _load_error = "无法获取 embedding 模型"
        raise RuntimeError(_load_error)
    
    # 先检查 HuggingFace 缓存
    _hf_cache_dir = Path(os.environ.get("HF_HUB_CACHE", os.path.expanduser("~/.cache/huggingface/hub")))
    _hf_model_dir = _hf_cache_dir / "models--sentence-transformers--all-MiniLM-L6-v2" / "snapshots"
    _hf_cached = False
    if _hf_model_dir.exists() and any(_hf_model_dir.iterdir()):
        # 检查 snapshot 目录下是否有完整模型文件
        for snap_dir in _hf_model_dir.iterdir():
            if snap_dir.is_dir() and (snap_dir / "pytorch_model.bin").exists():
                _hf_cached = True
                print(f"[RAG] 💾 HuggingFace 缓存已命中: {snap_dir}")
                break
    
    if _hf_cached:
        print(f"[RAG] ℹ️  将从 HuggingFace 缓存直接加载，无需下载")
    else:
        print(f"[RAG] 🌐 HuggingFace 缓存未命中，将自动从网络下载模型...")
    
    # 尝试加载模型（最多重试 3 次）
    max_retries = 3
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            _embeddings = HuggingFaceEmbeddings(
                model_name=model_to_use,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )
            _load_error = None  # 成功加载，清除之前的错误
            print(f"[RAG] ✅ embedding 模型加载成功 (来源: {'HF缓存' if _hf_cached else '网络下载'})")
            return _embeddings
            
        except Exception as exc:
            last_exception = exc
            print(f"[RAG] ⚠️ embedding 加载失败 (尝试 {attempt + 1}/{max_retries}): {exc}")
            
            # 如果是从本地加载失败，尝试使用默认下载
            if model_to_use != _EMBEDDING_MODEL_NAME:
                print(f"[RAG] 🔄 切换到 HuggingFace 默认下载...")
                model_to_use = _EMBEDDING_MODEL_NAME
                # 重新下载模型
                _download_model_with_fallback()
            
            # 重置状态，允许下次重试
            _embeddings = None
            if attempt < max_retries - 1:
                time.sleep(1)  # 等待 1 秒后重试

    _load_error = f"embedding 加载失败 ({max_retries} 次尝试): {last_exception}"
    print(f"[RAG] ❌ {_load_error}")
    raise RuntimeError(_load_error) from last_exception


def _init_vectorstore() -> InMemoryVectorStore:
    """
    首次检索时从 Chroma 持久化目录一次性加载到 InMemoryVectorStore。
    
    之后所有查询走内存，不再依赖 Chroma client 连接。
    
    处理策略：
    1. 懒加载 embedding 模型（支持多源下载）
    2. 从 Chroma 持久化目录加载数据
    3. 客户端关闭后自动垃圾回收
    4. 所有错误都优雅降级，不阻塞主流程
    """
    global _vectorstore, _load_error

    if _vectorstore is not None:
        return _vectorstore

    # 1. 获取 embedding 模型（支持多源下载）
    try:
        embeddings = _get_embeddings()
    except RuntimeError as exc:
        # embedding 加载失败，设置为空，在检索时处理降级逻辑
        _load_error = f"embedding 初始化失败: {exc}"
        print(f"[RAG] ⚠️ {_load_error}")
        _vectorstore = None
        return _vectorstore

    # 2. 创建 InMemoryVectorStore
    vs = InMemoryVectorStore(embeddings)

    # 3. 检查 Chroma 持久化目录
    if not _CHROMA_DIR.exists():
        _load_error = (
            f"向量库 {_CHROMA_DIR} 不存在。请先运行: python index_docs_official.py，"
            "或设置 TEST_CASE_AGENT_CHROMA_DIR 指向已有索引。"
        )
        print(f"[RAG] ⚠️ {_load_error}")
        _vectorstore = vs
        return vs

    # 4. 从 Chroma 加载数据
    try:
        import chromadb
        from langchain_chroma import Chroma

        print(f"[RAG] 📂 从 Chroma 加载数据: {_CHROMA_DIR}")
        
        client = chromadb.PersistentClient(path=str(_CHROMA_DIR))
        chroma_vs = Chroma(
            client=client, 
            collection_name="docs",
            embedding_function=embeddings,
        )
        collection = chroma_vs._collection
        count = collection.count()
        print(f"[RAG] 📊 Chroma 中有 {count} 个文本块")

        if count > 0:
            # 批量加载所有文档
            result = collection.get(include=["documents", "metadatas"])
            docs: list[Document] = []
            
            for i in range(count):
                doc_id = result["ids"][i]
                page_content = result["documents"][i] or ""
                metadata = result["metadatas"][i] or {}
                metadata["id"] = doc_id
                docs.append(Document(page_content=page_content, metadata=metadata))
            
            # 添加到内存向量库
            vs.add_documents(docs)
            print(f"[RAG] ✅ 已加载 {count} 个文本块到 InMemoryVectorStore")
        else:
            _load_error = "chroma_db 为空，请先运行 python index_docs.py"
            print(f"[RAG] ⚠️ {_load_error}")

    except ImportError as exc:
        _load_error = f"缺少依赖: {exc}"
        print(f"[RAG] ❌ 导入错误: {_load_error}")
        _vectorstore = vs
        return vs
        
    except Exception as exc:
        _load_error = f"{type(exc).__name__}: {exc}"
        print(f"[RAG] ❌ 加载 chroma_db 失败: {_load_error}")
        _vectorstore = vs
        return vs

    # 5. 安全关闭 Chroma client
    finally:
        try:
            del chroma_vs
            del client
            gc.collect()  # 强制垃圾回收
            print(f"[RAG] 🧹 Chroma client 已关闭，内存已释放")
        except Exception:
            pass  # 忽略清理时的错误

    _vectorstore = vs
    return vs


def _get_requirement(state: AgentState) -> str:
    req = state.get("requirement", "")
    if req and req.strip():
        return req.strip()

    for msg in reversed(state.get("messages", [])):
        content = ""
        if isinstance(msg, dict) and msg.get("role") == "user":
            content = msg.get("content", "")
        elif hasattr(msg, "type") and msg.type == "human":
            content = getattr(msg, "content", "")
        if content and content.strip():
            return content.strip()
    return ""


def context_retriever(state: AgentState) -> dict:
    print(f"\n{'='*60}")
    print("[RAG DIAGNOSTIC] context_retriever 开始执行")

    requirement = _get_requirement(state)
    print(f"[RAG] 提取到的 requirement: '{requirement[:80]}...' (长度: {len(requirement)})")

    docs: list = []
    rag_error: str | None = None

    try:
        store = _init_vectorstore()
        if store is None:
            # embedding 加载失败，直接进入降级模式
            rag_error = _load_error or "embedding 未初始化"
            print(f"[RAG] ⚠️ embedding 未初始化，跳过检索")
        else:
            print(f"[RAG] 正在执行 similarity_search(query='{requirement[:60]}...', k=4)")
            docs = store.similarity_search(requirement, k=4)
            if docs:
                print(f"[RAG] 检索完成，召回 {len(docs)} 条结果")
                for i, d in enumerate(docs):
                    src = d.metadata.get("source", "unknown")
                    preview = d.page_content[:60].replace('\n', ' ')
                    print(f"       [{i+1}] 来源: {src} | 内容: {preview}...")
            else:
                rag_error = _load_error or "检索结果为空"
    except Exception as exc:
        rag_error = f"{type(exc).__name__}: {exc}"
        print(f"[RAG] ❌ 意外异常: {rag_error}")
        import traceback
        traceback.print_exc()

    if docs:
        retrieved_text = "\n\n---\n\n".join([
            f"【来源: {d.metadata.get('source', 'unknown')}】\n{d.page_content}"
            for d in docs
        ])
        context = {
            "phase": "rag_enabled",
            "requirement": requirement,
            "retrieved_knowledge": retrieved_text,
            "retrieved_sources": [d.metadata.get("source") for d in docs],
            "retrieved_count": len(docs),
            "reference_roots": ["/home/zx/CICD/test_case", "/home/zx/CICD/rocm-on-radeon"],
            "case_format": "test_case/suites/<suite>/test_<name>.sh or pytest draft",
            "execution_mode": "dry_run_only",
        }
        assistant_msg = f"已从知识库检索到 {len(docs)} 篇相关文档。"
        print(f"[RAG] ✅ 进入 RAG 模式，retrieved_knowledge 长度: {len(retrieved_text)} 字符")
    else:
        context = {
            "phase": "phase_one_placeholder",
            "requirement": requirement,
            "reference_roots": ["/home/zx/CICD/test_case", "/home/zx/CICD/rocm-on-radeon"],
            "case_format": "test_case/suites/<suite>/test_<name>.sh or pytest draft",
            "execution_mode": "dry_run_only",
            "todo": "RAG 未检索到文档。",
        }
        if rag_error:
            context["rag_error"] = rag_error
        assistant_msg = f"知识库未就绪（{rag_error}），使用默认上下文。" if rag_error else "未检索到相关文档，使用默认上下文。"
        print(f"[RAG] ⚠️ 进入降级模式，原因: {rag_error or '检索结果为空'}")

    print(f"{'='*60}\n")

    return {
        "context": context,
        "messages": [{"role": "assistant", "content": assistant_msg}],
    }

# Changelog

All notable changes to the TestCaseAgent project will be documented in this file.

## [0.1.0] - 2025-05-29

### Added
- LangGraph-based agent for generating ROCm test cases
- Multi-intent routing: GENERATE, APPEND, UPDATE, REFACTOR, EXECUTE_EXTERNAL, DIAGNOSE, COVERAGE, PROBE, ENV_BUILD
- Sandbox execution with strategy pattern (Pytest, Docker Build, External Run)
- RAG context retrieval from Chroma vector store
- Memory management with LangGraph Store
- Langfuse tracing integration
- CLI interface for single-run test generation
- Multi-turn conversation support
- Docker Compose deployment with Langfuse stack
- CI/CD pipeline with GitHub Actions
- Pre-commit hooks (ruff, mypy)
- Config validation at startup
- Production-ready Checkpointer/Store (PostgreSQL support)
- API authentication via API Key

### Fixed
- Eliminated code duplication between nodes/utils.py and utils.py
- Unified message types to LangChain BaseMessage
- Moved hardcoded passwords from docker-compose.yml to environment variables
- Replaced hardcoded IP addresses with environment variable fallbacks
- Added thread-safe global state for embedding cache

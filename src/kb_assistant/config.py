"""
Acme Corp Internal Knowledge Base Assistant
Module: Configuration & Environment Management

This module implements Factor III of the 12-Factor App methodology:
"Store config in the environment".

Design Principles:
1. No Secrets in Code: API keys are NEVER hardcoded into strings or default values.
2. Sensible Local Defaults: By default, the application is pre-configured to run
   100% locally using Ollama and FastEmbed without requiring any external keys.
3. Declarative Schema: Centralizes all system environment variables in one module
   so other components import typed constants rather than calling os.getenv everywhere.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base project directory (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 1. Load environment variables from .env file (if present)
# load_dotenv() searches for a .env file in the current working directory or parents.
# If .env does not exist, it fails silently, allowing system environment variables
# (such as those injected by Docker Compose or Kubernetes) to take precedence.
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# ------------------------------------------------------------------------------
# Model Provider Settings (Defaults to 100% Local Ollama)
# ------------------------------------------------------------------------------
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2").strip()
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()

# ------------------------------------------------------------------------------
# Embedding Engine (Defaults to Local FastEmbed on CPU)
# ------------------------------------------------------------------------------
EMBEDDINGS_PROVIDER: str = os.getenv("EMBEDDINGS_PROVIDER", "local").strip().lower()

# ------------------------------------------------------------------------------
# Storage Paths (Local Vector DB, Knowledge Docs & Audit Logs)
# ------------------------------------------------------------------------------
CHROMA_DIR: str = str(PROJECT_ROOT / os.getenv("CHROMA_DIR", "chroma_db"))
DOCS_DIR: str = str(PROJECT_ROOT / os.getenv("DOCS_DIR", "data/docs"))
TICKETS_FILE: str = str(PROJECT_ROOT / os.getenv("TICKETS_FILE", "tickets.jsonl"))
LOG_FILE: str = str(PROJECT_ROOT / os.getenv("LOG_FILE", "assistant.log"))

# ------------------------------------------------------------------------------
# Optional Cloud Keys (Read purely from environment, default to empty string)
# ------------------------------------------------------------------------------
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "").strip()

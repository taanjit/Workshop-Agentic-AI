# Operations & Engineering Handover: Acme KB Assistant

> **Service Name:** `acme-kb-assistant`  
> **Repository:** `https://github.com/taanjit/Workshop-Agentic-AI.git`  
> **Version:** `1.0.0`  
> **Maintainer:** AI Engineering / DevOps Team

---

## 1. System Overview

The **Acme KB Assistant** is a containerized, grounded AI agent designed to resolve employee HR and IT questions. It operates using:
- **Local Embedding Generation:** FastEmbed running quantized `bge-small-en-v1.5` on CPU.
- **Local Vector Database:** Chroma running in persistent mode (`/app/chroma_db`).
- **Local LLM Engine:** Ollama running `llama3.2` on the host machine.
- **Multi-Stage Guardrails:** Prompt injection detection, PII redaction (email/phone), and output grounding verification.
- **Human-in-the-Loop (HITL):** Support ticket creation requires interactive confirmation.

---

## 2. Quickstart Runbook

### Running via Docker Compose (Recommended for Production)
```bash
# 1. Ensure Ollama is running on the host machine
ollama serve

# 2. Build the container image
docker compose build

# 3. Launch the interactive assistant
docker compose run --rm assistant
```

### Running Locally (Development Mode)
```bash
# 1. Activate Python virtual environment
source .venv/bin/activate

# 2. Rebuild the vector index from data/docs
PYTHONPATH=src python3 -m kb_assistant.ingest

# 3. Launch the application CLI
PYTHONPATH=src python3 -m kb_assistant.main
```

---

## 3. Knowledge Base Maintenance Protocol

To update existing company policies or add new ones:
1. Place standard Markdown files (`.md`) inside the `data/docs/` directory.
2. Re-index the vector database:
   ```bash
   # Delete stale index and regenerate embeddings
   rm -rf chroma_db/
   PYTHONPATH=src python3 -m kb_assistant.ingest
   ```
3. Run the automated golden test suite to ensure no policy regressions:
   ```bash
   pytest -m "not slow"
   pytest -m slow
   ```

---

## 4. Configuration Schema Reference (`.env`)

| Variable | Default Value | Description |
|---|---|---|
| `LLM_PROVIDER` | `ollama` | Model provider: `ollama`, `openai`, or `anthropic` |
| `LLM_MODEL` | `llama3.2` | Model parameter checkpoint identifier |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Endpoint for Ollama daemon |
| `EMBEDDINGS_PROVIDER` | `local` | Embedding engine: `local` (FastEmbed), `ollama`, `openai` |
| `CHROMA_DIR` | `chroma_db` | Persistent directory path for Chroma vectors |
| `DOCS_DIR` | `data/docs` | Source folder containing policy markdown files |
| `TICKETS_FILE` | `tickets.jsonl` | Append-only audit file for generated support tickets |
| `LOG_FILE` | `assistant.log` | Persistent operational audit trail log |

---

## 5. Security & Incident Response

- **Secret Leaks:** Never commit `.env`. All Docker images are built without credentials inside layers.
- **Audit Logs:** All user interactions, router classifications, and blocked security events are recorded in `assistant.log`.
- **Primary Support Contact:** AI Engineering Team (Dr. Anjit T A).

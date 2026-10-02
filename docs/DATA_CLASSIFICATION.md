# Data Classification Framework for LLM Architectures

> **Standard:** ISO/IEC 27001 & NIST AI Risk Management Framework  
> **Applicability:** All pipelines, vector databases, prompts, and logs

---

## 1. The 4-Tier Data Classification Matrix

Before feeding any text into a language model or vector database, data must be classified according to its sensitivity.

```
┌────────────────────────────────────────────────────────┐
│  TIER 4: RESTRICTED                                    │  Passwords, API Keys, Passports, Bank Accounts
│  ⛔ NEVER pass to any LLM or Vector Store.             │  Redact immediately at ingestion / input layer.
├────────────────────────────────────────────────────────┤
│  TIER 3: CONFIDENTIAL                                  │  Internal Policies, Employee Directory, IT Guides
│  🔒 Local On-Prem LLM (Ollama) ONLY.                   │  Must never leave internal network boundary.
├────────────────────────────────────────────────────────┤
│  TIER 2: INTERNAL                                      │  Cafeteria Menus, Holiday Calendars, General FAQs
│  🏢 Controlled internal distribution.                  │  Low risk if exposed internally.
├────────────────────────────────────────────────────────┤
│  TIER 1: PUBLIC                                        │  Marketing Blogs, Public Press Releases
│  🌐 Safe for any LLM (Cloud or Local).                 │  No confidentiality requirements.
└────────────────────────────────────────────────────────┘
```

---

## 2. Handling Rules for AI Systems

| Data Tier | Storage Requirements | Permitted Model Targets | DLP / Redaction Rule |
|---|---|---|---|
| **Tier 1: Public** | Standard databases, public Git | OpenAI, Anthropic, Ollama | None required |
| **Tier 2: Internal** | Authenticated intranet storage | Private Cloud LLMs (with zero data retention) or Local Ollama | Log user access |
| **Tier 3: Confidential** | Encrypted local Chroma vector database (`chroma_db/`) | **Strictly Local Models (Ollama)** | Require user authentication and role-based access control |
| **Tier 4: Restricted** | Secrets vault (HashiCorp Vault, AWS Secrets Manager) | **FORBIDDEN** from all models | Automated regex redaction (`[EMAIL_REDACTED]`, `[PHONE_REDACTED]`) |

---

## 3. Engineering Safeguards Implemented in this Project

1. **At the Input Layer (`src/kb_assistant/guardrails.py`):**
   - Every user query is passed through `redact_pii()` before the agent loop receives it.
   - Any phone numbers or email addresses are masked into synthetic tokens.
2. **At the Ingestion Layer (`src/kb_assistant/ingest.py`):**
   - Vector database storage is constrained to local disk (`chroma_db/`).
   - `chroma_db/` is permanently blacklisted in `.gitignore` to prevent company policy embeddings from entering GitHub.

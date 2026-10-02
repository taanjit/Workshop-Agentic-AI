# Step 03: Protecting Confidential Data & Secrets Hygiene

> **Branch:** `step-03-secure-confidential-data`  
> **Session:** 03 — How to Save Confidential Data  
> **Duration:** 40 Minutes (15 min lecture / 25 min hands-on lab)

---

## 1. Purpose

The objective of Step 03 is to implement the industry-standard **Separation of Configuration and Code**. 

In this step, we implement:
1. An environment template (`.env.example`) defining the configuration contract.
2. A hardened `.gitignore` preventing secrets, vector embeddings, and temporary logs from ever entering Git.
3. A centralized, defensive configuration module (`src/kb_assistant/config.py`) following the **12-Factor App** design pattern.

---

## 2. Why It Is Used in Industry

### The Disaster of Hardcoded API Keys
In software engineering, the #1 source of security incidents is committed credentials:
```python
# ❌ CATASTROPHIC ANTI-PATTERN: NEVER DO THIS!
client = OpenAI(api_key="sk-proj-9384729384729384729384729384")
```
- **Automated Scraping Bots:** Public GitHub commits are indexed by automated scraping bots within **3 seconds** of a push. Attackers immediately spin up hundreds of high-end GPU instances or exfiltrate private models under your credit card.
- **The Git History Trap:** Simply deleting the line in your next commit does **NOT** erase the key. Git is an immutable append-only ledger; anyone running `git log -p` or cloning an earlier commit will retrieve your secret.

### The 12-Factor App Solution
In enterprise architecture, code is **stateless and generic**. All secrets, hostnames, model names, and file paths are injected from the **environment** at runtime:
```python
# ✅ PRODUCTION PATTERN: Read from environment
api_key = os.getenv("OPENAI_API_KEY")
```

---

## 3. Line-by-Line Breakdown

### A. Deep Dive: `.env.example` vs `.env`

- **`.env.example` (Committed to Git):**
  - Serves as the blueprint for teammates and automated deployment pipelines.
  - Contains all variable names and sensible defaults, but **zero real secrets**.
- **`.env` (NEVER Committed):**
  - Your local, personal instance containing real keys, passwords, or overrides.
  - Blacklisted permanently in `.gitignore`.

---

### B. Deep Dive: `.gitignore`

```gitignore
# Secrets and Environment Variables (CRITICAL)
.env
.env.local
*.pem
*.key
```
- **Why it matters:** Ensures Git refuses to track your `.env` file even if you run `git add .`.

```gitignore
# Vector Database
chroma_db/
```
- **Why it matters:** Chroma stores vector embeddings on local disk. These files contain mathematical representations of your company's private documents. They are binary assets, large in size, and confidential—they belong on local disk or cloud volume mounts, **never in source control**.

```gitignore
# Runtime Logs and Tickets
tickets.jsonl
assistant.log
```
- **Why it matters:** `tickets.jsonl` contains support tickets submitted by employees (which may contain real user names or problem descriptions). Logging it to Git violates data minimization principles.

---

### C. Deep Dive: `src/kb_assistant/config.py`

```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
```
- **Line 16:** Computes the absolute path to the repository root dynamically.
- **Why this is critical:** If an engineer executes a script from `src/kb_assistant/` vs the repo root vs a Docker container, relative paths (`data/docs`) will fail. Resolving paths relative to `PROJECT_ROOT` guarantees that file lookups succeed regardless of current working directory ($CWD$).

```python
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
```
- **Line 22:** Reads key-value pairs from `.env` and injects them into Python's `os.environ`.
- If `.env` is absent (such as in a Docker container or Kubernetes pod where environment variables are injected natively), `load_dotenv` fails gracefully without raising an exception.

```python
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama").strip().lower()
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2").strip()
```
- **Line 27–28:** Defaults to `ollama` and `llama3.2`.
- Notice the defensive programming: `.strip().lower()` prevents invisible whitespace or casing bugs (e.g., `"Ollama "` becoming an unrecognized provider).

---

## 4. What To Do Next (Hands-on Lab)

Execute the following verification exercises in your terminal:

```bash
# 1. Copy the example configuration to your active local .env
cp .env.example .env

# 2. Verify that Git is actively ignoring .env (Crucial verification!)
git check-ignore -v .env
# Expected output: .gitignore:5:.env    .env

# 3. Test that the configuration loader resolves correctly
PYTHONPATH=src python3 -c "from kb_assistant import config; print(f'LLM Provider: {config.LLM_PROVIDER}'); print(f'Model: {config.LLM_MODEL}'); print(f'Docs Path: {config.DOCS_DIR}')"
```

Once verified, proceed to **Step 04** to establish automated pre-commit scanning hooks that block accidental leaks:
```bash
git checkout step-04-git-industrial-workflow
```

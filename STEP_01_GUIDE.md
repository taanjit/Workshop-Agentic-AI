# Step 01: Project Scaffolding & Industrial Charter

> **Branch:** `step-01-project-scaffold`  
> **Session:** 01 — How to Start a New Project  
> **Duration:** 35 Minutes (15 min lecture / 20 min lab)

---

## 1. Purpose

The objective of Step 01 is to establish a **production-grade foundation** for our AI Assistant before writing a single line of application code. In industry, professional software engineers do not jump straight into a code editor; they establish:
1. An isolated execution runtime (virtual environment).
2. A clean, modular directory structure adhering to package standards.
3. A pinned dependency manifest (`requirements.txt`).
4. An executive **Project Brief** (`docs/PROJECT_BRIEF.md`) defining technical scope, non-goals, and measurable SLAs.

---

## 2. Why It Is Used in Industry

### Why Not Just Write a Single Script in the Root Directory?
In amateur tutorials, developers often create a file called `agent.py` in their home directory, install packages globally with `pip install ...`, and hardcode secrets. In an enterprise:
- **Dependency Isolation:** Global package installations cause "dependency drift." Package updates on your laptop can break other projects or production servers. A local `.venv` guarantees isolation.
- **Topology & Conway's Law:** Separating `src/` (core application), `data/` (enterprise assets), `docs/` (architectural records), and `tests/` (verification) ensures the codebase can scale to hundreds of engineers without conflicts.
- **The Power of Non-Goals:** 80% of enterprise AI projects fail not because the model couldn't answer questions, but because stakeholders expected it to do things it was never designed for (e.g., provide legal advice or access confidential salaries). A formal **Project Brief** sets legal boundaries and prevents scope creep.

---

## 3. Line-by-Line Breakdown

### A. Deep Dive: `requirements.txt`

```text
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0
langchain-text-splitters>=0.3.0
```
- **Line 1–4 (`langchain` packages):**
  - **Purpose:** LangChain is the industry-standard orchestration library for LLMs.
  - **Why it is split:** Prior to LangChain v0.2/v0.3, LangChain was a massive, monolithic package that installed hundreds of unnecessary dependencies. The modern architecture splits it into `langchain-core` (lightweight interface for prompts, messages, and tools), `langchain-community` (third-party integrations), and `langchain-text-splitters` (document chunking).

```text
langchain-chroma>=0.1.4
chromadb>=0.5.0
fastembed>=0.3.4
```
- **Line 5–7 (Vector Database & Embeddings):**
  - **`chromadb`:** An open-source, embedded vector database. Unlike cloud vector stores (Pinecone, Weaviate) that charge monthly hosting fees and require external network access, Chroma runs directly inside our Python process or Docker container, writing files to local disk.
  - **`fastembed`:** A lightweight, blazing-fast embedding generator built by Qdrant. It runs quantized ONNX models directly on your CPU without requiring PyTorch, CUDA drivers, or expensive GPU hardware.

```text
langchain-ollama>=0.2.0
```
- **Line 8 (`langchain-ollama`):**
  - **Purpose:** The dedicated provider adapter that allows LangChain to communicate with a locally running Ollama engine via its HTTP API (`http://localhost:11434`).
  - **Why it is used:** Eliminates dependency on external proprietary APIs (OpenAI, Anthropic). It ensures 100% privacy and zero API invoices.

```text
python-dotenv>=1.0.1
```
- **Line 9 (`python-dotenv`):**
  - **Purpose:** Parses key-value pairs from a `.env` file and injects them into `os.environ`.
  - **Why it is used:** Implements Factor III of the *12-Factor App Methodology* ("Store config in the environment").

```text
pytest>=8.0.0
pre-commit>=3.7.0
detect-secrets>=1.5.0
```
- **Line 10–12 (Quality & Security):**
  - **`pytest`:** The standard testing framework for executing automated unit and golden-dataset evaluations.
  - **`pre-commit` & `detect-secrets`:** Security hooks that intercept `git commit` actions to prevent API keys and passwords from ever reaching GitHub.

---

### B. Deep Dive: `docs/PROJECT_BRIEF.md`

- **Section 1 (Executive Summary):** Translates engineering intent into business value (saving employee time answering HR/IT queries).
- **Section 2 (Non-Goals):**
  ```markdown
  ## Non-Goals (Strict Out-of-Scope)
  - No Legal or Medical Counseling
  - No Autonomous Write Access
  - No Speculative Answering ("I don't know" rule)
  ```
  In an audit, this section proves that the engineering team explicitly designed safety boundaries into the software architecture.
- **Section 3 (SLAs & Metrics):**
  Enterprise contracts demand measurable Service Level Agreements:
  - $\ge 90\%$ accuracy on golden test set.
  - $0$ leaked credentials.
  - $< 2$ minutes cold start deployment time.

---

## 4. What To Do Next (Hands-on Lab)

Execute the following commands in your terminal to initialize your local environment:

```bash
# 1. Create a dedicated Python virtual environment
python3 -m venv .venv

# 2. Activate the virtual environment
# On macOS / Linux:
source .venv/bin/activate
# On Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# 3. Upgrade pip and install the pinned dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify your active environment
python -c "import langchain, chromadb, fastembed; print('Environment initialized successfully!')"
```

Once your dependencies finish installing, proceed to **Step 02** to model token economics and establish the project risk register:
```bash
git checkout step-02-considerations-and-risks
```

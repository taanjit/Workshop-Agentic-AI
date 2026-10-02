# Industrial Agentic AI Workshop: Hands-on Lab

> **Institution:** TKM College of Engineering, Kollam  
> **Course:** Applying LLMs to Industrial Projects — Production-Grade AI Agents  
> **Facilitator:** Dr. Anjit T A  
> **Target Audience:** Postgraduate Students & Software Engineers  
> **Target LLM Stack:** 100% Local (Ollama + FastEmbed) — Zero API Cost, 100% Private

---

## 🚀 Workshop Overview

Welcome to the hands-on repository for the **Industrial Agentic AI Workshop** at TKM College of Engineering. 

In this workshop, you will step beyond academic notebook experiments and learn how software teams architect, secure, test, and containerize **production-grade AI agents**. Throughout the day, you will build **"Acme Corp Internal Knowledge Base Assistant"**—an intelligent agent that answers HR/IT questions using official company documents, executes tools, demands human authorization before performing risky actions, protects itself against prompt injection and PII leaks, and packages cleanly inside a secure Docker container.

---

## 🗺️ Step-by-Step Hands-on Navigator

The workshop is structured as a **progressive series of Git branches**. Each branch represents a milestone checkpoint containing working code, configurations, and a comprehensive **`STEP_XX_GUIDE.md`** explaining every file and line-by-line concept.

| Step | Branch Name | Core Theme & Topics | Step Guide Link |
|:---:|---|---|:---:|
| **00** | [`main`](https://github.com/taanjit/Workshop-Agentic-AI) | **Why Industry ≠ Research:** Reliability, cost budgeting, security, and governance principles. | [`SESSION_00_GUIDE`](docs/SESSION_00_INDUSTRY_VS_RESEARCH.md) |
| **01** | `step-01-project-scaffold` | **Project Scaffolding:** Industrial scoping, `PROJECT_BRIEF.md`, virtual environments, and dependency pinning. | `STEP_01_GUIDE.md` |
| **02** | `step-02-considerations-and-risks` | **Governance & Risk:** Data sensitivity classification (Public to Restricted), token economics, and `RISK_REGISTER.md`. | `STEP_02_GUIDE.md` |
| **03** | `step-03-secure-confidential-data` | **Secrets & Hygiene:** `.env` lifecycle, `.gitignore`, 12-factor config loaders, and credential leakage prevention. | `STEP_03_GUIDE.md` |
| **04** | `step-04-git-industrial-workflow` | **Industrial Git Workflow:** Pre-commit hooks, automated Gitleaks secret interception, and live red-team testing. | `STEP_04_GUIDE.md` |
| **05** | `step-05-agent-tools-and-skills` | **Agentic Tools & HITL:** Ollama model connectivity, function calling schemas, tool binding, and human-in-the-loop approvals. | `STEP_05_GUIDE.md` |
| **06** | `step-06-rag-guardrails-and-evals` | **RAG & Automated Evals:** Ingestion, Chroma vector database, prompt injection guardrails, PII masking, and pytest golden set. | `STEP_06_GUIDE.md` |
| **07** | `step-07-docker-deployment` | **Production Containerization:** Non-root Dockerfile, docker-compose orchestration with local Ollama, and secret leakage audits. | `STEP_07_GUIDE.md` |

---

## 🛠️ Pre-flight Setup (Do This Before the Workshop!)

Before attending the hands-on session, ensure your laptop has the required software installed. Run the pre-flight verification script:

```bash
# 1. Clone the repository
git clone https://github.com/taanjit/Workshop-Agentic-AI.git
cd Workshop-Agentic-AI

# 2. Run the automated pre-flight environment check
python3 check_setup.py
```

### Required Software
- **Python 3.10+** (`python3 --version`)
- **Git** (`git --version`)
- **Docker & Docker Desktop** (`docker --version` and `docker compose version`)
- **Ollama** ([Download from ollama.com](https://ollama.com/))
  ```bash
  # Pull the lightweight model for offline local inference
  ollama pull llama3.2
  ```

---

## 🧭 How to Use This Repository During the Lab

### 1. Following Along Live
As the instructor introduces each session, switch to the corresponding branch:
```bash
git checkout step-01-project-scaffold
```
Every branch contains a `STEP_XX_GUIDE.md` with:
- **Purpose**: Why this step matters.
- **Why It Is Used**: Real-world industrial relevance.
- **Line-by-Line Breakdown**: Deep explanation of code, parameters, and design decisions.
- **What To Do Next**: Hands-on exercises and checkpoint tests.

### 2. Emergency Recovery (If You Get Stuck)
If your code breaks during live typing, do not panic! You can immediately restore your workspace to the official checkpoint:
```bash
# Discard local changes and jump cleanly to the step checkpoint
git stash
git checkout step-0X-branch-name
```

---

## 🏗️ Final System Architecture

```
                          ┌──────────────────────────────┐
    User question ───────►│  1. INPUT GUARDRAILS         │  Blocks prompt injection
                          │     (guardrails.py)          │  Redacts email / phone (PII)
                          └──────────────┬───────────────┘
                                         ▼
                          ┌──────────────────────────────┐
                          │  2. AGENT CORE               │  Local Ollama LLM
                          │     (agent.py & router.py)   │  Tool-calling reasoning loop
                          └──────┬───────────┬───────────┘
                                 │           │
               ┌─────────────────┘           └─────────────────┐
               ▼                                               ▼
    ┌─────────────────────┐                        ┌─────────────────────────┐
    │ search_kb (RAG)     │                        │ create_ticket           │
    │ Chroma Vector Store │                        │ ⚠️ HUMAN APPROVAL NEEDED│
    └─────────────────────┘                        └─────────────────────────┘
               │
               ▼
    ┌─────────────────────┐
    │ data/docs/*.md      │   (Company Policies)
    └─────────────────────┘
                                         ▼
                          ┌──────────────────────────────┐
                          │  3. OUTPUT GROUNDING CHECK   │  Must cite source document;
                          │     + Audit Trail Logging    │  otherwise says "I don't know"
                          └──────────────┬───────────────┘
                                         ▼
                                   Final Answer
```

---

## 👨‍🏫 Facilitator Notes & Materials

For the instructor's schedule, minute-by-minute lecture talking points, interactive quiz questions, and live demonstration scripts, refer to:
👉 **[`INSTRUCTOR_RUNBOOK.md`](INSTRUCTOR_RUNBOOK.md)**

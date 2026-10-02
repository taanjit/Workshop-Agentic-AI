# Instructor Runbook: Industrial Agentic AI Workshop

> **Facilitator:** Dr. Anjit T A  
> **Institution:** TKM College of Engineering  
> **Course:** Applying LLMs to Industrial Projects (Agentic AI)  
> **Audience:** Postgraduate Students (M.Tech / MCA / Research Scholars)  
> **Delivery Format:** 5 Hours (40% Concepts / 60% Hands-on Coding Lab)

---

## 1. Master Workshop Schedule (Pacing Guide)

| Time | Duration | Session / Module | Format | Key Deliverable |
|---|---|---|---|---|
| **09:00 – 09:15** | 15 min | **Welcome & Orientation** | Lecture | Problem framing ("Acme Corp") |
| **09:15 – 09:45** | 30 min | **Session 00: Industry ≠ Research** | Discussion | Mindset shift, 5 enterprise pillars |
| **09:45 – 10:20** | 35 min | **Session 01: Project Scaffolding** | Hands-on (`step-01`) | Virtualenv, structure, project brief |
| **10:20 – 10:50** | 30 min | **Session 02: Considerations & Risks** | Discussion (`step-02`) | Data classification, cost calculations |
| **10:50 – 11:05** | **15 min** | ☕ **Morning Tea Break** | — | Environment triage for any stuck students |
| **11:05 – 11:45** | 40 min | **Session 03: Confidential Data & Secrets** | Hands-on (`step-03`) | `.env` pattern, config loader |
| **11:45 – 12:30** | 45 min | **Session 04: Industrial Git Workflow** | Hands-on (`step-04`) | Pre-commit hooks, live secret leak test |
| **12:30 – 13:30** | **60 min** | 🍽 **Lunch Break** | — | — |
| **13:30 – 14:15** | 45 min | **Session 05: Agent Skills & Tools** | Hands-on (`step-05`) | Function calling, human-in-the-loop |
| **14:15 – 15:15** | 60 min | **Session 06: RAG Assistant & Evals** | Hands-on (`step-06`) | Chroma RAG, guardrails, pytest evals |
| **15:15 – 15:30** | **15 min** | ☕ **Afternoon Break** | — | — |
| **15:30 – 16:15** | 45 min | **Session 07: Docker Containerization** | Hands-on (`step-07`) | Dockerfile, docker-compose, audit |
| **16:15 – 16:30** | 15 min | **Wrap-up, Assessment & Q&A** | Interactive | Student demos, certificate rubric |

---

## 2. Minute-by-Minute Lecture Scripts & Teaching Prompts

### Opening Hook (09:00 – 09:15)
- **What to say:**
  > *"Welcome everyone. Today is not about writing prompts into ChatGPT. Anyone can do that. Today is about what happens when your engineering manager asks you to build an AI system that a bank or a hospital can trust with real employee and company data. By 4:30 PM today, every single one of you will have built a containerized, secured, and evaluated AI Agent on your own laptops that uses local models, calls tools, respects guardrails, and requires human approval for risky actions."*
- **The Scenario:** Introduce Acme Corp (HR & IT helpdesk assistant).

---

### Session 00: Why Industry ≠ Research (09:15 – 09:45)
- **Visual Aid:** Open `docs/SESSION_00_INDUSTRY_VS_RESEARCH.md`.
- **Key Analogy:** 
  > *"Academic research is like building a Formula 1 race car. You only care about breaking the lap time record on a dry track. Production engineering is like building a commercial airline. You need it to fly safely through thunderstorms, carry passengers reliably 500 times a year, stay within fuel budgets, and never crash."*
- **Audience Interactive Question 1:** 
  > *"Raise your hand: how many of you have ever committed an API key or password to GitHub by accident?"* (Usually 50%+ raise hands. Use this to introduce why Module 4's pre-commit hook is a life-saver.)
- **Audience Interactive Question 2:**
  > *"If an AI assistant answers 95 out of 100 questions correctly, but tells one employee that they are entitled to 6 months of paid vacation when the real policy is 3 weeks, what happens to the company?"*
  - **Expected Answer:** Legal dispute, payroll chaos, loss of trust.

---

### Session 01: Project Scaffolding (`step-01-project-scaffold`)
- **Key Principle:** *"Before code, we write the charter."*
- **Teaching Point:** Walk through `docs/PROJECT_BRIEF.md`. Emphasize that defining **Non-Goals (Out of Scope)** is more important than defining goals. An AI that doesn't know its boundaries is dangerous.
- **Checkpoint Check:** Walk the room and make sure all students have their `.venv` activated in terminal.

---

### Session 02: Considerations & Risks (`step-02-considerations-and-risks`)
- **Interactive Exercise (The Token Trap):**
  Write this calculation on the whiteboard:
  $$\text{1,000 employees} \times \text{5 queries/day} \times \text{2,000 tokens/query} \times \text{30 days} = 300\text{M tokens/month}$$
  If using GPT-4o at \$5/million tokens:
  $$\text{Cost} = 300 \times \$5 = \$1,500\text{/month}$$
  Then show:
  > *"With local Ollama and FastEmbed running on on-premise hardware, your token cost is \$0. This is why local agentic AI is exploding in enterprise IT."*

---

### Session 03: Confidential Data & Secrets (`step-03-secure-confidential-data`)
- **Key Rule:** Never commit secrets. Walk through the `.env` vs `.env.example` distinction.
- **Teaching Point:** Show `git check-ignore .env`. When Git outputs `.env`, explain: *"This command proves Git is actively ignoring your secret file."*

---

### Session 04: Industrial Git Workflow (`step-04-git-industrial-workflow`)
- **🔴 The Live "Red-Team" Demo (High Engagement!):**
  Have students create a temporary test branch:
  ```bash
  git checkout -b leak-test
  echo 'OPENAI_API_KEY = "sk-proj-DEMOFAKEKEY1234567890abcdefghijklmnop"' > leak.py
  git add leak.py
  git commit -m "oops: committed a key"
  ```
  Watch the terminal output **BLOCK** the commit with a bright red Gitleaks violation message!
  Explain to the class:
  > *"Notice what just happened. Your computer refused to commit. The secret never touched git history. This single configuration saves developers their jobs every day."*

---

### Session 05: Agent Skills & Tools (`step-05-agent-tools-and-skills`)
- **💡 The "Aha!" Function Calling Moment:**
  Run `python3 try_tool.py`.
  Point to the output:
  `[{'name': 'calculate_leave', 'args': {'years_of_service': 3.0}, 'id': '...'}]`
  Ask the class:
  > *"Did the LLM execute our Python function? Look closely. No! The LLM generated a JSON request asking US to run the function. We are the operating system. We inspect the request, and we decide whether to execute it."*
- **Human-in-the-Loop (HITL):**
  Show why `create_ticket` pauses and prompts `[y/N]`. Explain irreversible side effects.

---

### Session 06: Knowledge Base, RAG & Evals (`step-06-rag-guardrails-and-evals`)
- **RAG Demonstration:**
  Ask: *"What is the parental leave policy?"*
  The agent returns: *"I don't know based on the available documents."*
  Highlight this:
  > *"In research, saying 'I don't know' gets you a zero score on an exam. In production AI, admitting you don't know is the gold standard of safety!"*
- **Evaluation:** Run `pytest -m "not slow"` and `pytest -m slow`. Explain golden test sets as the CI/CD pipeline for AI.

---

### Session 07: Docker Deployment (`step-07-docker-deployment`)
- **Container Security Demo:**
  Run:
  ```bash
  docker compose run --rm assistant
  ```
  Then inspect the container filesystem to prove no `.env` exists inside the image.

---

## 3. Emergency Troubleshooting Cheat Sheet (For the Instructor)

| Issue in Classroom | Root Cause | Instant Recovery Command |
|---|---|---|
| Student gets completely stuck / broken code | Syntax errors / missing files | `git stash && git checkout -f step-0X-name` |
| `ModuleNotFoundError: kb_assistant` | Python cannot find `src` | `export PYTHONPATH=src` (Mac/Linux) or `$env:PYTHONPATH="src"` (Windows) |
| Ollama connection refused | Background service not running | Run `ollama serve` in a dedicated terminal |
| Model inference is sluggish | Laptop has 8GB RAM or no GPU | Switch to lightweight model: `ollama pull llama3.2:3b` or `ollama pull qwen2.5:3b` |
| Docker Desktop won't start on student machine | Virtualization disabled in BIOS | Don't stall the class! Pair them up with a neighbor for Session 07, or let them complete the CLI parts locally. |
| Student committed their `.env` by accident | Ignored instructions | `git rm --cached .env && git commit -m "fix: untrack .env"` |

---

## 4. Pacing Management: What to Trim if Running Late

If by 14:00 (Session 06) the class is behind schedule:
1. **Trim:** Do not have every student manually type out all three policy markdown files. Have them pull from the branch or copy-paste directly.
2. **Trim:** Make the Docker session (Session 07) a live instructor demonstration with students following along on pre-built images rather than compiling from scratch.
3. **Never Trim:** Do not skip the **Function Calling demo (Session 05)** or the **Human-in-the-Loop approval loop**. That is the core "Agentic" learning outcome!

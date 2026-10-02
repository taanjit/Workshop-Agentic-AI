# Step 04: Industrial Git Workflow & Automated Secret Interception

> **Branch:** `step-04-git-industrial-workflow`  
> **Session:** 04 — How to Configure Git (Industrial Workflow)  
> **Duration:** 45 Minutes (20 min lecture / 25 min hands-on lab)

---

## 1. Purpose

The objective of Step 04 is to transform version control from a passive backup tool into an **active security and quality firewall**. 

In this step, we implement:
1. A **Pre-commit Hook Configuration** (`.pre-commit-config.yaml`) integrating **Gitleaks** and **Yelp detect-secrets**.
2. A **Baseline Fingerprint** (`.secrets.baseline`) preventing false positives on existing code.
3. An **Interactive Red-Team Simulator** (`scripts/simulate_leak.py`) allowing you to safely trigger and observe pre-commit blocking an attempted leak.
4. An **Industrial Branching & Commit Specification** (`docs/GIT_WORKFLOW_GUIDE.md`).

---

## 2. Why It Is Used in Industry

### Human Discipline vs. Automated Enforcement
Every company that has ever suffered a public data breach had a security policy that said: *"Developers must never commit API keys."*
Policy documents do not prevent breaches. **Automated code barriers do.**

A **Git Hook** is a script located inside `.git/hooks/` that triggers automatically at specific lifecycle events (such as `pre-commit`, `commit-msg`, or `pre-push`). By binding security scanners to the `pre-commit` event:
- The scan runs **on your local CPU** before the commit object is written to Git.
- If a secret is detected, the hook exits with code 1, and the commit is **aborted**.
- The secret never enters Git history, never touches your local commit log, and never reaches GitHub.

---

## 3. Line-by-Line Breakdown

### A. Deep Dive: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
```
- **Line 8–12 (Gitleaks):**
  - **What it does:** Gitleaks maintains a database of regular expressions matching secret token structures used by over 160 vendors (e.g., OpenAI `sk-[a-zA-Z0-9]{48}`, AWS `AKIA[0-9A-Z]{16}`, Slack tokens, RSA private keys).
  - **`rev: v8.18.4`:** Explicitly pins the tool version so builds remain reproducible across team machines.

```yaml
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
```
- **Line 14–19 (detect-secrets):**
  - **What it does:** Calculates the **Shannon Entropy** of strings. Secrets (like hashed passwords or API tokens) have extraordinarily high randomness compared to standard English words or camelCase code identifiers.
  - **`--baseline .secrets.baseline`:** Tells the scanner to ignore strings that have already been vetted, alerting developers only to newly introduced strings.

---

### B. Deep Dive: Conventional Commits (`docs/GIT_WORKFLOW_GUIDE.md`)

```
feat(agent): implement human-in-the-loop approval prompt
fix(guardrail): escape special regex characters in email filter
docs(readme): add step navigation table for students
```
- **`feat` / `fix` / `docs`:** Enables CI/CD pipelines to automatically determine whether a new release is a Major, Minor, or Patch version under Semantic Versioning ($SemVer$).
- **Imperative Mood:** *"implement"* rather than *"implemented"* or *"implements"*.

---

## 4. What To Do Next (Hands-on Lab & Red-Team Demo)

### Exercise 1: Install Pre-Commit Hooks
Run these commands in your virtual environment:

```bash
# 1. Install the pre-commit Git hooks into your local .git/hooks directory
pre-commit install

# 2. Run a full scan across all files in the repository
pre-commit run --all-files
# Expected: All hooks pass with green checkmarks!
```

### Exercise 2: 🔴 The Live Red-Team Leak Challenge
Simulate an accidental credential leak and watch pre-commit block it:

```bash
# 1. Generate a test file containing a simulated API key
python3 scripts/simulate_leak.py generate

# 2. Stage the file
git add test_leak.py

# 3. Attempt to commit the secret
git commit -m "chore: test committing a key"

# 4. OBSERVE: Gitleaks triggers and ABORTS the commit with a violation message!

# 5. Clean up the simulated leak
git reset HEAD test_leak.py
python3 scripts/simulate_leak.py cleanup
```

Once you have verified the pre-commit protection, proceed to **Step 05** to build the agent's tool-calling engine and Human-in-the-Loop authorization gate:
```bash
git checkout step-05-agent-tools-and-skills
```

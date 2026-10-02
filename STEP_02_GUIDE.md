# Step 02: Architectural Considerations, Data Governance & Risk Modeling

> **Branch:** `step-02-considerations-and-risks`  
> **Session:** 02 — Things to Consider Before Creating a Project  
> **Duration:** 30 Minutes (15 min presentation / 15 min interactive discussion)

---

## 1. Purpose

The objective of Step 02 is to perform the **pre-flight risk assessment and economic modeling** that enterprise software architects conduct before committing development resources. 

In this step, we establish:
1. A **Risk Register** (`docs/RISK_REGISTER.md`) mapping enterprise failure modes to technical mitigations.
2. A **Data Classification Framework** (`docs/DATA_CLASSIFICATION.md`) defining where sensitive data can and cannot travel.
3. A **Token Economics Model** (`docs/TOKEN_BUDGET_CALCULATOR.md`) sizing hardware and proving why local inference eliminates financial risk.

---

## 2. Why It Is Used in Industry

### The "Proof of Concept (POC) to Production" Graveyard
Over 80% of enterprise AI proofs-of-concept are never deployed to real users. Why?
- **The Financial Shock:** An engineer builds a prototype using a cloud API. It works beautifully for 10 test users. But when rolled out to 5,000 employees, the first monthly bill is \$12,000. Finance immediately kills the project.
- **The Legal & Compliance Blockade:** The security team discovers employee names, personal emails, or confidential roadmaps were transmitted to third-party servers without encryption or data processing agreements (violating GDPR or India's DPDP Act).
- **The Liability of Hallucination:** A model tells an employee that bereavement leave is 30 days instead of 3 days. The company is forced to honor the mistake or face legal backlash.

By formalizing risk registers, classification tiers, and token budgets upfront, an AI engineer designs safety directly into the architecture.

---

## 3. Line-by-Line Breakdown

### A. Deep Dive: `docs/RISK_REGISTER.md`

Let's examine how each identified risk maps to an architectural safeguard:

| Risk Item | Failure Mode | Architectural Mitigation in this Codebase |
|---|---|---|
| **RSK-01 (Secret Leak)** | API key pushed to GitHub | `.pre-commit-config.yaml` intercepts commits before they touch Git (`step-04`). |
| **RSK-02 (Hallucination)** | Assistant invents fake policy | RAG grounding check: if no source is cited, output is forced to *"I don't know based on the available documents"* (`step-06`). |
| **RSK-03 (PII Exfiltration)** | Employee email/phone sent to LLM | Regex redactor replaces raw values with synthetic tokens before LLM sees the text (`step-06`). |
| **RSK-04 (Token Runaway)** | Recursive agent loop burns compute | Hardcoded loop circuit-breaker: `MAX_STEPS = 5` (`step-05`). |
| **RSK-05 (Unauthorized Action)** | Agent files fake tickets automatically | Human-in-the-Loop (HITL) authorization prompt halts execution until human types `y` (`step-05`). |

---

### B. Deep Dive: `docs/DATA_CLASSIFICATION.md`

Enterprise data is classified into 4 distinct tiers:
- **Tier 1 (Public):** Marketing blogs, public news. Safe for any cloud LLM.
- **Tier 2 (Internal):** Cafeteria menus, company holiday calendar. Low risk.
- **Tier 3 (Confidential):** Company leave policies, internal IT docs. In our system, these stay **strictly on-premise** inside our local Chroma vector database (`chroma_db/`) and local Ollama model.
- **Tier 4 (Restricted):** Passwords, credit cards, government IDs. **Permanently banned** from language models. Handled via automated regex masking.

---

### C. Deep Dive: `docs/TOKEN_BUDGET_CALCULATOR.md`

The fundamental formula every AI engineer must know:
$$\text{Cost} = \text{Users} \times \text{Queries/Day} \times \text{Tokens/Query} \times \text{Days} \times \text{Price/Token}$$

- Notice how input tokens (prompts + retrieved documents) almost always exceed output tokens (answers).
- Notice why local models (Ollama `llama3.2`) change the economics: **Marginal cost per token becomes \$0.00**, making on-premise AI predictable and affordable.

---

## 4. Classroom Discussion Prompts

1. *"If you were building this assistant for a commercial bank, which risk in the register would worry your Chief Information Security Officer (CISO) the most? Why?"*
2. *"Why does setting the temperature to 0.0 in `llm.py` help mitigate RSK-02 (Policy Hallucination)?"*
3. *"Why is an agent that admits 'I don't know' vastly superior in industry to an agent that always tries to generate an answer?"*

---

## 5. What To Do Next

Now that our risk and governance framework is established, proceed to **Step 03** to implement secret management and the 12-factor configuration pattern:
```bash
git checkout step-03-secure-confidential-data
```

# Project Brief: Acme Corp Internal Knowledge Base & Ticket Assistant

> **Status:** Approved for Implementation  
> **Document Version:** 1.0.0  
> **Target Audience:** Internal Acme Employees (HR & IT Support)  
> **Project Owner:** AI Engineering Team

---

## 1. Executive Summary & Goal

Acme Corp employees spend an estimated 45 minutes daily navigating fragmented company policies, asking repetitive questions to HR and IT, or waiting in manual ticket queues for routine inquiries (such as leave entitlement, VPN resets, or remote work permissions).

**Primary Goal:**  
Deploy a secure, privacy-preserving, containerized AI assistant that answers employee questions accurately using official company documents, executes routine support actions (such as filing tickets), and enforces strict human authorization before executing irreversible actions.

---

## 2. In-Scope vs. Non-Goals (Boundaries)

Defining what the AI system **must NOT do** is the single most critical safeguard in enterprise AI architecture.

### In-Scope (What We Are Building)
- ✅ **Grounding & Retrieval:** Answer queries strictly using verified Markdown documentation stored in `data/docs/`.
- ✅ **Source Citation:** Mandatory citation of source documents for every answer provided.
- ✅ **Tool Execution:** Ability to run deterministic mathematical functions (e.g., leave calculation based on tenure).
- ✅ **Human-in-the-Loop (HITL):** Require explicit user confirmation before creating persistent support tickets.
- ✅ **Local Inference:** Operate 100% locally via Ollama and FastEmbed to ensure zero data exfiltration and zero API expense.
- ✅ **Containerization:** Distribute as a reproducible Docker Compose service.

### Non-Goals (Strict Out-of-Scope)
- ❌ **No Legal or Medical Counseling:** The assistant must never advise on employment disputes, legal liability, or medical diagnoses.
- ❌ **No Autonomous Write Access:** The assistant cannot modify employee records, alter databases, or submit tickets without human review.
- ❌ **No Speculative Answering:** If a policy is not present in the ingested knowledge base, the model is strictly forbidden from "guessing" or extrapolating plausible policies. It must admit: *"I don't know based on the available documents."*
- ❌ **No External Cloud Transmission:** No employee questions or corporate documents may be sent to third-party proprietary APIs (OpenAI, Anthropic) without explicit enterprise data processing agreements.

---

## 3. Measurable Success Metrics (SLAs)

| Metric | Target | Measurement Method |
|---|---|---|
| **Answer Accuracy & Grounding** | $\ge 90\%$ | Automated evaluation against golden Q&A dataset (`tests/test_eval.py`) |
| **Hallucination / Ungrounded Rate** | $0\%$ | Automated output guardrail replacing ungrounded claims with "I don't know" |
| **Source Attribution Rate** | $100\%$ | Mandatory inclusion of `(Source: <filename>.md)` in verified answers |
| **Secret Leaks to Version Control** | $0$ | Pre-commit scanning via Gitleaks and Yelp detect-secrets |
| **Inference Cost** | $\$0.00$ | Local inference execution on student laptops |
| **Cold Start Deployment Time** | $< 2$ minutes | Single-command launch via `docker compose run --rm assistant` |

---

## 4. Architectural Boundaries

```
[Employee Question]
       │
       ▼
[Input Guardrails: Injection & PII Redaction]
       │
       ▼
[Local Ollama Agent (llama3.2)] ──► [Deterministic Tools (calculate_leave)]
       │                        └──► [Human-Approved Tools (create_ticket)]
       ▼
[Chroma Vector Store (FastEmbed)]
       │
       ▼
[Output Guardrail: Source Citation Check]
       │
       ▼
[Grounded Answer with Source Attribution]
```

---

## 5. Team Governance & Handover

- **Lead Engineer:** Workshop Participant
- **Reviewer:** Dr. Anjit T A (Faculty Lead)
- **Deployment Target:** Acme Corp Internal Developer Cloud / Local Edge Devices

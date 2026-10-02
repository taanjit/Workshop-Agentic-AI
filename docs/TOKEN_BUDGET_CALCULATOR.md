# Enterprise Token Budget & Economics Calculator

> **Purpose:** Estimate monthly inference expenses, hardware sizing, and capacity planning before deploying an AI agent.

---

## 1. The Token Cost Formula

Unlike traditional web applications where compute costs scale sublinearly with traffic, LLM API costs scale **linearly** with every token processed.

$$\text{Monthly Cost} = N_{\text{users}} \times Q_{\text{per\_day}} \times \left( T_{\text{in}} \cdot P_{\text{in}} + T_{\text{out}} \cdot P_{\text{out}} \right) \times D_{\text{days}}$$

Where:
- $N_{\text{users}}$: Active daily employee count
- $Q_{\text{per\_day}}$: Average queries per employee per day
- $T_{\text{in}}$: Input tokens per query (System prompt + Chat history + Retrieved RAG chunks + User query)
- $T_{\text{out}}$: Output tokens per query (Generated answer + Tool call JSON payloads)
- $P_{\text{in}}$: Price per million input tokens
- $P_{\text{out}}$: Price per million output tokens
- $D_{\text{days}}$: Working days in a month (standard: 22 to 30)

---

## 2. Real-World Enterprise Scenario: Acme Corp

Assume Acme Corp deploys this assistant to **1,000 employees**:
- **Daily Volume:** 5 questions per employee = 5,000 queries/day.
- **RAG Context Size:**
  - System Prompt: 250 tokens
  - 3 Retrieved Document Chunks (500 chars each): ~450 tokens
  - User Query: 50 tokens
  - Total $T_{\text{in}} \approx 750$ tokens
- **Agent Reasoning & Output:**
  - Tool invocation request: ~100 tokens
  - Final Answer: ~150 tokens
  - Total $T_{\text{out}} \approx 250$ tokens
- **Total Tokens per Query:** 1,000 tokens.
- **Monthly Token Consumption:**
  $$5,000 \text{ queries/day} \times 1,000 \text{ tokens} \times 30 \text{ days} = \mathbf{150,000,000 \text{ tokens/month}}$$

---

## 3. Cost Comparison: Cloud APIs vs. Local Ollama

| Provider / Model | Input Price ($ / 1M) | Output Price ($ / 1M) | Monthly Cloud Cost (150M Tokens) | Hardware Required |
|---|:---:|:---:|:---:|---|
| **Proprietary Commercial LLM (Tier 1)** | \$5.00 | \$15.00 | **\$1,125.00 / mo** | None (Cloud SaaS) |
| **Commodity Cloud API (Tier 2)** | \$0.50 | \$1.50 | **\$112.50 / mo** | None (Cloud SaaS) |
| **Local On-Prem Ollama (Llama 3.2)** | **\$0.00** | **\$0.00** | **\$0.00 (Zero Marginal Cost)** | 1x Local Workstation (8GB–16GB RAM) or Internal Server |

---

## 4. Hardware Sizing Guidelines for Local Ollama

| Model Parameter Size | Quantization | Minimum RAM Required | Recommended Hardware | Tokens/sec Speed |
|---|:---:|:---:|---|:---:|
| **3B (`llama3.2:3b`)** | 4-bit (Q4_K_M) | 4 GB | Standard Laptop CPU / Apple Silicon M1+ | 25 – 45 t/s |
| **8B (`llama3.1:8b`)** | 4-bit (Q4_K_M) | 8 GB | 16 GB Laptop / Workstation | 15 – 30 t/s |
| **70B (`llama3.1:70b`)** | 4-bit (Q4_K_M) | 48 GB | Multi-GPU Server (e.g. 2x RTX 3090/4090) | 8 – 15 t/s |

### Architectural Conclusion
For an internal enterprise document assistant, running a quantized **3B or 8B model locally** provides ample reasoning accuracy for document question answering while delivering **zero incremental API cost** and **100% data sovereignty**.

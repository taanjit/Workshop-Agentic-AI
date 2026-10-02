# Step 05: Agent Capabilities, Tool Calling & Human-in-the-Loop

> **Branch:** `step-05-agent-tools-and-skills`  
> **Session:** 05 — Adding Skills/Tools to an Agent  
> **Duration:** 45 Minutes (20 min lecture / 25 min hands-on lab)

---

## 1. Purpose

The objective of Step 05 is to bridge the gap between **conversational chatbots** (which only generate text) and **autonomous AI agents** (which decide when and how to invoke external software tools).

In this step, we implement:
1. The **Model Factory** (`src/kb_assistant/llm.py`) connecting to local Ollama and FastEmbed.
2. A **Deterministic Tool Suite** (`src/kb_assistant/tools.py`) defining schemas for policy search, leave calculation, and ticket creation.
3. The **Agent Core Loop** (`src/kb_assistant/agent.py`) with a `MAX_STEPS` circuit-breaker and a **Human-in-the-Loop (HITL)** authorization gate.
4. A **Supervisor Router** (`src/kb_assistant/router.py`) dispatching queries between HR and IT specialists.
5. An **Interactive Playground** (`try_tool.py`) isolating the "Aha!" moment of tool calling.

---

## 2. Why It Is Used in Industry

### The Core Flaw of LLMs
Language models do not calculate; they predict the next most likely token based on probabilistic statistical distributions. If you ask an LLM:
> *"An employee joined on March 14, 2021. Today is October 2, 2026. How many leave days do they have?"*
The model might hallucinate 21 days, 24 days, or 18 days depending on temperature randomness. **In enterprise payroll, guessing is unacceptable.**

### The Agentic Solution: Function Calling
Instead of letting the model compute the answer, we provide it with a Python function:
```python
@tool
def calculate_leave(years_of_service: float) -> int: ...
```
1. The model inspects the user question.
2. It recognizes that it needs to calculate leave for 5.5 years.
3. It emits a structured JSON command: `{"name": "calculate_leave", "args": {"years_of_service": 5.5}}`.
4. Our Python runtime executes the function and gets `28`.
5. The model receives `28` and explains it to the user.

### Why Human-in-the-Loop (HITL)?
Reading documents is low-risk. **Writing data or triggering actions** (e.g. creating tickets, transferring funds, restarting servers) is high-risk. By categorizing `create_ticket` into `RISKY_TOOLS`, our agent will literally pause execution and ask the human: `Do you authorize this action? [y/N]`.

---

## 3. Line-by-Line Breakdown

### A. Deep Dive: `src/kb_assistant/tools.py`

```python
@tool
def calculate_leave(years_of_service: float) -> int:
    """Calculate annual paid leave days entitlement for an employee based on years of service."""
```
- **The `@tool` Decorator:** Converts standard Python functions into JSON Schema definitions conforming to the OpenAI/Ollama function calling protocol.
- **Type Annotations (`years_of_service: float`):** Generates strict parameter validation so the model knows what types to supply.
- **The Docstring:** Crucial! The model reads your docstring as an instruction manual. A vague docstring means the model won't know when to invoke the tool.

```python
RISKY_TOOLS = {"create_ticket"}
```
- **Line 87:** Defines which actions alter external state and require human sign-off before running.

---

### B. Deep Dive: `src/kb_assistant/agent.py`

```python
MAX_STEPS: int = 5
```
- **Line 33:** **The Circuit-Breaker.** Without a step limit, an agent that gets confused by an error can loop endlessly between tools, consuming 100% CPU or burning thousands of tokens.

```python
for step in range(1, MAX_STEPS + 1):
    ai_response = llm.invoke(messages)
    messages.append(ai_response)
    
    if not ai_response.tool_calls:
        return text_of(ai_response)
```
- **Line 65–72:** The ReAct Loop.
  - The model inspects conversation history.
  - If `ai_response.tool_calls` is empty, the model has gathered enough information and generated the final text answer.
  - If `tool_calls` exists, the agent halts, executes each requested tool, packages the response inside a `ToolMessage`, and repeats the loop.

```python
elif tool_name in RISKY_TOOLS and not (auto_approve or ask_human(tool_name, tool_args)):
    result_content = "ACTION_REJECTED: The human operator declined authorization."
```
- **Line 92–95:** The HITL Gate. If the user types `n`, the tool is never executed, and the model is informed that the human declined the action.

---

## 4. What To Do Next (Hands-on Lab)

Execute the following hands-on verification exercises:

```bash
# 1. Experience the "Aha!" Moment of function calling
python3 try_tool.py

# 2. Test the full agent loop with leave calculation
PYTHONPATH=src python3 -c "
from kb_assistant.agent import run_agent
print(run_agent('I have worked at Acme Corp for 4 years. How many leave days do I get?'))
"

# 3. Test the Human-in-the-Loop approval gate
PYTHONPATH=src python3 -c "
from kb_assistant.agent import run_agent
print(run_agent('My laptop screen is flickering. Please create a support ticket for me.'))
"
# (Observe: The CLI will pause and prompt you: 'Do you authorize this action? [y/N]:')
```

Once you have verified function calling and HITL authorization, proceed to **Step 06** to implement the RAG knowledge base, guardrails, and automated evaluation tests:
```bash
git checkout step-06-rag-guardrails-and-evals
```

"""
Acme Corp Internal Knowledge Base Assistant
Module: Tool Definitions & Function Schemas

Tools are deterministic Python functions exposed to the Language Model.
The LLM does NOT execute these functions itself; rather, it outputs a JSON
specification containing the tool name and validated arguments.
Our agent runtime intercepts the request, executes the Python code, and
returns the result back to the model.
"""

import json
import datetime
from pathlib import Path
from langchain_core.tools import tool
from . import config


@tool
def search_kb(query: str) -> str:
    """
    Search the Acme Corp internal knowledge base for company policies, IT help, or HR rules.
    Use this tool whenever an employee asks about leave entitlements, VPN issues,
    remote work allowances, equipment replacement, or office policies.
    """
    try:
        from .rag import retrieve
        chunks = retrieve(query)
        if not chunks:
            return "NO_RESULTS: No relevant policy documents found matching the query."
        return "\n\n".join(
            f"[Source: {chunk['source']}]\n{chunk['text']}" for chunk in chunks
        )
    except ImportError:
        # Graceful fallback in Step 05 before RAG module is fully implemented in Step 06
        return (
            "[Source: leave_policy.md]\n"
            "Employees with < 2 years receive 18 days leave; 2-5 years receive 24 days; > 5 years receive 28 days.\n"
            "[Source: it_support.md]\n"
            "Reset VPN password at it.acme.example/reset using authenticator app."
        )


@tool
def calculate_leave(years_of_service: float) -> int:
    """
    Calculate annual paid leave days entitlement for an employee based on years of service.
    
    Args:
        years_of_service: Number of full or partial years the employee has worked at Acme Corp.
    
    Returns:
        Exact number of annual leave days (18, 24, or 28).
    """
    # Deterministic business logic executed in Python (not guessed by LLM)
    if years_of_service < 2.0:
        return 18
    elif years_of_service <= 5.0:
        return 24
    else:
        return 28


@tool
def create_ticket(summary: str) -> str:
    """
    Create a persistent IT or HR support ticket in Acme's tracking system.
    
    ⚠️ RISKY TOOL: This action causes irreversible side-effects (writes to disk/database)
    and strictly REQUIRES human approval before execution.
    
    Args:
        summary: Clear, concise description of the employee's issue or request.
    
    Returns:
        Confirmation message containing the generated Ticket ID.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    ticket_id = f"TICK-{timestamp}"
    record = {
        "id": ticket_id,
        "summary": summary.strip(),
        "created_at": datetime.datetime.now().isoformat(),
        "status": "OPEN",
    }

    # Append ticket to local JSONL audit file
    tickets_path = Path(config.TICKETS_FILE)
    with tickets_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return f"SUCCESS: Support ticket {ticket_id} created with status 'OPEN'."


# ------------------------------------------------------------------------------
# Tool Registries
# ------------------------------------------------------------------------------
# Complete list of tools bound to the LLM
TOOLS = [search_kb, calculate_leave, create_ticket]

# Map of tool names to callable objects for rapid lookup in the agent loop
TOOL_MAP = {t.name: t for t in TOOLS}

# Set of tools requiring explicit human confirmation before invocation
RISKY_TOOLS = {"create_ticket"}

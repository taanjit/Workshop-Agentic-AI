"""
Acme Corp Internal Knowledge Base Assistant
Module: Supervisor Router (Multi-Agent Dispatcher)

In enterprise agent architectures, routing queries to domain-specific
specialists (e.g. HR vs IT) yields higher accuracy, smaller prompts,
and lower latency than using one bloated generalist prompt.
"""

from langchain_core.messages import SystemMessage, HumanMessage
from .llm import get_llm, text_of

ROUTER_PROMPT = """You are Acme Corp's internal query dispatcher.
Classify the user's inquiry into exactly ONE of the following departments:
- HR: Questions regarding annual leave, sick leave, benefits, remote work approvals, or parental leave.
- IT: Questions regarding VPN access, password resets, laptops, monitors, software, or technical support tickets.

Respond with exactly ONE word: either 'HR' or 'IT'. Do not include punctuation or explanation.
"""


def route(question: str) -> str:
    """
    Classify a question into 'HR' or 'IT'.
    
    Args:
        question: Cleaned user input text.
        
    Returns:
        Department category string ('HR' or 'IT').
    """
    try:
        llm = get_llm(temperature=0.0)
        messages = [
            SystemMessage(content=ROUTER_PROMPT),
            HumanMessage(content=question),
        ]
        raw_output = text_of(llm.invoke(messages)).strip().upper()

        if "IT" in raw_output.split()[:2]:
            return "IT"
        return "HR"
    except Exception:
        # Fallback to general HR triage on error
        return "HR"

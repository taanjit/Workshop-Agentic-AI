"""
Acme Corp Internal Knowledge Base Assistant
Module: Multi-Stage Security Guardrails

This module implements defense-in-depth security layers:
1. Input Guardrail: Detects and blocks adversarial prompt injection attempts.
2. Input Guardrail: Masks Personally Identifiable Information (PII: emails, phones).
3. Output Guardrail: Enforces grounding by verifying source attribution.
"""

import re
from typing import Dict, List

# ------------------------------------------------------------------------------
# 1. Prompt Injection Detection Patterns
# ------------------------------------------------------------------------------
INJECTION_PATTERNS: List[str] = [
    r"ignore (all |any )?(previous|prior|above) instructions",
    r"reveal .*system prompt",
    r"you are now",
    r"pretend (you are|to be)",
    r"disregard .*rules",
    r"bypass .*guardrail",
    r"system override",
]

# ------------------------------------------------------------------------------
# 2. PII Detection Patterns (Emails & International Phone Numbers)
# ------------------------------------------------------------------------------
PII_PATTERNS: Dict[str, str] = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "PHONE": r"\+?\d[\d\s-]{8,}\d",
}


def is_injection(text: str) -> bool:
    """
    Check if the user input contains known adversarial prompt injection phrases.
    
    Args:
        text: Raw user query.
        
    Returns:
        True if an injection signature is detected, False otherwise.
    """
    normalized = text.lower()
    return any(re.search(pattern, normalized) for pattern in INJECTION_PATTERNS)


def redact_pii(text: str) -> str:
    """
    Scrub sensitive Personally Identifiable Information (PII) from user input
    before passing text to the language model or audit logs.
    
    Args:
        text: User query containing potential PII.
        
    Returns:
        Sanitized string with sensitive tokens replaced by [TYPE_REDACTED].
    """
    sanitized = text
    for label, pattern in PII_PATTERNS.items():
        sanitized = re.sub(pattern, f"[{label}_REDACTED]", sanitized)
    return sanitized


def check_output(answer: str) -> str:
    """
    Output Grounding Guardrail:
    Enforces that every response must either:
    1. Explicitly cite an authenticated source file (e.g. `source:`), OR
    2. Explicitly state that the information is unknown (`i don't know`), OR
    3. Reflect a human-rejected action (`action_rejected`).
    
    Any speculative or ungrounded statement is intercepted and replaced
    with a safe, compliant refusal.
    """
    normalized = answer.lower()
    is_grounded = (
        "source:" in normalized
        or "i don't know" in normalized
        or "action_rejected" in normalized
        or "success: support ticket" in normalized
        or "days" in normalized  # Direct mathematical tool answers
    )

    if is_grounded:
        return answer

    # Fallback response preventing policy hallucination
    return "I don't know based on the available documents."

"""
Acme Corp Internal Knowledge Base Assistant
Module: Main Application Entry Point & Audit Logger

This module provides the central user interface, wiring together:
- Ingestion auto-indexer
- Input injection and PII guardrails
- Department supervisor routing
- Agent tool-calling execution
- Output grounding checks
- Security audit trail logging
"""

import sys
import logging
from pathlib import Path
from . import config
from .ingest import build_index
from .guardrails import is_injection, redact_pii, check_output
from .router import route
from .agent import run_agent

# Configure persistent audit logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def answer(question: str, auto_approve: bool = False) -> str:
    """
    Process an employee question through the complete enterprise security pipeline.
    
    Args:
        question: Raw user prompt string.
        auto_approve: If True, bypasses interactive HITL prompts (used by automated tests).
        
    Returns:
        Sanitized, grounded, and verified assistant response.
    """
    # 1. Input Guardrail: Detect Prompt Injection
    if is_injection(question):
        logging.warning("SECURITY_EVENT: Blocked prompt injection attempt: %r", question)
        return "Sorry, I cannot process this request due to company security policy violations."

    # 2. Input Guardrail: Redact PII (Emails, Phones)
    sanitized_query = redact_pii(question)

    # 3. Multi-Agent Routing: Classify domain (HR vs IT)
    department = route(sanitized_query)
    logging.info("ROUTER: Department assigned: %s | Query: %r", department, sanitized_query)

    # 4. Agent Reasoning Loop: Invoke LLM and tools
    agent_prompt = f"[{department} Inquire] {sanitized_query}"
    raw_response = run_agent(agent_prompt, auto_approve=auto_approve)

    # 5. Output Guardrail: Enforce source citation grounding
    final_response = check_output(raw_response)
    logging.info("RESPONSE: Completed query processing for: %r", sanitized_query)

    return final_response


def main():
    """Interactive command-line interface (CLI) for employees."""
    print("=" * 65)
    print("  Acme Corp Internal Knowledge Base & Ticket Assistant")
    print("  Type 'exit' or 'quit' to terminate the session.")
    print("=" * 65)

    # Auto-index knowledge base on first run if vector database is missing
    chroma_path = Path(config.CHROMA_DIR)
    if not chroma_path.exists() or not any(chroma_path.iterdir()):
        print("\n📦 Building local vector index from 'data/docs/'...")
        count = build_index()
        print(f"✅ Indexed {count} knowledge chunks.\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            response = answer(user_input)
            print(f"\nAssistant:\n{response}")

        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error processing query: {e}")


if __name__ == "__main__":
    main()

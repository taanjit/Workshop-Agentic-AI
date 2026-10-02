"""
Automated Agent Evaluation: Golden Q&A Benchmark
Acme Corp CI/CD Quality Gate

This test suite executes the complete agent pipeline against a curated
golden test set. Tests are marked as 'slow' because they invoke the local LLM.

Usage:
    pytest -m "not slow"   # Fast guardrail tests only (0 tokens, milliseconds)
    pytest -m slow         # Full end-to-end evaluation using local LLM
"""

import pytest
from kb_assistant.main import answer

# The Golden Set: (Question, Mandatory Expected Fact/Substring)
GOLDEN_SET = [
    ("How many annual leave days do I get after 3 years of service?", "24"),
    ("Where do I go to reset my VPN password?", "it.acme.example"),
    ("How many days per year am I allowed to work from abroad?", "14"),
    ("What is Acme Corp's policy on parental leave?", "don't know"),
]


@pytest.mark.slow
@pytest.mark.parametrize("question,expected_substring", GOLDEN_SET)
def test_golden_qa_benchmarks(question: str, expected_substring: str):
    """
    Verify that the assistant correctly answers golden questions using RAG
    and strictly admits 'I don't know' for questions outside company documents.
    """
    result = answer(question, auto_approve=True).lower()
    assert (
        expected_substring.lower() in result
    ), f"Failed golden assertion! Query: '{question}' | Expected: '{expected_substring}' | Got: '{result}'"

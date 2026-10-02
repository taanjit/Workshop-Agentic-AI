#!/usr/bin/env python3
"""
Red-Team Exercise: Secret Leak Simulator
Acme Corp Security Training

This script simulates an accidental developer credential leak by generating
a temporary file containing a fake OpenAI API key signature.

Usage:
    1. python3 scripts/simulate_leak.py generate
    2. git add test_leak.py
    3. git commit -m "oops: committing a fake key"
       --> OBSERVE: Pre-commit / Gitleaks will BLOCK the commit!
    4. python3 scripts/simulate_leak.py cleanup
"""

import sys
from pathlib import Path

LEAK_FILE = Path("test_leak.py")

# A dummy key formatted to match OpenAI project key entropy patterns
FAKE_KEY_CONTENT = '''# SECURITY TRAINING DEMO: This is a fake key for testing pre-commit hooks
# It has no real value and is designed to trigger Gitleaks pattern detection.
OPENAI_API_KEY = "sk-proj-DEMOFAKEKEY1234567890abcdefghijklmnop1234567890"
'''

def generate():
    LEAK_FILE.write_text(FAKE_KEY_CONTENT)
    print("=" * 65)
    print("🚨 [RED-TEAM SIMULATOR] Generated 'test_leak.py' with fake credentials.")
    print("=" * 65)
    print("Now run the following commands to observe your pre-commit hook in action:")
    print()
    print("   git add test_leak.py")
    print("   git commit -m 'test: attempt to commit a key'")
    print()
    print("Expected outcome: The commit will be BLOCKED by Gitleaks!")
    print("When finished testing, run: python3 scripts/simulate_leak.py cleanup")
    print("=" * 65)

def cleanup():
    if LEAK_FILE.exists():
        LEAK_FILE.unlink()
        print("✅ Cleaned up 'test_leak.py'.")
    else:
        print("ℹ️  'test_leak.py' was already removed.")

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("generate", "cleanup"):
        print("Usage: python3 scripts/simulate_leak.py [generate|cleanup]")
        sys.exit(1)

    if sys.argv[1] == "generate":
        generate()
    elif sys.argv[1] == "cleanup":
        cleanup()

if __name__ == "__main__":
    main()

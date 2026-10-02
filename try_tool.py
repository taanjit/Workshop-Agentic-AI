#!/usr/bin/env python3
"""
Interactive Playground: The 'Aha!' Moment of Function Calling
Acme Corp AI Engineering Training

Run this script to observe how a Language Model requests tool execution
without actually running code itself.

Usage:
    PYTHONPATH=src python3 try_tool.py
"""

import sys
from pathlib import Path

# Add src/ to python path dynamically
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from kb_assistant.llm import get_llm
from kb_assistant.tools import calculate_leave

def main():
    print("=" * 65)
    print("  Interactive Function Calling Demonstration ('Aha!' Moment)")
    print("=" * 65)

    # 1. Initialize local LLM and bind the Python tool
    print("\n1. Binding 'calculate_leave' tool schema to local LLM...")
    try:
        llm = get_llm(temperature=0.0).bind_tools([calculate_leave])
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        return

    # 2. Issue a question that requires mathematical policy calculation
    user_query = "I have been working at Acme Corp for 3 years. How many annual leave days do I get?"
    print(f"2. Sending query: \"{user_query}\"")
    print("   Waiting for model response...\n")

    try:
        reply = llm.invoke(user_query)

        print("-" * 65)
        print("Model Response Inspection:")
        print("-" * 65)
        print(f"• Text Content:  {repr(reply.content)}")
        print(f"• Tool Calls:    {reply.tool_calls}")
        print("-" * 65)

        if reply.tool_calls:
            call = reply.tool_calls[0]
            name = call["name"]
            args = call["args"]
            print(f"\n💡 [THE 'AHA!' MOMENT]:")
            print(f"   The model DID NOT execute Python code!")
            print(f"   Instead, it produced a structured JSON intent:")
            print(f"     Function : {name}")
            print(f"     Arguments: {args}")
            print()
            print("   Now our host application executes the real Python code:")
            result = calculate_leave.invoke(args)
            print(f"   ==> calculate_leave({args}) returned: {result} days")
            print()
            print("   In the full agent loop, this result is sent back to the LLM")
            print("   so it can formulate the final user-facing sentence.")
        else:
            print("\n⚠️ The model answered without generating a tool call.")
            print("   (Ensure your local model supports function calling, e.g. llama3.2 or llama3.1)")

    except Exception as e:
        print(f"❌ Ollama Connection Error: {e}")
        print("   👉 Check that Ollama is running (`ollama serve`) and the model is pulled (`ollama pull llama3.2`).")

    print("=" * 65)

if __name__ == "__main__":
    main()

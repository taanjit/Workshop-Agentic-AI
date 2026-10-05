#!/usr/bin/env python3
"""
Pre-flight Verification Script for Agentic AI Workshop

Run this script prior to the workshop to verify that your environment
has all the required software and local models installed.

Usage:
    python3 check_setup.py
"""

import sys
import shutil
import subprocess
import urllib.request
import json

def check_python():
    version = sys.version_info
    ok = version >= (3, 10)
    print(f"{'✅' if ok else '❌'} Python version: {sys.version.split()[0]} (Requires >= 3.10)")
    return ok

def check_command(cmd, name):
    path = shutil.which(cmd)
    ok = path is not None
    print(f"{'✅' if ok else '❌'} {name}: {'Found (' + path + ')' if ok else 'NOT found'}")
    return ok

def check_docker_daemon():
    if not shutil.which("docker"):
        return False
    try:
        res = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        ok = res.returncode == 0
        print(f"{'✅' if ok else '❌'} Docker daemon: {'Running' if ok else 'Installed but NOT running (please start Docker Desktop)'}")
        return ok
    except Exception as e:
        print(f"❌ Docker daemon check failed: {e}")
        return False

def check_ollama():
    if not shutil.which("ollama"):
        print("❌ Ollama: NOT found. Install from https://ollama.com/")
        return False
    print("✅ Ollama binary: Found")

    # Check if daemon is active
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                print("✅ Ollama service: Running on http://localhost:11434")
                
                # Check for standard model
                recommended_models = ["llama3.2:latest", "llama3.2:3b", "llama3.1:latest", "llama3.1:8b", "llama3:latest", "qwen2.5:3b"]
                available = [m for m in recommended_models if any(m in model_name for model_name in models)]
                
                if available:
                    print(f"✅ Required local LLM detected: {available[0]}")
                    return True
                else:
                    print(f"⚠️  Ollama is running, but no recommended model was found.")
                    print(f"   Installed models: {models if models else 'None'}")
                    print("   👉 Please run:  ollama pull llama3.2")
                    return False
    except Exception:
        print("⚠️  Ollama is installed, but the background service is not running.")
        print("   👉 Start it by running:  ollama serve  (or start the Ollama desktop app)")
        return False

def main():
    print("=" * 60)
    print("  Agentic AI Workshop — Pre-flight Environment Check")
    print("=" * 60)
    print()

    results = [
        check_python(),
        check_command("git", "Git version control"),
        check_command("docker", "Docker CLI"),
        check_docker_daemon(),
        check_ollama()
    ]

    print()
    print("=" * 60)
    if all(results):
        print("🎉 EXCELLENT! Your machine is 100% prepared for the workshop.")
    else:
        print("⚠️  Some prerequisites are missing or need attention above.")
        print("    Please resolve them before the hands-on session starts.")
    print("=" * 60)

if __name__ == "__main__":
    main()

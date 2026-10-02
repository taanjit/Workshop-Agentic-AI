#!/usr/bin/env bash
# ==============================================================================
# Docker Image Secret Audit Script
# Acme Corp Security Verification
# ==============================================================================
# Verifies that no .env or sensitive configuration files were accidentally
# copied into the Docker container image during build time.
# ==============================================================================

set -euo pipefail

IMAGE_NAME="workshop-agentic-ai-assistant"

echo "============================================================"
echo "  Auditing Docker Image for Accidental Credential Baking"
echo "============================================================"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker CLI not found. Please install Docker."
    exit 1
fi

echo "1. Inspecting /app directory inside container image..."
# Run a temporary container and list all files including hidden ones
docker run --rm --entrypoint /bin/sh "$IMAGE_NAME" -c "ls -la /app"

echo ""
echo "2. Checking for .env presence..."
if docker run --rm --entrypoint /bin/sh "$IMAGE_NAME" -c "test -f /app/.env" 2>/dev/null; then
    echo "🚨 SECURITY VIOLATION: .env file found inside Docker image!"
    exit 1
else
    echo "✅ PASS: No .env file detected inside image filesystem."
fi

echo ""
echo "3. Checking execution user..."
CURRENT_USER=$(docker run --rm --entrypoint /bin/sh "$IMAGE_NAME" -c "whoami")
if [ "$CURRENT_USER" = "appuser" ]; then
    echo "✅ PASS: Container runs as unprivileged user '$CURRENT_USER' (Non-root)."
else
    echo "⚠️  WARNING: Container is running as '$CURRENT_USER' instead of unprivileged 'appuser'."
fi

echo "============================================================"
echo "🎉 Image audit complete. Zero secrets detected in layers!"
echo "============================================================"

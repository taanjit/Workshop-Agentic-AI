# Step 07: Production Containerization & Deployment with Docker

> **Branch:** `step-07-docker-deployment`  
> **Session:** 07 — Deploy Using Docker  
> **Duration:** 45 Minutes (15 min architecture / 30 min hands-on lab)

---

## 1. Purpose

The objective of Step 07 is to package our completed Knowledge Base Assistant into an **enterprise-ready, containerized microservice**. 

In this step, we implement:
1. A security-hardened **`Dockerfile`** running as an unprivileged non-root user.
2. An orchestration specification (**`docker-compose.yml`**) routing traffic between the containerized assistant and the host machine's Ollama engine.
3. A build exclusion mask (**`.dockerignore`**) guaranteeing zero secrets enter Docker image layers.
4. A production **Handover Runbook** (`docs/HANDOVER.md`).
5. An automated **Image Secret Audit Script** (`scripts/verify_container_secrets.sh`).

---

## 2. Why It Is Used in Industry

### "Works on My Machine" is Not a Deployment Strategy
When deploying AI agents across enterprise clouds (AWS, GCP, Azure, on-prem Kubernetes):
- One developer runs macOS on ARM64; another runs Ubuntu on x86; the production server runs Red Hat.
- Differences in Python versions, C-library bindings (ONNX, sqlite3), or path separators break solo scripts.
- **Docker Containers** freeze the entire operating system, Python runtime, dependencies, and code into an immutable image that runs identically everywhere.

### The 2 Golden Rules of Container Security
1. **Never Run as Root:** If an attacker achieves code execution through prompt injection or a vulnerable dependency inside a container running as `root`, they can break out and compromise the host operating system. We enforce `USER appuser`.
2. **Never Bake Secrets into Images:** Running `COPY .env /app/.env` inside a Dockerfile is catastrophic. Anyone with read access to the Docker image or registry can inspect layers with `docker history` and steal your keys. Secrets must be injected **strictly at runtime** via `env_file`.

---

## 3. Line-by-Line Breakdown

### A. Deep Dive: `Dockerfile`

```dockerfile
FROM python:3.11-slim
```
- **Why `python:3.11-slim`?** Full Python images weigh over 1 GB. Alpine images, while small, lack standard C-libraries ($glibc$) causing severe compatibility issues with machine learning libraries like FastEmbed and ONNX. `slim` provides a lightweight Debian footprint (~150MB) with 100% binary compatibility.

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
```
- **Layer Caching:** Docker builds in sequential cached layers. By copying `requirements.txt` and running `pip install` **before** copying your application code, Docker caches the heavy package installation. When you edit Python code, rebuilds take **2 seconds** instead of reinstalling all dependencies!

```dockerfile
RUN useradd --create-home --shell /bin/bash appuser && \
    mkdir -p /app/chroma_db && \
    chown -R appuser:appuser /app
USER appuser
```
- Creates an unprivileged user named `appuser` and assigns ownership of the persistent Chroma vector folder. Switches the container's execution context to non-root.

---

### B. Deep Dive: `docker-compose.yml`

```yaml
env_file:
  - .env
```
- **Runtime Secret Injection:** Docker Compose reads your local `.env` and injects keys into the container's memory during boot. The image itself remains completely free of credentials.

```yaml
environment:
  OLLAMA_BASE_URL: http://host.docker.internal:11434
extra_hosts:
  - "host.docker.internal:host-gateway"
```
- Inside a Docker container, `localhost` refers to the container itself, **not your laptop**.
- `host.docker.internal` allows the containerized assistant to communicate seamlessly with the Ollama service running natively on your laptop!

```yaml
volumes:
  - chroma_data:/app/chroma_db
```
- **Named Volumes:** Containers are ephemeral by default (any data written inside is wiped when the container stops). Mounting a named volume ensures your vector database index persists across restarts.

---

## 4. What To Do Next (Hands-on Lab)

Execute the complete container build, launch, and security audit:

```bash
# 1. Build the Docker container image
docker compose build

# 2. Launch the containerized assistant interactively
docker compose run --rm assistant
```

Test asking the same policy questions inside the container:
- `"How many annual leave days do I get after 3 years?"`
- `"Where do I go to reset my VPN password?"`
- `"What is the company's parental leave policy?"`

### 3. Run the Security Audit Script
Verify that your container image is 100% compliant and contains zero secrets:
```bash
chmod +x scripts/verify_container_secrets.sh
./scripts/verify_container_secrets.sh
```

### 4. Tag the Final Release
```bash
git tag v1.0.0
git push origin --tags
```

🎉 **Congratulations!** You have built, tested, secured, evaluated, and containerized an enterprise-ready Agentic AI system from scratch!

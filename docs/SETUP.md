# 📋 Setup Guide — DevOps Toolchain

## Install Required Tools

### 1. Docker Desktop ✅ (Required)
Download: https://www.docker.com/products/docker-desktop/

**Important — allocate enough resources:**
- Open Docker Desktop → Settings → Resources
- Set Memory to at least **6 GB** (SonarQube + Jenkins need it)
- Set CPUs to at least **4**
- Click Apply & Restart

### 2. Python 3.11+ (for local development)
Download: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during install
- Verify: `python --version`

---

## Start the Full Toolchain

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/devops-toolchain.git
cd devops-toolchain

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# OR manually:
docker compose -f docker/docker-compose.yml up -d
```

**First startup takes 3-5 minutes** — Docker pulls large images (Jenkins ~700MB, SonarQube ~600MB, Nexus ~500MB).

---

## Access All Tools

| Tool | URL | Username | Password |
|---|---|---|---|
| **App** | http://localhost:80 | — | — |
| **Flask direct** | http://localhost:5000 | — | — |
| **Jenkins** | http://localhost:8090 | admin | admin123 |
| **SonarQube** | http://localhost:9000 | admin | admin |
| **Nexus** | http://localhost:8081 | admin | admin123 |

---

## Test the Application APIs

```bash
# Health check
curl http://localhost:5000/health

# List all tasks
curl http://localhost:5000/api/tasks

# Create a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"My DevOps Task","priority":"high"}'

# Complete a task (replace 1 with actual ID)
curl -X PATCH http://localhost:5000/api/tasks/1/complete

# Filter tasks
curl "http://localhost:5000/api/tasks?status=pending&priority=high"
```

---

## Jenkins — First Time Setup

1. Open http://localhost:8090
2. Login: **admin / admin123**
3. Go to **New Item → Pipeline**
4. Under Pipeline Definition → select **Pipeline script from SCM**
5. Set SCM: **Git**, URL: your GitHub repo URL
6. Script Path: `jenkins/pipelines/Jenkinsfile`
7. Click Save → **Build Now**

### Run the Seed Job (creates all pipelines automatically)
1. Jenkins → New Item → **Freestyle project** → name it `seed-job`
2. Build Steps → **Process Job DSLs**
3. DSL Scripts: `jenkins/jobs/seed-job.groovy`
4. Save and Build

---

## SonarQube — First Time Setup

1. Open http://localhost:9000
2. Login: **admin / admin**
3. Change password when prompted
4. Go to **Administration → Security → Tokens**
5. Generate token named `jenkins-token`
6. Copy the token → paste into Jenkins credentials (ID: `sonarqube-token`)

---

## Stop Everything

```bash
docker compose -f docker/docker-compose.yml down

# Remove all data volumes (fresh start)
docker compose -f docker/docker-compose.yml down -v
```

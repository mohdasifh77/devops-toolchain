# 🚀 Full DevOps Toolchain — Jenkins + SonarQube + Nexus

> **Enterprise-grade CI/CD platform** running 100% locally with Docker Desktop.
> No AWS account needed. Runs Jenkins, SonarQube, Nexus Artifact Registry,
> and a Python/Node.js application — the exact stack used at real companies.

![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![SonarQube](https://img.shields.io/badge/SonarQube-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

---

## 📌 What This Project Does

A complete **DevOps toolchain** that automates the full software delivery lifecycle:

```
Developer pushes code
        │
        ▼
  GitHub Actions          ← Triggers on every push
        │
        ▼
  Jenkins Pipeline        ← Orchestrates everything
  ┌─────┴──────────────────────────────┐
  │  1. Checkout code                  │
  │  2. Install dependencies           │
  │  3. Run unit tests                 │
  │  4. SonarQube code quality scan    │
  │  5. Build Docker image             │
  │  6. Security scan (Trivy)          │
  │  7. Push to Nexus registry         │
  │  8. Deploy to staging              │
  │  9. Run integration tests          │
  │  10. Deploy to production          │
  └────────────────────────────────────┘
        │
        ▼
   Live App at http://localhost:8080
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Docker Network                     │
│                                                      │
│  ┌──────────────┐    ┌──────────────────────────┐   │
│  │   Jenkins    │───▶│  SonarQube + PostgreSQL  │   │
│  │  :8090       │    │  :9000                   │   │
│  └──────┬───────┘    └──────────────────────────┘   │
│         │                                            │
│         │            ┌──────────────────────────┐   │
│         ├───────────▶│   Nexus Repository       │   │
│         │            │   :8081                  │   │
│         │            └──────────────────────────┘   │
│         │                                            │
│         │            ┌──────────────────────────┐   │
│         └───────────▶│   Application (Python)   │   │
│                      │   + Nginx Reverse Proxy  │   │
│                      │   :80                    │   │
│                      └──────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
devops-toolchain/
├── app/                        # Python Flask application
│   ├── src/
│   │   ├── main.py             # Flask app with REST API
│   │   └── database.py         # SQLite database layer
│   ├── tests/
│   │   ├── test_app.py         # Unit tests
│   │   └── test_integration.py # Integration tests
│   ├── Dockerfile              # Multi-stage Docker build
│   └── requirements.txt
├── jenkins/
│   ├── Dockerfile              # Custom Jenkins image + plugins
│   ├── pipelines/
│   │   ├── Jenkinsfile         # Main CI/CD pipeline
│   │   └── Jenkinsfile.pr      # PR validation pipeline
│   ├── shared-library/vars/    # Reusable pipeline functions
│   │   ├── buildApp.groovy
│   │   ├── runTests.groovy
│   │   ├── sonarScan.groovy
│   │   └── deployApp.groovy
│   └── jobs/
│       └── seed-job.groovy     # Auto-creates all Jenkins jobs
├── sonarqube/
│   └── sonar-project.properties # SonarQube analysis config
├── nexus/
│   └── nexus.properties        # Nexus configuration
├── nginx/
│   └── nginx.conf              # Reverse proxy config
├── docker/
│   └── docker-compose.yml      # Full toolchain stack
├── kubernetes/                 # K8s manifests for each tool
├── scripts/
│   ├── setup.sh                # One-click setup
│   ├── configure-jenkins.sh    # Auto-configure Jenkins
│   └── health-check.sh         # Check all tools are running
├── .github/workflows/
│   └── ci-cd.yml               # GitHub Actions pipeline
└── docs/
    ├── SETUP.md
    ├── JENKINS.md
    ├── SONARQUBE.md
    └── NEXUS.md
```

---

## ⚡ Quick Start

### Step 1 — Install prerequisites
```bash
# Just needs Docker Desktop — that's it!
# Download: https://www.docker.com/products/docker-desktop/
```

### Step 2 — Start the full toolchain
```bash
git clone https://github.com/YOUR_USERNAME/devops-toolchain.git
cd devops-toolchain
docker compose -f docker/docker-compose.yml up -d
```

### Step 3 — Wait 2 minutes, then open tools
| Tool | URL | Login |
|---|---|---|
| **Jenkins** | http://localhost:8090 | admin / admin123 |
| **SonarQube** | http://localhost:9000 | admin / admin |
| **Nexus** | http://localhost:8081 | admin / admin123 |
| **App** | http://localhost:80 | — |

---

## 🎯 DevOps Skills This Demonstrates

- ✅ **Jenkins** — Declarative pipelines, shared libraries, seed jobs, multi-branch
- ✅ **SonarQube** — Code quality gates, coverage reports, vulnerability scanning
- ✅ **Nexus** — Docker registry, Python (PyPI) proxy, npm proxy
- ✅ **Docker** — Multi-stage builds, Docker-in-Docker, image scanning
- ✅ **Python** — Flask REST API, pytest, coverage reports
- ✅ **Nginx** — Reverse proxy, load balancing config
- ✅ **CI/CD** — Full pipeline from commit to deployment
- ✅ **Infrastructure as Code** — Everything defined as code, reproducible

---

## 📖 Documentation
- [Setup Guide](docs/SETUP.md)
- [Jenkins Guide](docs/JENKINS.md)
- [SonarQube Guide](docs/SONARQUBE.md)
- [Nexus Guide](docs/NEXUS.md)

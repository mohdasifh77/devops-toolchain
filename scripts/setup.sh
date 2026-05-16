#!/usr/bin/env bash
# ==============================================================
# setup.sh — One-click DevOps Toolchain Setup
# ==============================================================
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✅] $*${NC}"; }
info() { echo -e "${YELLOW}[⏳] $*${NC}"; }
err()  { echo -e "${RED}[❌] $*${NC}"; exit 1; }
head() { echo -e "${BLUE}$*${NC}"; }

head ""
head "╔══════════════════════════════════════════════════════════╗"
head "║   🚀 DevOps Toolchain Setup                              ║"
head "║   Jenkins + SonarQube + Nexus + App + Nginx              ║"
head "╚══════════════════════════════════════════════════════════╝"
echo ""

# ── Check Docker ──────────────────────────────────────────────
command -v docker &>/dev/null || err "Docker not found. Install Docker Desktop first."
docker info &>/dev/null       || err "Docker is not running. Start Docker Desktop."
log "Docker is running"

# ── Set kernel param for SonarQube ───────────────────────────
info "Setting vm.max_map_count for SonarQube (requires sudo)..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo sysctl -w vm.max_map_count=262144
    log "Kernel param set"
else
    log "Not Linux — skipping sysctl (SonarQube may show warnings)"
fi

# ── Start services ────────────────────────────────────────────
info "Building and starting all services (first run: 3-5 minutes)..."
docker compose -f docker/docker-compose.yml up -d --build

# ── Wait with progress ────────────────────────────────────────
info "Waiting for services to start..."
for i in $(seq 1 12); do
    echo -n "  ⏳ Waiting... ($((i*15))s)"
    sleep 15
    echo ""
done

# ── Health checks ─────────────────────────────────────────────
echo ""
info "Checking services..."

check_service() {
    local name="$1" url="$2"
    if curl -sf "$url" -o /dev/null 2>/dev/null; then
        log "$name is UP"
    else
        echo -e "${YELLOW}  ⚠️  $name not ready yet (may need more time)${NC}"
    fi
}

check_service "App (Flask)"  "http://localhost:5000/health"
check_service "Nginx Proxy"  "http://localhost:80/health"
check_service "Jenkins"      "http://localhost:8090/login"
check_service "SonarQube"    "http://localhost:9000"
check_service "Nexus"        "http://localhost:8081"

echo ""
head "╔══════════════════════════════════════════════════════════╗"
head "║   🎉 DevOps Toolchain is Running!                        ║"
head "╠══════════════════════════════════════════════════════════╣"
head "║  App (via Nginx) → http://localhost:80                   ║"
head "║  App (direct)    → http://localhost:5000                 ║"
head "║  Jenkins         → http://localhost:8090                 ║"
head "║                    Login: admin / admin123               ║"
head "║  SonarQube       → http://localhost:9000                 ║"
head "║                    Login: admin / admin                  ║"
head "║  Nexus           → http://localhost:8081                 ║"
head "║                    Login: admin / admin123               ║"
head "╠══════════════════════════════════════════════════════════╣"
head "║  Stop: docker compose -f docker/docker-compose.yml down  ║"
head "╚══════════════════════════════════════════════════════════╝"

#!/usr/bin/env bash
# health-check.sh — Check all DevOps tools are running

GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'

echo "================================"
echo "  DevOps Toolchain Health Check"
echo "================================"

check() {
    local name="$1" url="$2"
    if curl -sf "$url" -o /dev/null 2>/dev/null; then
        echo -e "${GREEN}  ✅ $name${NC}"
    else
        echo -e "${RED}  ❌ $name — not reachable at $url${NC}"
    fi
}

check "Flask App"    "http://localhost:5000/health"
check "Nginx Proxy"  "http://localhost:80/health"
check "Jenkins"      "http://localhost:8090/login"
check "SonarQube"    "http://localhost:9000"
check "Nexus"        "http://localhost:8081/service/rest/v1/status"

echo "================================"
echo "  Running containers:"
docker ps --format "  {{.Names}} — {{.Status}}" | grep -E "jenkins|sonarqube|nexus|app|nginx|sonar-db" || true
echo "================================"

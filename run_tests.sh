#!/bin/bash
#
# Automated test runner script for Codeflix Catalog Admin
#
# Usage:
#   ./run_tests.sh              # Fast tests + E2E (starts Keycloak via Docker)
#   ./run_tests.sh --no-cleanup # Keep containers running after tests
#   ./run_tests.sh --fast-only  # Fast tests only (no Docker)
#   ./run_tests.sh --e2e-only   # E2E tests only (starts Keycloak)
#
# Marker reference (see src/pytest.ini):
#   pytest              # default: not e2e
#   pytest -m e2e       # real Keycloak smoke tests

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
SRC_DIR="$PROJECT_ROOT/src"
DOCKER_STARTED=false
CLEANUP=true
TEST_TYPE="all"

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cleanup)
            CLEANUP=false
            shift
            ;;
        --fast-only|--unit-only)
            TEST_TYPE="fast"
            shift
            ;;
        --e2e-only)
            TEST_TYPE="e2e"
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

cleanup() {
    if [ "$DOCKER_STARTED" = true ] && [ "$CLEANUP" = true ]; then
        echo -e "\n${YELLOW}Cleaning up containers...${NC}"
        cd "$PROJECT_ROOT"
        docker compose down -v 2>/dev/null || true
    elif [ "$DOCKER_STARTED" = true ]; then
        echo -e "\n${YELLOW}Keeping containers running (--no-cleanup specified)${NC}"
    fi
}

trap cleanup EXIT

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Codeflix Catalog Admin Test Runner   ${NC}"
echo -e "${BLUE}========================================${NC}\n"

start_keycloak() {
    echo -e "${BLUE}Starting Keycloak...${NC}"
    cd "$PROJECT_ROOT"

    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
        exit 1
    fi

    docker compose up -d keycloak
    DOCKER_STARTED=true
    echo -e "${GREEN}✓ Keycloak container started${NC}\n"

    echo -e "${BLUE}Waiting for Keycloak to be ready...${NC}"
    KEYCLOAK_URL="http://localhost:8080/realms/codeflix"

    for i in $(seq 1 60); do
        if curl -sf "$KEYCLOAK_URL" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Keycloak is ready${NC}\n"
            break
        fi

        if [ $i -eq 60 ]; then
            echo -e "${RED}Error: Keycloak failed to start within timeout${NC}"
            docker compose logs keycloak --tail=50
            exit 1
        fi

        echo -e "  Waiting for Keycloak... (attempt $i/60)"
        sleep 2
    done

    echo -e "${BLUE}Updating .env with Keycloak public key...${NC}"
    PUBLIC_KEY=$(curl -s "$KEYCLOAK_URL" | jq -r '.public_key')

    if [ -z "$PUBLIC_KEY" ] || [ "$PUBLIC_KEY" = "null" ]; then
        echo -e "${RED}Error: Failed to get public key from Keycloak${NC}"
        exit 1
    fi

    if [ -f "$PROJECT_ROOT/.env" ]; then
        sed -i "s|^AUTH_PUBLIC_KEY=.*|AUTH_PUBLIC_KEY=\"$PUBLIC_KEY\"|" "$PROJECT_ROOT/.env"
    else
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env" 2>/dev/null || true
        sed -i "s|^AUTH_PUBLIC_KEY=.*|AUTH_PUBLIC_KEY=\"$PUBLIC_KEY\"|" "$PROJECT_ROOT/.env"
    fi
    echo -e "${GREEN}✓ .env updated with Keycloak public key${NC}\n"
}

if [ "$TEST_TYPE" != "fast" ]; then
    start_keycloak
else
    echo -e "${YELLOW}Fast test mode: skipping Docker services${NC}\n"
fi

cd "$SRC_DIR"

echo -e "${BLUE}Checking Clean Architecture import boundaries...${NC}"
if command -v lint-imports &> /dev/null; then
    if lint-imports; then
        echo -e "${GREEN}✓ Import boundaries OK${NC}\n"
    else
        echo -e "${RED}Import boundary check failed (run: cd src && lint-imports)${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Skipping lint-imports (not installed)${NC}\n"
fi

case $TEST_TYPE in
    fast)
        echo -e "${YELLOW}Running fast tests (unit, integration, api)...${NC}\n"
        PYTEST_MARKER="-m not e2e"
        ;;
    e2e)
        echo -e "${YELLOW}Running E2E tests only...${NC}\n"
        PYTEST_MARKER="-m e2e"
        ;;
    *)
        echo -e "${YELLOW}Running fast + E2E tests...${NC}\n"
        PYTEST_MARKER=""
        ;;
esac

if python -m pytest -v -o addopts= $PYTEST_MARKER; then
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}  All tests passed!                     ${NC}"
    echo -e "${GREEN}========================================${NC}"
    exit 0
else
    echo -e "\n${RED}========================================${NC}"
    echo -e "${RED}  Some tests failed!                    ${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi

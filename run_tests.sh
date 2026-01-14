#!/bin/bash
#
# Automated test runner script for Codeflix Catalog Admin
# 
# This script:
# 1. Starts required services (Keycloak, RabbitMQ) via Docker Compose
# 2. Waits for services to be healthy
# 3. Updates .env with Keycloak public key
# 4. Optionally starts RabbitMQ consumer for consumer-dependent tests
# 5. Runs all pytest tests
# 6. Optionally cleans up containers on exit
#
# Usage:
#   ./run_tests.sh                      # Run all tests (except consumer-dependent)
#   ./run_tests.sh --no-cleanup         # Keep containers running after tests
#   ./run_tests.sh --e2e-only           # Run only E2E tests
#   ./run_tests.sh --unit-only          # Run only unit tests (skip E2E)
#   ./run_tests.sh --with-consumer-tests # Include consumer-dependent E2E tests
#

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
SRC_DIR="$PROJECT_ROOT/src"
CONSUMER_PID=""

# Parse command line arguments
CLEANUP=true
TEST_TYPE="all"
SKIP_CONSUMER_TESTS=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-cleanup)
            CLEANUP=false
            shift
            ;;
        --e2e-only)
            TEST_TYPE="e2e"
            shift
            ;;
        --unit-only)
            TEST_TYPE="unit"
            shift
            ;;
        --with-consumer-tests)
            SKIP_CONSUMER_TESTS=false
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Cleanup function
cleanup() {
    # Stop consumer if running
    if [ -n "$CONSUMER_PID" ]; then
        echo -e "\n${YELLOW}Stopping consumer (PID: $CONSUMER_PID)...${NC}"
        kill $CONSUMER_PID 2>/dev/null || true
        wait $CONSUMER_PID 2>/dev/null || true
    fi
    
    if [ "$CLEANUP" = true ]; then
        echo -e "\n${YELLOW}Cleaning up containers...${NC}"
        cd "$PROJECT_ROOT"
        docker compose down -v 2>/dev/null || true
    else
        echo -e "\n${YELLOW}Keeping containers running (--no-cleanup specified)${NC}"
    fi
}

# Set trap to cleanup on exit (including errors)
trap cleanup EXIT

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Codeflix Catalog Admin Test Runner   ${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Step 1: Start Docker Compose services
echo -e "${BLUE}[1/5] Starting Docker Compose services...${NC}"
cd "$PROJECT_ROOT"

# Check if docker compose is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
    exit 1
fi

# Start services
docker compose up -d

echo -e "${GREEN}✓ Services started${NC}\n"

# Step 2: Wait for Keycloak to be healthy
echo -e "${BLUE}[2/5] Waiting for Keycloak to be ready...${NC}"

KEYCLOAK_MAX_RETRIES=60
KEYCLOAK_RETRY_DELAY=2
KEYCLOAK_URL="http://localhost:8080/realms/codeflix"

for i in $(seq 1 $KEYCLOAK_MAX_RETRIES); do
    if curl -sf "$KEYCLOAK_URL" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Keycloak is ready${NC}\n"
        break
    fi
    
    if [ $i -eq $KEYCLOAK_MAX_RETRIES ]; then
        echo -e "${RED}Error: Keycloak failed to start within timeout${NC}"
        echo -e "${YELLOW}Checking Keycloak logs:${NC}"
        docker compose logs keycloak --tail=50
        exit 1
    fi
    
    echo -e "  Waiting for Keycloak... (attempt $i/$KEYCLOAK_MAX_RETRIES)"
    sleep $KEYCLOAK_RETRY_DELAY
done

# Step 3: Wait for RabbitMQ to be healthy
echo -e "${BLUE}[3/5] Waiting for RabbitMQ to be ready...${NC}"

RABBITMQ_MAX_RETRIES=30
RABBITMQ_RETRY_DELAY=2
RABBITMQ_URL="http://localhost:15672"

for i in $(seq 1 $RABBITMQ_MAX_RETRIES); do
    if curl -sf "$RABBITMQ_URL" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ RabbitMQ is ready${NC}\n"
        break
    fi
    
    if [ $i -eq $RABBITMQ_MAX_RETRIES ]; then
        echo -e "${RED}Error: RabbitMQ failed to start within timeout${NC}"
        echo -e "${YELLOW}Checking RabbitMQ logs:${NC}"
        docker compose logs rabbitmq --tail=50
        exit 1
    fi
    
    echo -e "  Waiting for RabbitMQ... (attempt $i/$RABBITMQ_MAX_RETRIES)"
    sleep $RABBITMQ_RETRY_DELAY
done

# Step 4: Update .env with Keycloak public key
echo -e "${BLUE}[4/6] Updating .env with Keycloak public key...${NC}"

PUBLIC_KEY=$(curl -s "$KEYCLOAK_URL" | jq -r '.public_key')

if [ -z "$PUBLIC_KEY" ] || [ "$PUBLIC_KEY" = "null" ]; then
    echo -e "${RED}Error: Failed to get public key from Keycloak${NC}"
    exit 1
fi

# Update .env file
if [ -f "$PROJECT_ROOT/.env" ]; then
    sed -i "s|^AUTH_PUBLIC_KEY=.*|AUTH_PUBLIC_KEY=\"$PUBLIC_KEY\"|" "$PROJECT_ROOT/.env"
    echo -e "${GREEN}✓ .env updated with Keycloak public key${NC}\n"
else
    echo -e "${YELLOW}Warning: .env file not found, creating it...${NC}"
    echo "AUTH_PUBLIC_KEY=\"$PUBLIC_KEY\"" > "$PROJECT_ROOT/.env"
    echo -e "${GREEN}✓ .env created with Keycloak public key${NC}\n"
fi

# Step 5: Start the RabbitMQ consumer (if needed)
if [ "$SKIP_CONSUMER_TESTS" = false ]; then
    echo -e "${BLUE}[5/6] Starting RabbitMQ consumer...${NC}"

    cd "$SRC_DIR"

    # Start consumer in background and capture PID
    python manage.py startconsumer > /tmp/consumer.log 2>&1 &
    CONSUMER_PID=$!

    # Wait a bit for consumer to initialize
    sleep 2

    # Check if consumer is still running
    if ps -p $CONSUMER_PID > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Consumer started (PID: $CONSUMER_PID)${NC}\n"
    else
        echo -e "${RED}Error: Consumer failed to start${NC}"
        echo -e "${YELLOW}Consumer log:${NC}"
        cat /tmp/consumer.log
        exit 1
    fi
else
    echo -e "${BLUE}[5/6] Skipping consumer (use --with-consumer-tests to enable)...${NC}\n"
fi

# Step 6: Run pytest
echo -e "${BLUE}[6/6] Running tests...${NC}\n"

cd "$SRC_DIR"

# Build pytest command based on test type
PYTEST_ARGS="-v"

# Skip consumer-dependent tests by default
if [ "$SKIP_CONSUMER_TESTS" = true ]; then
    PYTEST_ARGS="$PYTEST_ARGS --ignore=tests_e2e/test_video_conversion_e2e.py"
fi

case $TEST_TYPE in
    "e2e")
        echo -e "${YELLOW}Running E2E tests only...${NC}\n"
        PYTEST_ARGS="$PYTEST_ARGS tests_e2e/"
        ;;
    "unit")
        echo -e "${YELLOW}Running unit tests only (excluding E2E)...${NC}\n"
        PYTEST_ARGS="$PYTEST_ARGS --ignore=tests_e2e/"
        ;;
    *)
        echo -e "${YELLOW}Running all tests...${NC}\n"
        ;;
esac

# Run pytest
if python -m pytest $PYTEST_ARGS; then
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}  All tests passed!                     ${NC}"
    echo -e "${GREEN}========================================${NC}"
    EXIT_CODE=0
else
    echo -e "\n${RED}========================================${NC}"
    echo -e "${RED}  Some tests failed!                    ${NC}"
    echo -e "${RED}========================================${NC}"
    EXIT_CODE=1
fi

exit $EXIT_CODE

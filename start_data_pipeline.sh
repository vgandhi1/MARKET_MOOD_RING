#!/bin/bash
# Market Mood Ring Data Pipeline Startup Script
# This script starts all required infrastructure and producers with proper sequencing
# Version: 2.0

set -e  # Exit on error

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🚀 Starting Market Mood Ring Data Pipeline"
echo "=========================================="
echo ""

# ============================================
# STEP 1: Pre-flight Checks
# ============================================
echo "📋 Step 1/6: Running pre-flight checks..."

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ ERROR: .env file not found!${NC}"
    echo ""
    if [ -f .env.example ]; then
        echo "Creating .env from .env.example template..."
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env and add your FINNHUB_API_KEY${NC}"
        echo ""
        echo "Get your free API key from: https://finnhub.io/"
        echo "Then run this script again."
    else
        echo "Creating basic .env template..."
        echo "FINNHUB_API_KEY=your_key_here" > .env
        echo -e "${YELLOW}⚠️  Please edit .env and add your FINNHUB_API_KEY${NC}"
    fi
    exit 1
fi

# Validate FINNHUB_API_KEY is set
source .env
if [ -z "$FINNHUB_API_KEY" ] || [ "$FINNHUB_API_KEY" = "your_key_here" ] || [ "$FINNHUB_API_KEY" = "your_finnhub_api_key_here" ]; then
    echo -e "${RED}❌ ERROR: FINNHUB_API_KEY is not set in .env file${NC}"
    echo ""
    echo "Please edit .env and add your actual Finnhub API key."
    echo "Get your free API key from: https://finnhub.io/"
    exit 1
fi

# Check if required files exist
echo "   Checking required files..."
REQUIRED_FILES=("docker-compose.yaml" "init.sql" "Dockerfile.flink")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ ERROR: Required file '$file' not found!${NC}"
        exit 1
    fi
done

# Check if required directories exist
REQUIRED_DIRS=("producer" "flink_jobs" "dashboard")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "${RED}❌ ERROR: Required directory '$dir' not found!${NC}"
        exit 1
    fi
done

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ ERROR: Docker is not running!${NC}"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ ERROR: docker-compose is not installed!${NC}"
    echo "Please install docker-compose and try again."
    exit 1
fi

echo -e "   ${GREEN}✅ All pre-flight checks passed${NC}"
echo ""

# ============================================
# STEP 2: Detect Windows Host IP (for Ollama)
# ============================================
echo "📋 Step 2/6: Detecting Windows Host IP for Ollama connection..."

# Try to resolve host.docker.internal first (preferred for WSL2)
if host_ip=$(python3 -c "import socket; print(socket.gethostbyname('host.docker.internal'))" 2>/dev/null); then
    export WINDOWS_HOST_IP=$host_ip
    echo -e "   ${GREEN}✅ Resolved host.docker.internal to: $WINDOWS_HOST_IP${NC}"
else
    # Fallback to default gateway
    export WINDOWS_HOST_IP=$(ip route show | grep default | awk '{print $3}')
    echo -e "   ${YELLOW}⚠️  Using Gateway IP: $WINDOWS_HOST_IP${NC}"
fi

# Validate IP is not empty
if [ -z "$WINDOWS_HOST_IP" ]; then
    echo -e "   ${YELLOW}⚠️  Could not detect Windows Host IP. Using default: 172.17.0.1${NC}"
    export WINDOWS_HOST_IP="172.17.0.1"
fi

echo ""

# ============================================
# STEP 3: Clean up old containers (if any)
# ============================================
echo "📋 Step 3/6: Checking for old containers..."

# Check for containers with corrupted metadata
CORRUPTED_CONTAINERS=$(docker ps -a --filter "name=market_" --format "{{.Names}}" | grep -E "^[a-f0-9]{12}_market_" || true)

if [ ! -z "$CORRUPTED_CONTAINERS" ]; then
    echo -e "   ${YELLOW}⚠️  Found containers with corrupted metadata. Cleaning up...${NC}"
    echo "$CORRUPTED_CONTAINERS" | xargs docker rm -f 2>/dev/null || true
    echo -e "   ${GREEN}✅ Cleanup complete${NC}"
else
    echo -e "   ${GREEN}✅ No cleanup needed${NC}"
fi

echo ""

# ============================================
# STEP 4: Start Infrastructure & Producers
# ============================================
echo "📋 Step 4/6: Starting all services (Infrastructure + Producers)..."
echo "   This includes: Kafka, PostgreSQL, Flink, Dashboard, and all Producers"
echo ""

# Try to start services, handle network recreation if needed
if ! docker-compose --profile producers up -d 2>&1 | tee /tmp/compose_output.txt | grep -q "needs to be recreated"; then
    # Success or other error
    if grep -q "ERROR" /tmp/compose_output.txt; then
        # Check if it's the network recreation issue
        if grep -q "needs to be recreated" /tmp/compose_output.txt; then
            echo -e "   ${YELLOW}⚠️  Network configuration changed. Recreating...${NC}"
            docker-compose --profile producers down > /dev/null 2>&1
            sleep 2
            echo "   Restarting with fresh network..."
            docker-compose --profile producers up -d
        else
            # Some other error
            cat /tmp/compose_output.txt
            exit 1
        fi
    fi
else
    # Network needs recreation
    echo -e "   ${YELLOW}⚠️  Network configuration changed. Recreating...${NC}"
    docker-compose --profile producers down > /dev/null 2>&1
    sleep 2
    echo "   Restarting with fresh network..."
    docker-compose --profile producers up -d
fi

rm -f /tmp/compose_output.txt

echo ""
echo -e "   ${GREEN}✅ Docker containers started${NC}"
echo ""

# ============================================
# STEP 5: Wait for Services to be Healthy
# ============================================
echo "📋 Step 5/6: Waiting for services to become healthy..."
echo ""

# Wait for Kafka
echo "   Waiting for Kafka..."
RETRY=0
MAX_RETRIES=30
while [ $RETRY -lt $MAX_RETRIES ]; do
    if docker exec market_kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Kafka is ready${NC}"
        break
    fi
    RETRY=$((RETRY+1))
    echo -n "."
    sleep 2
done

if [ $RETRY -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ ERROR: Kafka failed to start within timeout${NC}"
    echo "Check logs: docker logs market_kafka"
    exit 1
fi

# Wait for PostgreSQL
echo "   Waiting for PostgreSQL..."
RETRY=0
while [ $RETRY -lt $MAX_RETRIES ]; do
    if docker exec market_postgres pg_isready -U market_user -d market_mood > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ PostgreSQL is ready${NC}"
        break
    fi
    RETRY=$((RETRY+1))
    echo -n "."
    sleep 2
done

if [ $RETRY -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ ERROR: PostgreSQL failed to start within timeout${NC}"
    echo "Check logs: docker logs market_postgres"
    exit 1
fi

# Wait for Flink JobManager
echo "   Waiting for Flink JobManager..."
RETRY=0
while [ $RETRY -lt $MAX_RETRIES ]; do
    if docker exec market_jobmanager ./bin/flink list > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Flink JobManager is ready${NC}"
        break
    fi
    RETRY=$((RETRY+1))
    echo -n "."
    sleep 2
done

if [ $RETRY -eq $MAX_RETRIES ]; then
    echo -e "${RED}❌ ERROR: Flink JobManager failed to start within timeout${NC}"
    echo "Check logs: docker logs market_jobmanager"
    exit 1
fi

# Check producer statuses
echo ""
echo "   Checking producer statuses..."
sleep 3  # Give producers a moment to start

PRODUCER_STATUS=$(docker ps --filter "name=market_" --format "{{.Names}}\t{{.Status}}")
echo "$PRODUCER_STATUS" | grep -E "(news_producer|price_producer|price_consumer|rag_ingest)" || true

echo ""

# ============================================
# STEP 6: Submit Flink Job
# ============================================
echo "📋 Step 6/6: Checking Flink job status..."

# Check if Flink sentiment job is already running
FLINK_JOBS=$(docker exec market_jobmanager ./bin/flink list 2>/dev/null | grep "flink_sentiment" | wc -l)

if [ "$FLINK_JOBS" -eq "0" ]; then
    echo "   ⚠️  Flink job not running. Submitting..."
    
    if docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py 2>&1 | grep -q "Job has been submitted"; then
        echo -e "   ${GREEN}✅ Flink sentiment job submitted successfully${NC}"
    else
        echo -e "   ${YELLOW}⚠️  Flink job submission may have failed. Check logs.${NC}"
        echo "   Check logs: docker logs market_jobmanager"
    fi
else
    echo -e "   ${GREEN}✅ Flink sentiment job is already running${NC}"
fi

echo ""

# ============================================
# FINAL STATUS & ACCESS INFO
# ============================================
echo ""
echo "================================================================"
echo -e "${GREEN}✅ Pipeline is fully active!${NC}"
echo "================================================================"
echo ""

# Verify actual container states
echo "📊 Service Status:"
docker ps --filter "name=market_" --format "   {{.Names}}: {{.Status}}" | sort

echo ""
echo "🔗 Access Points:"
echo "   📊 Dashboard:    http://localhost:8502"
echo "   🌊 Flink UI:     http://localhost:8081"
echo "   🗄️  PostgreSQL:   localhost:5432 (user: market_user, db: market_mood)"
echo "   📨 Kafka:        localhost:9092"

echo ""
echo "📋 Useful Commands:"
echo "   View logs:       docker-compose logs -f news-producer price-producer"
echo "   Stop pipeline:   docker-compose --profile producers down"
echo "   Restart service: docker-compose restart <service-name>"
echo "   Check status:    docker ps --filter 'name=market_'"

echo ""
echo "📚 Documentation:"
echo "   Getting Started: docs/GETTING_STARTED.md"
echo "   Troubleshooting: docs/TROUBLESHOOTING.md"
echo "   Flink Job Guide: docs/FLINK_JOB_GUIDE.md"

echo ""
echo "🌊 Flink Job Management:"
echo "   Check status:    docker exec market_jobmanager ./bin/flink list"
echo "   View Flink UI:   http://localhost:8081"
echo "   Submit manually: docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py"

echo ""
echo "🎉 Happy analyzing!"
echo ""

#!/bin/bash
# Start Data Pipeline for Phase 1
# This script starts all required producers and consumers

set -e

echo "🚀 Starting Market Mood Ring Data Pipeline"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Creating .env template..."
    echo "FINNHUB_API_KEY=your_key_here" > .env
    echo "Please edit .env and add your FINNHUB_API_KEY"
    exit 1
fi

# Detect Windows Host IP for WSL2
# We try to resolve host.docker.internal first (LAN IP), as it's often more permissive than the WSL gateway
echo "🔍 Detecting Windows Host IP..."
if host_ip=$(python3 -c "import socket; print(socket.gethostbyname('host.docker.internal'))" 2>/dev/null); then
    export WINDOWS_HOST_IP=$host_ip
    echo "   ✅ Resolved host.docker.internal to: $WINDOWS_HOST_IP"
else
    # Fallback to gateway if resolution fails
    export WINDOWS_HOST_IP=$(ip route show | grep default | awk '{print $3}')
    echo "   ⚠️  Could not resolve host.docker.internal, using Gateway IP: $WINDOWS_HOST_IP"
fi

echo "1. Starting/Updating all services (Infrastructure + Producers)..."
# We start everything at once to avoid network inconsistency issues
docker-compose --profile producers up -d

echo "⏳ Waiting for services to stabilize (15s)..."
sleep 15

# Check if Flink job is running
echo "2. Checking Flink job status..."
# Use wc -l to count lines matching the job name
FLINK_JOBS=$(docker exec market_jobmanager ./bin/flink list 2>/dev/null | grep "flink_sentiment" | wc -l)

if [ "$FLINK_JOBS" -eq "0" ]; then
    echo "   ⚠️  Flink job not submitted"
    echo "   Submitting Flink job..."
    # Removed -it to allow non-interactive execution
    docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
    echo ""
else
    echo "   ✅ Flink job is running"
    echo ""
fi

echo "✅ Pipeline is fully active!"
echo "   - News Producer: Running"
echo "   - Price Producer: Running"
echo "   - Price Consumer: Running"
echo "   - RAG Ingest: Running"
echo ""
echo "📋 Monitor logs with:"
echo "   docker-compose logs -f news-producer price-producer"
echo ""
echo "📊 Dashboard: http://localhost:8502"
echo ""

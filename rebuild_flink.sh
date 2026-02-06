#!/bin/bash
# Rebuild Flink containers with Python symlink fix

set -e

echo "🔧 Rebuilding Flink containers with Python fix..."
echo ""

# Stop Flink services
echo "1. Stopping Flink services..."
docker-compose stop jobmanager taskmanager

# Rebuild containers
echo ""
echo "2. Rebuilding containers (this may take a few minutes)..."
docker-compose build jobmanager taskmanager

# Start services
echo ""
echo "3. Starting Flink services..."
docker-compose up -d jobmanager taskmanager

# Wait for services to be ready
echo ""
echo "4. Waiting for services to be ready..."
sleep 10

# Verify python symlink exists
echo ""
echo "5. Verifying python symlink..."
if docker exec market_taskmanager which python > /dev/null 2>&1; then
    echo "✅ Python symlink exists!"
    docker exec market_taskmanager which python
    echo ""
    echo "6. You can now submit the Flink job:"
    echo "   docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py"
else
    echo "❌ Python symlink not found. Check Dockerfile.flink"
    exit 1
fi

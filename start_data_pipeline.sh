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

# Check if containers are running
echo "1. Checking infrastructure..."
if ! docker ps | grep -q market_postgres; then
    echo "❌ PostgreSQL not running. Starting infrastructure..."
    docker-compose up -d
    echo "⏳ Waiting for services to be ready..."
    sleep 10
fi

echo "✅ Infrastructure is running"
echo ""

# Check if price_consumer is already running
if docker ps | grep -q price_consumer; then
    echo "⚠️  Price consumer is already running"
else
    echo "2. Starting price consumer (writes prices to database)..."
    echo "   Run this in a separate terminal:"
    echo "   docker-compose run --rm producer python price_consumer.py"
    echo ""
fi

# Check if Flink job is running
echo "3. Checking Flink job status..."
FLINK_JOBS=$(docker exec market_jobmanager ./bin/flink list 2>/dev/null | grep -c "flink_sentiment" || echo "0")

if [ "$FLINK_JOBS" -eq "0" ]; then
    echo "   ⚠️  Flink job not submitted"
    echo "   Submitting Flink job..."
    docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
    echo ""
else
    echo "   ✅ Flink job is running"
    echo ""
fi

echo "4. Starting producers..."
echo ""
echo "📋 Next Steps:"
echo "=============="
echo ""
echo "Open 3 separate terminals and run:"
echo ""
echo "Terminal 1 - News Producer:"
echo "  docker-compose run --rm producer python news_producer.py"
echo ""
echo "Terminal 2 - Price Producer:"
echo "  docker-compose run --rm producer python price_producer.py"
echo ""
echo "Terminal 3 - Price Consumer:"
echo "  docker-compose run --rm producer python price_consumer.py"
echo ""
echo "After 1-2 minutes, check dashboard: http://localhost:8502"
echo ""
echo "To verify data:"
echo "  docker exec market_postgres psql -U market_user -d market_mood -c 'SELECT COUNT(*) FROM price_log;'"
echo "  docker exec market_postgres psql -U market_user -d market_mood -c 'SELECT COUNT(*) FROM sentiment_log;'"
echo ""

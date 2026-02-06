#!/bin/bash
# Market Mood Ring - Setup Script
# Creates virtual environment using UV and installs dependencies

set -e  # Exit on error

echo "🚀 Market Mood Ring - Setup Script"
echo "===================================="
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "❌ UV is not installed!"
    echo "📦 Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ UV installed. Please restart your terminal or run: source ~/.cargo/env"
    exit 1
fi

echo "✅ UV is installed"
echo ""

# Create virtual environment using UV
echo "📦 Creating virtual environment with UV..."
uv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing Python packages from requirements.txt..."
uv pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Create .env file with your FINNHUB_API_KEY:"
echo "   echo 'FINNHUB_API_KEY=your_key_here' > .env"
echo ""
echo "2. Activate virtual environment (if not already active):"
echo "   source .venv/bin/activate"
echo ""
echo "3. Start Docker containers:"
echo "   docker-compose up -d --build"
echo ""
echo "4. Start Docker containers:"
echo "   docker-compose up -d --build"
echo ""
echo "5. Run producers (in separate terminals):"
echo "   docker-compose run --rm producer python news_producer.py"
echo "   docker-compose run --rm producer python price_producer.py"
echo "   docker-compose run --rm producer python price_consumer.py"
echo ""
echo "6. Submit Flink job:"
echo "   docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py"
echo ""

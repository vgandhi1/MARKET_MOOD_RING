# 🚀 UV Environment Setup Guide

## What is UV?

**UV** is a fast Python package installer and resolver written in Rust. It's a modern alternative to pip/conda.

## Installation

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv

# Or via homebrew (macOS)
brew install uv
```

## Setting Up Environment Variables with UV

### Option 1: Using UV's Environment Variable Support

UV can manage environment variables through `.env` files or directly:

```bash
# Create .env file (recommended)
uv run --env-file .env python script.py

# Or set inline
uv run --env FINNHUB_API_KEY=your_key python script.py
```

### Option 2: Using UV with .env File

1. **Create `.env` file:**
   ```bash
   # .env file
   FINNHUB_API_KEY=your_finnhub_api_key_here
   STOCK_SYMBOLS=AAPL,MSFT,TSLA
   KAFKA_BOOTSTRAP_SERVERS=kafka:29092
   POSTGRES_HOST=postgres
   POSTGRES_DB=market_mood
   POSTGRES_USER=market_user
   POSTGRES_PASSWORD=market_password
   ```

2. **Load environment variables:**
   ```bash
   # UV automatically loads .env file
   uv run python producer/news_producer.py
   ```

### Option 3: Using UV's Virtual Environment

```bash
# Create virtual environment with UV
uv venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Set environment variables
export FINNHUB_API_KEY=your_key
export STOCK_SYMBOLS=AAPL,MSFT,TSLA

# Run scripts
python producer/news_producer.py
```

## Complete UV Setup for Market Mood Ring

### Step 1: Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Create .env File
```bash
cat > .env << EOF
FINNHUB_API_KEY=your_finnhub_api_key_here
STOCK_SYMBOLS=AAPL,MSFT,TSLA,GOOGL,AMZN
KAFKA_BOOTSTRAP_SERVERS=kafka:29092
POSTGRES_HOST=postgres
POSTGRES_DB=market_mood
POSTGRES_USER=market_user
POSTGRES_PASSWORD=market_password
EOF
```

### Step 3: Install Dependencies
```bash
# Using UV
uv pip install -r requirements.txt

# Or create venv and install
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Step 4: Run Scripts
```bash
# With UV (loads .env automatically) - from project root
uv run python producer/news_producer.py

# Or with activated venv - from project root
source .venv/bin/activate
python producer/news_producer.py

# In Docker container (files mounted to /app/)
docker-compose run --rm producer python news_producer.py
```

## UV Advantages

✅ **Fast:** 10-100x faster than pip  
✅ **Reliable:** Better dependency resolution  
✅ **Modern:** Built with Rust for performance  
✅ **Compatible:** Works with existing pip packages  
✅ **Environment Support:** Built-in .env file support  

## Docker vs UV

- **Docker:** Use for containerized deployment (production)
- **UV:** Use for local development and testing

Both can coexist! Use UV for local dev, Docker for deployment.

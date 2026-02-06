# 🚀 Phase 1: Quick Start Guide

## Overview

Phase 1 focuses on building and validating the **ETL Pipeline with Sentiment Analysis** using NLTK. This phase does NOT include RAG or AI chat features (those come in Phase 2).

## ✅ Phase 1 Components

- ✅ **Kafka** - Message streaming
- ✅ **PostgreSQL** - Data storage
- ✅ **Flink** - Stream processing with NLTK sentiment analysis
- ✅ **Producers** - News and price data ingestion
- ✅ **Dashboard** - Live charts and sentiment tables
- ❌ **Ollama** - Commented out (Phase 2)
- ❌ **RAG Pipeline** - Commented out (Phase 2)
- ❌ **AI Chat** - Commented out (Phase 2)

## 🚀 Quick Start

### 1. Setup Python Environment (UV)

**Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Create virtual environment and install dependencies:**
```bash
# Create venv
uv venv

# Activate venv
source .venv/bin/activate  # Linux/Mac

# Install packages
uv pip install -r requirements.txt
```

**Or use the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Setup Environment Variables

Create `.env` file:
```bash
FINNHUB_API_KEY=your_actual_api_key_here
```

### 3. Launch Infrastructure (Phase 1 Only)

Start Phase 1 services:
```bash
docker-compose up -d --build
```

This starts:
- ✅ Zookeeper
- ✅ Kafka
- ✅ PostgreSQL
- ✅ Flink (JobManager + TaskManager)
- ✅ Streamlit Dashboard
- ❌ Ollama (commented out)

### 3. Start Data Pipelines

**Terminal A - News Producer:**
```bash
docker-compose run --rm producer python news_producer.py
```

**Terminal B - Price Producer:**
```bash
docker-compose run --rm producer python price_producer.py
```

**Terminal C - Price Consumer:**
```bash
docker-compose run --rm producer python price_consumer.py
```

### 4. Submit Flink Sentiment Job

```bash
docker exec -it vibe_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

### 5. Access Dashboard

Open browser: **http://localhost:8502**

You should see:
- 📊 Live price charts
- 📈 Sentiment score tables

## ✅ Phase 1 Validation Checklist

### Data Ingestion
- [ ] News producer fetching and publishing to Kafka `stock_news` topic
- [ ] Price producer fetching and publishing to Kafka `stock_prices` topic
- [ ] Price consumer writing to PostgreSQL `price_log` table

### Stream Processing
- [ ] Flink job running successfully (check http://localhost:8081)
- [ ] Sentiment scores appearing in `sentiment_log` table
- [ ] Sentiment scores are between -1.0 and 1.0

### Dashboard
- [ ] Dashboard accessible at http://localhost:8502
- [ ] Price charts displaying data
- [ ] Sentiment scores table showing data
- [ ] Can filter by symbol

### Database Verification

```bash
# Connect to database
docker exec -it vibe_postgres psql -U vibe_user -d crypto_vibes

# Check tables
\dt

# Check price data
SELECT COUNT(*) FROM price_log;
SELECT * FROM price_log ORDER BY timestamp DESC LIMIT 10;

# Check sentiment data
SELECT COUNT(*) FROM sentiment_log;
SELECT symbol, headline, sentiment_score FROM sentiment_log ORDER BY created_at DESC LIMIT 10;
```

## 🔍 Monitoring

### Check Kafka Topics
```bash
docker exec -it vibe_kafka kafka-topics --list --bootstrap-server localhost:9092
docker exec -it vibe_kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic stock_news --from-beginning
```

### Check Flink Job
- Visit: http://localhost:8081
- Check "Running Jobs" section
- View job metrics and logs

### Check Logs
```bash
# Producer logs
docker-compose logs producer

# Flink logs
docker-compose logs jobmanager
docker-compose logs taskmanager

# Kafka logs
docker-compose logs kafka

# Dashboard logs
docker-compose logs dashboard
```

## 🐛 Common Issues

### No Data in Dashboard
1. Check if producers are running: `docker-compose ps`
2. Check Kafka topics have messages
3. Check Flink job is running
4. Verify database has data: `SELECT COUNT(*) FROM price_log;`

### Flink Job Not Starting
1. Check Flink logs: `docker-compose logs jobmanager`
2. Verify NLTK data is downloaded in Flink container
3. Check Kafka connectivity from Flink

### Producer Connection Errors
1. Verify Kafka is healthy: `docker-compose ps kafka`
2. Check network: `docker network ls`
3. Verify FINNHUB_API_KEY is set

## 📊 Expected Data Flow

```
Finnhub API
    ↓
Producers (news_producer.py, price_producer.py)
    ↓
Kafka Topics (stock_news, stock_prices)
    ↓
Flink Sentiment Job (flink_sentiment.py)
    ↓
PostgreSQL (sentiment_log table)
    ↓
Price Consumer (price_consumer.py)
    ↓
PostgreSQL (price_log table)
    ↓
Streamlit Dashboard (app.py)
```

## 🎯 Phase 1 Success Criteria

- ✅ All services running without errors
- ✅ Data flowing through entire pipeline
- ✅ Sentiment scores calculated correctly
- ✅ Dashboard displaying live data
- ✅ System stable for extended period (1+ hours)

## 🔮 Next Steps (Phase 2)

Once Phase 1 is validated:
1. Uncomment Ollama in `docker-compose.yaml`
2. Uncomment `financial_knowledge` table in `init.sql`
3. Uncomment AI Analyst page in `dashboard/app.py`
4. Start RAG ingestion: `docker-compose run producer python rag_ingest.py`
5. Initialize Ollama: `docker exec -it vibe_ollama ollama run llama3`

See `PHASE_PLANNING.md` for detailed phase information.

---

**Current Phase:** Phase 1 - ETL with Sentiment Analysis  
**Status:** Ready for testing

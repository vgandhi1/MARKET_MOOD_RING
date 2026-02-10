# 🚀 Phase 1: Quick Start Guide

**⚠️ Note:** This is an older guide. For the most up-to-date setup instructions, see **[GETTING_STARTED.md](../GETTING_STARTED.md)**.

## Overview

Phase 1 focuses on building and validating the **ETL Pipeline with Sentiment Analysis** using NLTK. This phase does NOT include AI chat features (those come when using Ollama).

## ✅ Phase 1 Components

- ✅ **Kafka** - Message streaming
- ✅ **PostgreSQL** - Data storage
- ✅ **Flink** - Stream processing with NLTK sentiment analysis
- ✅ **Producers** - News and price data ingestion
- ✅ **Dashboard** - Live charts and sentiment tables
- ⚠️ **Ollama** - Optional (for AI Analyst feature)
- ⚠️ **RAG Pipeline** - Optional (for AI context)

---

## 🚀 Recommended Quick Start (2026 Method)

### ✅ Use the Startup Script (Easiest)

```bash
# 1. Create .env file
cp .env.example .env
nano .env  # Add your FINNHUB_API_KEY

# 2. Run the startup script (handles everything!)
./start_data_pipeline.sh
```

**That's it!** The script automatically:
- ✅ Validates environment and files
- ✅ Detects Windows Host IP (for Ollama)
- ✅ Starts all services with health checks
- ✅ Submits Flink job
- ✅ Shows detailed status

**Access Dashboard:** http://localhost:8502

---

## 📋 Manual Setup (Alternative)

### 1. Setup Environment Variables

Create `.env` file:
```bash
cp .env.example .env
# Edit and add: FINNHUB_API_KEY=your_actual_api_key_here
```

### 2. Start All Services

```bash
# Start infrastructure and producers (using profiles)
docker-compose --profile producers up -d
```

This starts:
- ✅ Kafka
- ✅ PostgreSQL
- ✅ Flink (JobManager + TaskManager)
- ✅ News Producer
- ✅ Price Producer
- ✅ Price Consumer
- ✅ RAG Ingest
- ✅ Dashboard

### 3. Submit Flink Sentiment Job

```bash
# Wait 30 seconds for Flink to be ready, then:
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

**⚠️ Important:** Use `market_jobmanager` (not `vibe_jobmanager`)

### 4. Access Dashboard

Open browser: **http://localhost:8502**

You should see:
- 📊 Live price charts
- 📈 Sentiment score tables

---

## ✅ Phase 1 Validation Checklist

### Data Ingestion
- [ ] News producer fetching and publishing to Kafka `stock_news` topic
- [ ] Price producer fetching and publishing to Kafka `stock_prices` topic
- [ ] Price consumer writing to PostgreSQL `stock_prices` table

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
# Connect to database (correct container name!)
docker exec -it market_postgres psql -U market_user -d market_mood

# Check tables
\dt

# Check price data
SELECT COUNT(*) FROM stock_prices;
SELECT * FROM stock_prices ORDER BY timestamp DESC LIMIT 10;

# Check sentiment data
SELECT COUNT(*) FROM sentiment_log;
SELECT symbol, headline, sentiment_score FROM sentiment_log ORDER BY timestamp DESC LIMIT 10;

# Exit
\q
```

---

## 🔍 Monitoring

### Check Kafka Topics
```bash
# List topics
docker exec market_kafka kafka-topics --list --bootstrap-server localhost:9092

# Consume from stock_news topic
docker exec market_kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic stock_news --from-beginning --max-messages 5
```

### Check Flink Job
- Visit: http://localhost:8081
- Check "Running Jobs" section
- View job metrics and logs

### Check Container Logs
```bash
# News producer
docker logs market_news_producer --tail 20

# Price producer
docker logs market_price_producer --tail 20

# Flink
docker logs market_jobmanager --tail 20
docker logs market_taskmanager --tail 20

# Kafka
docker logs market_kafka --tail 20

# Dashboard
docker logs market_dashboard --tail 20
```

---

## 🐛 Common Issues

### No Data in Dashboard
**Solution:**
1. Wait 2-3 minutes for initial data collection
2. Check if producers are running: `docker ps | grep producer`
3. Verify database has data: `SELECT COUNT(*) FROM stock_prices;`
4. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for comprehensive guide

### Flink Job Not Starting
**Solution:**
```bash
# Check if job is running
docker exec market_jobmanager ./bin/flink list

# If not running, submit it
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

See [FLINK_JOB_GUIDE.md](../FLINK_JOB_GUIDE.md) for detailed instructions.

### Producer Connection Errors
**Solution:**
1. Verify Kafka is healthy: `docker ps | grep kafka`
2. Check FINNHUB_API_KEY is set: `grep FINNHUB .env`
3. Restart with startup script: `./start_data_pipeline.sh`

---

## 📊 Expected Data Flow

```
Finnhub API
    ↓
Producers (news_producer.py, price_producer.py)
    ↓
Kafka Topics (stock_news, stock_prices)
    ↓
Consumers (Flink job, price_consumer.py)
    ↓
PostgreSQL (sentiment_log, stock_prices tables)
    ↓
Streamlit Dashboard (app.py)
```

---

## 🎯 Phase 1 Success Criteria

- ✅ All services running without errors
- ✅ Data flowing through entire pipeline
- ✅ Sentiment scores calculated correctly
- ✅ Dashboard displaying live data
- ✅ System stable for extended period (1+ hours)

---

## 🔮 Adding Ollama (Optional)

To enable the AI Analyst feature:

1. **Install Ollama on Windows**
   ```powershell
   # Download from: https://ollama.com/
   ```

2. **Configure network access**
   ```powershell
   # Set environment variable
   setx OLLAMA_HOST "0.0.0.0:11434"
   
   # Add firewall rule (as Administrator)
   New-NetFirewallRule -DisplayName "Ollama Allow" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
   ```

3. **Pull model**
   ```powershell
   ollama pull llama3
   ```

4. **Restart pipeline**
   ```bash
   ./start_data_pipeline.sh
   ```

5. **Access AI Analyst**
   - Dashboard: http://localhost:8502
   - Click "💬 AI Analyst" tab

See [LLM_API_INTEGRATION.md](LLM_API_INTEGRATION.md) for complete guide.

---

## 📚 Related Documentation

- **[GETTING_STARTED.md](../GETTING_STARTED.md)** - ⭐ **Recommended** Complete modern guide
- **[TROUBLESHOOTING.md](../TROUBLESHOOTING.md)** - Comprehensive troubleshooting
- **[FLINK_JOB_GUIDE.md](../FLINK_JOB_GUIDE.md)** - Flink job management
- **[DOCKER_VS_SCRIPT_GUIDE.md](../DOCKER_VS_SCRIPT_GUIDE.md)** - Command reference
- **[DOCUMENTATION_INDEX.md](../DOCUMENTATION_INDEX.md)** - All documentation

---

**Current Phase:** Phase 1 - ETL with Sentiment Analysis  
**Status:** Production Ready  
**Last Updated:** February 2026

**For most up-to-date instructions, use: [GETTING_STARTED.md](../GETTING_STARTED.md)**

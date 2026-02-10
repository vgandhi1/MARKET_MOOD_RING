# 🔍 Dashboard Shows No Data - Troubleshooting Guide

**⚠️ Note:** For comprehensive troubleshooting, see **[TROUBLESHOOTING.md](../TROUBLESHOOTING.md)** (master guide with 35+ issues).

---

## Problem

Dashboard shows:
- "No price data available. Start the price producer to see live data."
- "No sentiment data available. Start the Flink job to see sentiment analysis."

## Root Cause

**No data in database** - The data pipeline isn't running or data isn't flowing through.

## Data Flow Required

```
Finnhub API
    ↓
Producers (news_producer.py, price_producer.py)
    ↓
Kafka Topics (stock_news, stock_prices)
    ↓
Consumers (price_consumer.py, Flink job)
    ↓
PostgreSQL (stock_prices, sentiment_log tables)
    ↓
Dashboard (displays data)
```

---

## ✅ Quick Fix (Recommended)

**Use the startup script - handles everything automatically:**

```bash
# Stop everything
docker-compose --profile producers down

# Start with automated script
./start_data_pipeline.sh

# Wait 2-3 minutes for data collection
# Then refresh dashboard: http://localhost:8502
```

---

## Step-by-Step Troubleshooting

### Step 1: Check Database Tables

```bash
# Check if tables exist
docker exec market_postgres psql -U market_user -d market_mood -c "\dt"

# Check row counts
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM stock_prices;"
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM sentiment_log;"
```

**Expected:** Tables should exist. May have 0 rows if pipeline just started.

### Step 2: Check Kafka Topics Have Data

```bash
# List topics
docker exec market_kafka kafka-topics --list --bootstrap-server localhost:9092

# Check stock_prices topic
docker exec market_kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic stock_prices --from-beginning --max-messages 5 --timeout-ms 10000

# Check stock_news topic
docker exec market_kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic stock_news --from-beginning --max-messages 5 --timeout-ms 10000
```

**Expected:** Should see JSON messages if producers are running.

### Step 3: Verify Producers Are Running

```bash
# Check running containers
docker ps --filter "name=market_" | grep producer

# Should see:
# market_news_producer
# market_price_producer
# market_price_consumer
# market_rag_ingest

# Check producer logs
docker logs market_news_producer --tail 20
docker logs market_price_producer --tail 20
```

**Expected:** Should see logs like:
- "✅ Published: AAPL @ $150.25"
- "✅ Published: AAPL - Headline..."

### Step 4: Verify Price Consumer Is Running

The `price_consumer.py` must be running to write prices to database:

```bash
# Check if price_consumer is running
docker ps | grep price_consumer

# Check logs
docker logs market_price_consumer --tail 20
```

**Expected:** Should see logs like "✅ Stored: AAPL @ $150.25"

**If not running:** The startup script starts it automatically. If using manual method:
```bash
docker-compose restart price-consumer
```

### Step 5: Verify Flink Job Is Running

```bash
# Check Flink dashboard
# Visit: http://localhost:8081

# Or check via command line
docker exec market_jobmanager ./bin/flink list
```

**Expected:** Should see `flink_sentiment` job with status RUNNING.

**If not running:**
```bash
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

See [FLINK_JOB_GUIDE.md](../FLINK_JOB_GUIDE.md) for detailed instructions.

---

## Complete Setup Checklist

### ✅ Infrastructure Running
- [ ] `docker ps` shows all services up
- [ ] Kafka is healthy
- [ ] PostgreSQL is healthy
- [ ] Flink JobManager and TaskManager are running

### ✅ Data Producers Running
- [ ] `market_news_producer` - Up
- [ ] `market_price_producer` - Up  
- [ ] `market_price_consumer` - Up
- [ ] `market_rag_ingest` - Up

### ✅ Flink Job Submitted
- [ ] Flink job running: `docker exec market_jobmanager ./bin/flink list`
- [ ] Job shows as "RUNNING" in Flink dashboard (http://localhost:8081)

### ✅ Data Flowing
- [ ] Kafka topics have messages
- [ ] Database tables have rows
- [ ] Dashboard shows data

---

## Common Issues

### Issue 1: Used docker-compose without startup script

**Symptom:** Producers exit with `NoBrokersAvailable` error

**Fix:** Use the startup script which handles proper sequencing:
```bash
docker-compose --profile producers down
./start_data_pipeline.sh
```

### Issue 2: Flink Job Not Submitted

**Symptom:** Kafka has news, but `sentiment_log` table is empty

**Fix:** Submit Flink job (startup script does this automatically):
```bash
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

### Issue 3: API Key Missing

**Symptom:** Producers fail with "FINNHUB_API_KEY not set"

**Fix:** 
```bash
# Create/edit .env file
nano .env
# Add: FINNHUB_API_KEY=your_actual_key_from_finnhub

# Restart
./start_data_pipeline.sh
```

### Issue 4: Wrong Container Names

**Symptom:** Commands fail with "No such container: vibe_*"

**Fix:** Use correct container names:
- ✅ `market_jobmanager` (NOT `vibe_jobmanager`)
- ✅ `market_postgres` (NOT `vibe_postgres`)  
- ✅ `market_kafka` (NOT `vibe_kafka`)
- ✅ Database: `market_mood` (NOT `crypto_vibes`)

### Issue 5: Just Started, No Data Yet

**Symptom:** Everything running but no data

**Fix:** Wait 2-3 minutes for initial data collection:
- 0-60 seconds: Producers fetch data
- 60-120 seconds: Data processed
- 2+ minutes: Dashboard shows data

---

## Verification Queries

```sql
-- Connect to database
docker exec -it market_postgres psql -U market_user -d market_mood

-- Check recent prices
SELECT symbol, price, timestamp 
FROM stock_prices 
ORDER BY timestamp DESC 
LIMIT 10;

-- Check recent sentiment
SELECT symbol, headline, sentiment_score, timestamp
FROM sentiment_log 
ORDER BY timestamp DESC 
LIMIT 10;

-- Check data counts
SELECT 
    (SELECT COUNT(*) FROM stock_prices) as price_count,
    (SELECT COUNT(*) FROM sentiment_log) as sentiment_count;

-- Exit
\q
```

---

## Expected Timeline

- **0-30 seconds:** Producers start fetching data → Kafka topics get messages
- **30-60 seconds:** Price consumer writes to database → `stock_prices` has rows
- **60-120 seconds:** Flink processes news → `sentiment_log` has rows
- **2+ minutes:** Dashboard shows data

---

## Related Documentation

- **[TROUBLESHOOTING.md](../TROUBLESHOOTING.md)** - Master guide (35+ issues)
- **[GETTING_STARTED.md](../GETTING_STARTED.md)** - Complete setup guide
- **[FLINK_JOB_GUIDE.md](../FLINK_JOB_GUIDE.md)** - Flink job management
- **[DOCKER_VS_SCRIPT_GUIDE.md](../DOCKER_VS_SCRIPT_GUIDE.md)** - Command reference

---

**If still no data after following all steps:**
1. Check [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for comprehensive guide
2. Verify producer logs for errors: `docker logs market_news_producer`
3. Check Flink logs: `docker logs market_jobmanager`
4. Verify connectivity: `docker network inspect market_mood_ring_market_network`

---

*Last Updated: February 2026*  
*For comprehensive troubleshooting: [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)*

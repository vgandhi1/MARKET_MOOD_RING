# 🔍 Dashboard Shows No Data - Troubleshooting Guide

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
PostgreSQL (price_log, sentiment_log)
    ↓
Dashboard (displays data)
```

## Step-by-Step Troubleshooting

### Step 1: Check Database Tables

```bash
# Check if tables exist
docker exec market_postgres psql -U market_user -d market_mood -c "\dt"

# Check row counts
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM price_log;"
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM sentiment_log;"
```

**Expected:** Tables should exist, but may have 0 rows if pipeline isn't running.

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
docker ps | grep producer

# Check producer logs
docker logs <producer-container-name> | tail -20
```

**Expected:** Should see logs like:
- "✅ Published: AAPL @ $150.25"
- "✅ Published: AAPL - Headline..."

### Step 4: Verify Price Consumer Is Running

The `price_consumer.py` must be running to write prices to database:

```bash
# Check if price_consumer is running
docker ps | grep price_consumer

# If not running, start it:
docker-compose run --rm producer python price_consumer.py
```

**Expected:** Should see logs like "✅ Stored: AAPL @ $150.25"

### Step 5: Verify Flink Job Is Running

```bash
# Check Flink dashboard
# Visit: http://localhost:8081

# Or check via command line
docker exec market_jobmanager ./bin/flink list
```

**Expected:** Should see `flink_sentiment.py` job running.

**If not running, submit it:**
```bash
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

## Complete Setup Checklist

### ✅ Infrastructure Running
- [ ] `docker-compose ps` shows all services up
- [ ] Kafka is healthy
- [ ] PostgreSQL is healthy
- [ ] Flink JobManager and TaskManager are running

### ✅ Data Producers Running
- [ ] News producer running: `docker-compose run --rm producer python news_producer.py`
- [ ] Price producer running: `docker-compose run --rm producer python price_producer.py`
- [ ] Price consumer running: `docker-compose run --rm producer python price_consumer.py`

### ✅ Flink Job Submitted
- [ ] Flink job submitted: `docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py`
- [ ] Job shows as "Running" in Flink dashboard (http://localhost:8081)

### ✅ Data Flowing
- [ ] Kafka topics have messages
- [ ] Database tables have rows
- [ ] Dashboard shows data

## Common Issues

### Issue 1: No Producers Running
**Symptom:** Empty Kafka topics
**Fix:** Start producers in separate terminals

### Issue 2: Price Consumer Not Running
**Symptom:** Kafka has data, but `price_log` table is empty
**Fix:** Start `price_consumer.py`

### Issue 3: Flink Job Not Submitted
**Symptom:** Kafka has news, but `sentiment_log` table is empty
**Fix:** Submit Flink job

### Issue 4: API Key Missing
**Symptom:** Producers fail with "FINNHUB_API_KEY not set"
**Fix:** Create `.env` file with `FINNHUB_API_KEY=your_key`

### Issue 5: Database Connection Failed
**Symptom:** "password authentication failed"
**Fix:** Run `./fix_postgres.sh` or `docker-compose down -v && docker-compose up -d`

## Quick Fix Commands

```bash
# 1. Ensure all infrastructure is running
docker-compose up -d

# 2. Start all producers (in separate terminals)
docker-compose run --rm producer python news_producer.py
docker-compose run --rm producer python price_producer.py
docker-compose run --rm producer python price_consumer.py

# 3. Submit Flink job
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# 4. Wait 1-2 minutes for data to accumulate

# 5. Check database
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM price_log;"
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM sentiment_log;"

# 6. Refresh dashboard at http://localhost:8502
```

## Expected Timeline

- **0-30 seconds:** Producers start fetching data → Kafka topics get messages
- **30-60 seconds:** Price consumer writes to database → `price_log` has rows
- **60-120 seconds:** Flink processes news → `sentiment_log` has rows
- **2+ minutes:** Dashboard shows data

## Verification Queries

```sql
-- Check recent prices
SELECT symbol, price, timestamp 
FROM price_log 
ORDER BY timestamp DESC 
LIMIT 10;

-- Check recent sentiment
SELECT symbol, headline, sentiment_score 
FROM sentiment_log 
ORDER BY created_at DESC 
LIMIT 10;

-- Check data counts
SELECT 
    (SELECT COUNT(*) FROM price_log) as price_count,
    (SELECT COUNT(*) FROM sentiment_log) as sentiment_count;
```

---

**If still no data after following all steps, check:**
1. Producer logs for errors
2. Flink job logs for errors
3. Database connection from producers
4. Kafka connectivity

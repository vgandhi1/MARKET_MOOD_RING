# 🔧 Flink Kafka Group ID Fix

## Problem

Flink job fails with:
```
Property group.id is required when using committed offset for offsets initializer
```

## Root Cause

Flink Kafka connector requires a `group.id` property when using committed offsets. This is needed for Kafka consumer group management.

## Solution

Added `group.id` property to Kafka source configuration in `flink_sentiment.py`:

```python
'properties.group.id' = 'flink-sentiment-consumer',
'scan.startup.mode' = 'latest-offset',
```

## What Changed

Updated the Kafka source table definition:

**Before:**
```python
WITH (
    'connector' = 'kafka',
    'topic' = 'stock_news',
    'properties.bootstrap.servers' = 'kafka:29092',
    'format' = 'json'
)
```

**After:**
```python
WITH (
    'connector' = 'kafka',
    'topic' = 'stock_news',
    'properties.bootstrap.servers' = 'kafka:29092',
    'properties.group.id' = 'flink-sentiment-consumer',
    'scan.startup.mode' = 'latest-offset',
    'format' = 'json'
)
```

## Explanation

- **`properties.group.id`**: Unique identifier for the Kafka consumer group. Required for offset management.
- **`scan.startup.mode`**: 
  - `latest-offset`: Start reading from the latest messages (good for real-time processing)
  - `earliest-offset`: Start from the beginning of the topic
  - `group-offsets`: Use committed offsets from the consumer group

## How to Apply

The fix is already in `flink_jobs/flink_sentiment.py`. Since the file is mounted as a volume, the change is immediately available.

Just resubmit the Flink job:
```bash
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

## Expected Behavior

After the fix:
- Flink job should submit successfully
- Job will start reading from Kafka topic `stock_news`
- Sentiment analysis will process news headlines
- Results will be written to PostgreSQL `sentiment_log` table

## Verify

Check job status:
```bash
docker exec market_jobmanager ./bin/flink list
```

Check sentiment data:
```bash
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM sentiment_log;"
```

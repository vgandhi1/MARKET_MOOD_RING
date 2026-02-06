# 🔧 Flink Kafka Connector Fix

## Problem

Flink job fails with:
```
Could not find any factory for identifier 'kafka' that implements 'org.apache.flink.table.factories.DynamicTableFactory' in the classpath.
```

## Root Cause

The Kafka connector JAR is missing from Flink's `/opt/flink/lib/` directory. The `apache-flink-libraries` Python package doesn't include the Java connector JARs.

## Solution

Added connector JARs to `Dockerfile.flink`:

1. **Kafka Connector:** `flink-sql-connector-kafka-1.17.0.jar`
2. **JDBC Connector:** `flink-connector-jdbc-3.1.1-1.17.jar`
3. **PostgreSQL Driver:** `postgresql-42.5.4.jar`

## How to Apply Fix

### Rebuild Flink Containers

```bash
# Stop Flink services
docker-compose stop jobmanager taskmanager

# Rebuild with connector JARs
docker-compose build jobmanager taskmanager

# Start services
docker-compose up -d jobmanager taskmanager

# Wait for services to be ready
sleep 10

# Submit Flink job
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

## Verification

After rebuilding, verify connectors are available:

```bash
# Check Kafka connector JAR exists
docker exec market_taskmanager ls -la /opt/flink/lib/ | grep kafka

# Check JDBC connector JAR exists
docker exec market_taskmanager ls -la /opt/flink/lib/ | grep jdbc

# Check PostgreSQL driver exists
docker exec market_taskmanager ls -la /opt/flink/lib/ | grep postgresql
```

Expected output should show:
- `flink-sql-connector-kafka-1.17.0.jar`
- `flink-connector-jdbc-3.1.1-1.17.jar`
- `postgresql-42.5.4.jar`

## What Changed

The `Dockerfile.flink` now downloads and installs:
1. Kafka connector for reading from Kafka topics
2. JDBC connector for writing to PostgreSQL
3. PostgreSQL JDBC driver for database connectivity

These JARs are placed in `/opt/flink/lib/` where Flink automatically discovers them.

## Expected Behavior After Fix

When you submit the Flink job:
```bash
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

You should see:
- Job submitted successfully
- Job ID returned
- No "connector not found" errors

Check job status:
```bash
docker exec market_jobmanager ./bin/flink list
```

Or visit Flink dashboard: http://localhost:8081

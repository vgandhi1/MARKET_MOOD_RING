# Flink build and runtime fixes

Common Flink issues for Market Mood Ring. For job submission and operations, see **[FLINK_JOB_GUIDE.md](../FLINK_JOB_GUIDE.md)**.

---

## 1. Kafka connector not found

**Error:**
```
Could not find any factory for identifier 'kafka' that implements 'org.apache.flink.table.factories.DynamicTableFactory' in the classpath.
```

**Cause:** Kafka/JDBC connector JARs missing from `/opt/flink/lib/`.

**Fix:** Rebuild Flink images (JARs are installed in `Dockerfile.flink`):

```bash
docker-compose stop jobmanager taskmanager
docker-compose build jobmanager taskmanager
docker-compose up -d jobmanager taskmanager
sleep 10
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

**Verify:**
```bash
docker exec market_taskmanager ls /opt/flink/lib/ | grep -E 'kafka|jdbc|postgresql'
```

Expected: `flink-sql-connector-kafka-1.17.0.jar`, `flink-connector-jdbc-3.1.1-1.17.jar`, `postgresql-42.5.4.jar`

---

## 2. Kafka group.id required

**Error:**
```
Property group.id is required when using committed offset for offsets initializer
```

**Fix:** Already configured in `flink_jobs/flink_sentiment.py`:

```python
'properties.group.id' = 'flink-sentiment-consumer',
'scan.startup.mode' = 'latest-offset',
```

Resubmit the job:
```bash
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

---

## 3. Python command not found

**Error:**
```
Cannot run program "python": error=2, No such file or directory
```

**Cause:** Container has `python3` only; Flink expects `python`.

**Fix:** `Dockerfile.flink` creates `python` → `python3` symlink. Rebuild:

```bash
docker-compose up -d --build jobmanager taskmanager
docker exec market_taskmanager which python   # should print /usr/bin/python
```

---

## Verification

```bash
docker exec market_jobmanager ./bin/flink list
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM sentiment_log;"
```

Flink UI: http://localhost:8081

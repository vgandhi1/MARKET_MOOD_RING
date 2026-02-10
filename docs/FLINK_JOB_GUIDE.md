# 🌊 Flink Job Management Guide

**Complete Guide to Managing Apache Flink Jobs in Market Mood Ring**

This guide covers everything you need to know about running, monitoring, and troubleshooting Flink jobs.

---

## 📋 Table of Contents

1. [Quick Reference](#quick-reference)
2. [Understanding Flink Jobs](#understanding-flink-jobs)
3. [Automatic Job Submission](#automatic-job-submission)
4. [Manual Job Submission](#manual-job-submission)
5. [Monitoring Flink Jobs](#monitoring-flink-jobs)
6. [Managing Jobs](#managing-jobs)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Operations](#advanced-operations)

---

## Quick Reference

### Essential Commands

```bash
# ✅ RECOMMENDED: Use startup script (handles everything)
./start_data_pipeline.sh

# Check if job is running
docker exec market_jobmanager ./bin/flink list

# Submit job manually (correct container name!)
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# Cancel a job
docker exec market_jobmanager ./bin/flink cancel <job-id>

# View Flink UI
# Open: http://localhost:8081
```

### Container Names

| ❌ WRONG | ✅ CORRECT |
|----------|-----------|
| `vibe_jobmanager` | `market_jobmanager` |
| `vibe_taskmanager` | `market_taskmanager` |

**Common mistake:** Using old container names from a different project!

---

## Understanding Flink Jobs

### What is the Flink Sentiment Job?

**File:** `flink_jobs/flink_sentiment.py`

**Purpose:** Real-time sentiment analysis of stock news headlines

**What it does:**
1. 📥 Consumes messages from Kafka topic `stock_news`
2. 🧠 Analyzes sentiment using NLTK Vader
3. 💾 Writes results to PostgreSQL table `sentiment_log`

**Data Flow:**
```
Kafka (stock_news topic)
    ↓
Flink Job (sentiment analysis)
    ↓
PostgreSQL (sentiment_log table)
    ↓
Dashboard (visualization)
```

### Job Architecture

```python
# Simplified structure of flink_sentiment.py

1. Create Flink execution environment
2. Connect to Kafka as source
3. Define sentiment analysis UDF (NLTK Vader)
4. Apply sentiment function to news stream
5. Connect to PostgreSQL as sink
6. Execute job
```

**Processing Model:** Streaming (continuous processing)

**Parallelism:** Configurable in docker-compose.yaml (default: 1)

**Checkpointing:** Enabled for fault tolerance

---

## Automatic Job Submission

### Using start_data_pipeline.sh (Recommended)

The startup script **automatically** handles Flink job submission as Step 6/6:

```bash
./start_data_pipeline.sh
```

**What happens:**

```
📋 Step 6/6: Checking Flink job status...

   ⚠️  Flink job not running. Submitting...
   ✅ Flink sentiment job submitted successfully

   Job ID: c2fc53cc39771e7c23a2e97cb89a99c3
```

**Script logic:**

```bash
# 1. Check if job is already running
FLINK_JOBS=$(docker exec market_jobmanager ./bin/flink list 2>/dev/null | grep "flink_sentiment" | wc -l)

# 2. If not running, submit it
if [ "$FLINK_JOBS" -eq "0" ]; then
    docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
fi

# 3. If already running, skip
# "✅ Flink sentiment job is already running"
```

**Advantages:**
- ✅ Automatic - no manual steps
- ✅ Idempotent - safe to run multiple times
- ✅ Error handling - shows helpful messages
- ✅ Waits for JobManager to be ready

---

## Manual Job Submission

### When to Submit Manually

**Use cases:**
- Job crashed and needs resubmission
- Testing job modifications
- Debugging job issues
- Started containers with docker-compose (not script)

### Step-by-Step Manual Submission

#### Step 1: Verify JobManager is Running

```bash
# Check container status
docker ps | grep jobmanager

# Should show:
# market_jobmanager   Up X minutes
```

#### Step 2: Check Current Job Status

```bash
docker exec market_jobmanager ./bin/flink list
```

**Output if no job running:**
```
Waiting for response...
No running jobs.
No scheduled jobs.
```

**Output if job is running:**
```
------------------ Running/Restarting Jobs -------------------
10.02.2026 03:55:23 : c2fc53cc39771e7c23a2e97cb89a99c3 : insert-into_default_catalog.default_database.sentiment_sink (RUNNING)
--------------------------------------------------------------
```

#### Step 3: Submit the Job (If Not Running)

**✅ Correct command:**
```bash
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

**Expected output:**
```
Job has been submitted with JobID c2fc53cc39771e7c23a2e97cb89a99c3
```

**⏱️ Wait time:** 5-10 seconds

#### Step 4: Verify Submission

```bash
# Check job is running
docker exec market_jobmanager ./bin/flink list

# Should now show job in RUNNING state
```

### Common Mistakes

#### ❌ WRONG: Using Old Container Name

```bash
# This will fail if you copied from old project
docker exec vibe_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# Error: No such container: vibe_jobmanager
```

**✅ FIX:** Use `market_jobmanager`

#### ❌ WRONG: Using Wrong File Path

```bash
# Wrong path
docker exec market_jobmanager ./bin/flink run -py /app/flink_sentiment.py

# Error: File not found
```

**✅ FIX:** Use `/opt/flink/usrlib/flink_sentiment.py`

#### ❌ WRONG: JobManager Not Ready

```bash
# Submitting too soon after starting containers
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# Error: Connection refused
```

**✅ FIX:** Wait 30 seconds or use the startup script

---

## Monitoring Flink Jobs

### Method 1: Flink Web UI (Recommended)

**Access:** http://localhost:8081

**Features:**
- ✅ Visual job graph
- ✅ Real-time metrics
- ✅ Task manager status
- ✅ Exception logs
- ✅ Checkpoint history

**Navigation:**
```
http://localhost:8081
    ↓
Jobs → Running Jobs
    ↓
Click on job → Overview
    ↓
View: Graph, Timeline, Exceptions, Checkpoints
```

**Key Metrics to Monitor:**
- **Status:** Should be `RUNNING`
- **Uptime:** How long job has been running
- **Records Received:** Count of messages processed
- **Records Sent:** Count of records written to PostgreSQL
- **Backpressure:** Should be green (low)

### Method 2: Command Line

```bash
# List all jobs
docker exec market_jobmanager ./bin/flink list

# Get detailed job info
docker exec market_jobmanager ./bin/flink info <job-id>

# View JobManager logs
docker logs market_jobmanager --tail 100

# View TaskManager logs
docker logs market_taskmanager --tail 100
```

### Method 3: Check Database Output

```bash
# Verify sentiment records are being written
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT COUNT(*) as total_records,
       MAX(timestamp) as latest_record
FROM sentiment_log;
"

# View recent sentiment records
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT symbol, headline, sentiment_score, timestamp
FROM sentiment_log
ORDER BY timestamp DESC
LIMIT 10;
"
```

**Expected:** Should see increasing count and recent timestamps

---

## Managing Jobs

### Restart a Job

**Scenario:** Job crashed or needs update

```bash
# 1. Get current job ID
docker exec market_jobmanager ./bin/flink list

# 2. Cancel the job
docker exec market_jobmanager ./bin/flink cancel <job-id>

# 3. Wait for cancellation (5-10 seconds)
sleep 10

# 4. Resubmit
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# OR just use the script (easier):
./start_data_pipeline.sh
```

### Stop a Job

```bash
# Graceful cancellation (with savepoint)
docker exec market_jobmanager ./bin/flink cancel -s /tmp/savepoints <job-id>

# Force stop (without savepoint)
docker exec market_jobmanager ./bin/flink cancel <job-id>
```

### Update Job Code

```bash
# 1. Edit the Python file
nano flink_jobs/flink_sentiment.py

# 2. Stop current job
docker exec market_jobmanager ./bin/flink cancel <job-id>

# 3. Restart Flink containers (picks up new file via volume mount)
docker-compose restart jobmanager taskmanager

# 4. Wait for Flink to be ready
sleep 30

# 5. Submit updated job
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

**Note:** Changes are reflected immediately due to volume mount in docker-compose.yaml:
```yaml
volumes:
  - ./flink_jobs:/opt/flink/usrlib
```

---

## Troubleshooting

### Issue 1: "No such container: vibe_jobmanager"

**Error:**
```bash
Error response from daemon: No such container: vibe_jobmanager
```

**Cause:** Using wrong container name (from old project or tutorial)

**Solution:**
```bash
# Check actual container name
docker ps --filter "name=jobmanager"

# Use correct name
docker exec market_jobmanager ./bin/flink list
```

---

### Issue 2: Job Not Running After Startup

**Symptom:**
```bash
docker exec market_jobmanager ./bin/flink list
# Shows: No running jobs
```

**Causes & Solutions:**

**A. Started with docker-compose (not script)**
```bash
# The script handles job submission, docker-compose doesn't
# Solution: Use the script
./start_data_pipeline.sh
```

**B. Job submission failed silently**
```bash
# Check logs for errors
docker logs market_jobmanager | grep -i error

# Manually submit
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

**C. JobManager not ready when job was submitted**
```bash
# Restart with proper sequencing
./start_data_pipeline.sh
```

---

### Issue 3: Job Keeps Failing/Restarting

**Symptom:** Flink UI shows job status changes from RUNNING → FAILED → RESTARTING

**Check 1: Kafka Connection**
```bash
# Verify Kafka is healthy
docker exec market_kafka kafka-broker-api-versions --bootstrap-server localhost:9092

# Check if topic exists
docker exec market_kafka kafka-topics --list --bootstrap-server localhost:9092 | grep stock_news
```

**Check 2: PostgreSQL Connection**
```bash
# Verify PostgreSQL is healthy
docker exec market_postgres pg_isready -U market_user -d market_mood

# Check if table exists
docker exec market_postgres psql -U market_user -d market_mood -c "\dt sentiment_log"
```

**Check 3: Job Logs**
```bash
# View JobManager logs
docker logs market_jobmanager --tail 100 | grep -i error

# View TaskManager logs
docker logs market_taskmanager --tail 100 | grep -i error
```

**Check 4: Python Dependencies**
```bash
# Verify NLTK data is available
docker exec market_jobmanager python3 -c "import nltk; nltk.data.find('vader_lexicon')"

# If not found, rebuild Flink image
docker-compose build --no-cache jobmanager taskmanager
docker-compose up -d jobmanager taskmanager
```

---

### Issue 4: "Connection refused" When Submitting

**Error:**
```
java.net.ConnectException: Connection refused
```

**Cause:** JobManager not fully started

**Solution:**
```bash
# Wait for JobManager to be ready
echo "Waiting for Flink..."
until docker exec market_jobmanager ./bin/flink list &> /dev/null; do
    echo -n "."
    sleep 2
done
echo " Ready!"

# Now submit
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

**Or use the script (handles this automatically):**
```bash
./start_data_pipeline.sh
```

---

### Issue 5: Job Submitted But No Data in Database

**Symptom:** Job shows RUNNING, but `sentiment_log` table is empty

**Check 1: Kafka Has Data**
```bash
# Check if news producer is running
docker logs market_news_producer --tail 20

# Should see: "Published: AAPL - Headline..."
```

**Check 2: Flink Job Is Consuming**
```bash
# Open Flink UI: http://localhost:8081
# Navigate to: Jobs → Running Jobs → Your Job
# Check: "Records Received" should be increasing
```

**Check 3: Check for Exceptions**
```bash
# Flink UI → Exceptions tab
# Look for database write errors
```

**Check 4: Database Permissions**
```bash
# Verify connection from Flink
docker exec market_jobmanager python3 -c "
import psycopg2
conn = psycopg2.connect(
    host='postgres',
    database='market_mood',
    user='market_user',
    password='market_password'
)
print('✅ Connection successful')
conn.close()
"
```

---

## Advanced Operations

### View Job Details

```bash
# Get job ID
JOB_ID=$(docker exec market_jobmanager ./bin/flink list 2>/dev/null | grep -oP '(?<=: )\w+' | head -1)

# Show job info
docker exec market_jobmanager ./bin/flink info $JOB_ID

# Show job plan (JSON)
docker exec market_jobmanager ./bin/flink info -p $JOB_ID
```

### Create Savepoint

```bash
# Create savepoint (for backup before upgrade)
docker exec market_jobmanager ./bin/flink savepoint <job-id> /tmp/savepoints

# List savepoints
docker exec market_jobmanager ls -la /tmp/savepoints/
```

### Restore from Savepoint

```bash
# Submit job with savepoint
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py -s /tmp/savepoints/<savepoint-id>
```

### Change Parallelism

**Edit docker-compose.yaml:**
```yaml
environment:
  - |
    FLINK_PROPERTIES=
    jobmanager.rpc.address: jobmanager
    taskmanager.numberOfTaskSlots: 4  # Increase from 2
    parallelism.default: 2              # Increase from 1
```

**Restart:**
```bash
docker-compose restart jobmanager taskmanager
./start_data_pipeline.sh
```

### Debug Mode

**Enable verbose logging:**
```bash
# Edit flink_jobs/flink_sentiment.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)

# Restart job to see debug logs
docker logs market_taskmanager -f
```

---

## Complete Workflow Example

### Starting from Scratch

```bash
# 1. Start everything with script (includes Flink job)
./start_data_pipeline.sh

# 2. Verify job is running
docker exec market_jobmanager ./bin/flink list
# Should show: insert-into_default_catalog... (RUNNING)

# 3. Monitor in UI
# Open: http://localhost:8081

# 4. Check data is flowing
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT COUNT(*) FROM sentiment_log;
"
# Should show increasing count
```

### After Container Restart

```bash
# If you stopped containers
docker-compose --profile producers up -d

# Wait for services (30 seconds)
sleep 30

# Submit Flink job
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# OR just use script:
./start_data_pipeline.sh
```

---

## Quick Troubleshooting Checklist

When Flink job issues occur, check in order:

- [ ] JobManager container is running: `docker ps | grep jobmanager`
- [ ] Job is submitted: `docker exec market_jobmanager ./bin/flink list`
- [ ] Kafka is healthy: `docker logs market_kafka --tail 20`
- [ ] PostgreSQL is healthy: `docker exec market_postgres pg_isready`
- [ ] News producer is publishing: `docker logs market_news_producer --tail 20`
- [ ] No errors in Flink logs: `docker logs market_jobmanager | grep -i error`
- [ ] Data appearing in database: `SELECT COUNT(*) FROM sentiment_log;`

---

## Summary

### Recommended Approach

**✅ Use `./start_data_pipeline.sh`**
- Handles everything automatically
- Checks if job is already running
- Waits for dependencies
- Shows clear status

### Manual Operations

**When needed:**
- Use correct container name: `market_jobmanager` (not `vibe_jobmanager`)
- Use correct file path: `/opt/flink/usrlib/flink_sentiment.py`
- Wait for JobManager to be ready before submitting

### Key Commands

```bash
# Check status
docker exec market_jobmanager ./bin/flink list

# Submit job
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# Cancel job
docker exec market_jobmanager ./bin/flink cancel <job-id>

# Monitor UI
http://localhost:8081
```

---

## Related Documentation

- [Getting Started](../GETTING_STARTED.md) - Initial setup
- [Troubleshooting](../TROUBLESHOOTING.md) - Common issues
- [NLTK Sentiment Analysis](../technical/NLTK_SENTIMENT_ANALYSIS.md) - How sentiment works
- [System Architecture](../architecture/SYSTEM_ARCHITECTURE.md) - Overall design

---

*Last Updated: February 2026*  
*For issues, see [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)*

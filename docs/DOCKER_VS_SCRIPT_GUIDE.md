# Docker Compose vs start_data_pipeline.sh

**Understanding When and How to Use Each Method**

This guide explains the differences between using `docker-compose` directly versus the `start_data_pipeline.sh` script, and when to use each approach.

---

## 📋 Table of Contents

1. [Quick Comparison](#quick-comparison)
2. [Understanding start_data_pipeline.sh](#understanding-start_data_pipelinesh)
3. [Understanding docker-compose](#understanding-docker-compose)
4. [When to Use Each Method](#when-to-use-each-method)
5. [Common Scenarios](#common-scenarios)
6. [Troubleshooting](#troubleshooting)

---

## Quick Comparison

| Feature | start_data_pipeline.sh | docker-compose |
|---------|----------------------|----------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Beginner-friendly | ⭐⭐⭐ Requires knowledge |
| **Pre-flight Checks** | ✅ Validates .env, files, Docker | ❌ None |
| **Startup Sequencing** | ✅ Waits for services to be healthy | ❌ Starts all at once |
| **Flink Job Submission** | ✅ Automatic | ❌ Manual |
| **Ollama IP Detection** | ✅ Automatic (Windows host) | ❌ Manual configuration needed |
| **Error Handling** | ✅ Detailed error messages | ⚠️ Generic Docker errors |
| **Cleanup** | ✅ Removes corrupted containers | ❌ Manual |
| **Status Reporting** | ✅ Shows detailed progress | ⚠️ Basic output |
| **Use Case** | Daily use, first-time setup | Development, debugging |

**Recommendation:** Use `start_data_pipeline.sh` for normal operation.

---

## Understanding start_data_pipeline.sh

### What It Does

The startup script is a **smart wrapper** around docker-compose that handles the complexity of starting a multi-service pipeline correctly.

### Step-by-Step Execution

```bash
./start_data_pipeline.sh
```

**Phase 1: Pre-flight Checks (10 seconds)**
```
📋 Step 1/6: Running pre-flight checks...
```
- ✅ Checks `.env` file exists
- ✅ Validates `FINNHUB_API_KEY` is set (not placeholder)
- ✅ Verifies required files exist (`docker-compose.yaml`, `init.sql`, etc.)
- ✅ Checks required directories exist (`producer/`, `flink_jobs/`, etc.)
- ✅ Confirms Docker is running
- ✅ Confirms docker-compose is installed

**Phase 2: Network Configuration (5 seconds)**
```
📋 Step 2/6: Detecting Windows Host IP...
```
- 🔍 Resolves `host.docker.internal` to actual Windows host IP
- 📝 Exports `WINDOWS_HOST_IP` environment variable
- 🎯 Used for Ollama connection from dashboard container

**Phase 3: Container Cleanup (5 seconds)**
```
📋 Step 3/6: Checking for old containers...
```
- 🧹 Detects containers with corrupted metadata (from `KeyError: 'ContainerConfig'`)
- 🗑️ Automatically removes corrupted containers
- ✨ Prevents startup failures

**Phase 4: Service Startup (30 seconds)**
```
📋 Step 4/6: Starting all services...
```
- 🚀 Runs `docker-compose --profile producers up -d`
- 🏗️ Creates network, volumes, and containers
- ⏳ Returns when containers are created (not necessarily ready)

**Phase 5: Health Checks (30-60 seconds)**
```
📋 Step 5/6: Waiting for services to become healthy...
```
- ⏰ Waits for Kafka to accept connections (up to 60s)
- ⏰ Waits for PostgreSQL to be ready (up to 60s)
- ⏰ Waits for Flink JobManager to accept commands (up to 60s)
- ✅ Ensures producers won't fail with `NoBrokersAvailable`

**Phase 6: Flink Job Submission (10 seconds)**
```
📋 Step 6/6: Checking Flink job status...
```
- 🔍 Checks if sentiment job is already running
- 📤 Submits job if not running
- ✅ Verifies submission succeeded

**Final Report**
```
✅ Pipeline is fully active!
📊 Service Status: [list of all services]
🔗 Access Points: [URLs and ports]
```

### Advantages

1. **Beginner-Friendly**
   - No need to know Docker commands
   - Clear progress messages
   - Helpful error messages

2. **Prevents Common Issues**
   - No `NoBrokersAvailable` errors
   - No corrupted container metadata
   - No "Ollama connection refused" issues

3. **Saves Time**
   - No manual health checking
   - No manual Flink job submission
   - No troubleshooting startup sequence

4. **Idempotent**
   - Safe to run multiple times
   - Handles already-running services gracefully

### Source Code

```bash
# View the script
cat start_data_pipeline.sh

# Make executable (if needed)
chmod +x start_data_pipeline.sh
```

---

## Understanding docker-compose

### What It Is

`docker-compose` is the **underlying tool** for managing multi-container Docker applications. It reads `docker-compose.yaml` and creates/starts containers accordingly.

### Basic Commands

```bash
# Start all services (infrastructure only, no producers)
docker-compose up -d

# Start with producers profile
docker-compose --profile producers up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart <service-name>

# Rebuild images
docker-compose build --no-cache

# View service status
docker-compose ps
```

### What docker-compose Does

When you run `docker-compose --profile producers up -d`:

1. **Reads Configuration**
   - Parses `docker-compose.yaml`
   - Loads `.env` file (if present)
   - Evaluates environment variable substitutions

2. **Creates Resources**
   - Creates network: `market_mood_ring_market_network`
   - Creates volumes: `postgres_data`, `ollama_data`

3. **Starts Containers** (in dependency order)
   ```
   kafka, postgres (independent)
     ↓
   jobmanager, dashboard (depends on kafka, postgres)
     ↓
   taskmanager (depends on jobmanager)
     ↓
   news-producer, price-producer, price-consumer, rag-ingest
     (depends on kafka, postgres via profile)
   ```

4. **Returns Immediately**
   - Doesn't wait for services to be ready
   - Just starts containers and exits

### What docker-compose Does NOT Do

- ❌ Wait for Kafka to accept connections
- ❌ Wait for PostgreSQL to initialize
- ❌ Submit Flink jobs
- ❌ Check for corrupted containers
- ❌ Detect Windows host IP for Ollama
- ❌ Validate environment variables
- ❌ Show detailed status information

### Advantages

1. **Fine-Grained Control**
   - Start/stop individual services
   - Rebuild specific images
   - View raw Docker output

2. **Development Workflow**
   - Quick iteration on single service
   - Inspect container internals
   - Debug networking issues

3. **CI/CD Integration**
   - Scriptable
   - Standard tool
   - Well-documented

### Disadvantages for Beginners

1. **Requires Knowledge**
   - Need to understand Docker concepts
   - Must know service dependencies
   - Have to troubleshoot startup issues

2. **Manual Steps Required**
   - Must wait manually for services
   - Must submit Flink jobs manually
   - Must handle errors yourself

3. **Race Conditions**
   - Producers may start before Kafka ready
   - Results in `NoBrokersAvailable` errors
   - Requires restart

---

## When to Use Each Method

### Use start_data_pipeline.sh For:

✅ **Daily Operations**
```bash
# Start pipeline for the day
./start_data_pipeline.sh
```

✅ **First-Time Setup**
```bash
# Initial setup after git clone
./start_data_pipeline.sh
```

✅ **After System Restart**
```bash
# After rebooting computer
./start_data_pipeline.sh
```

✅ **Troubleshooting**
```bash
# Something went wrong, start fresh
docker-compose --profile producers down
./start_data_pipeline.sh
```

✅ **Production/Demo**
```bash
# Presenting to someone
./start_data_pipeline.sh
```

---

### Use docker-compose For:

🔧 **Stopping Services**
```bash
# Stop everything
docker-compose --profile producers down

# Stop but keep data
docker-compose --profile producers stop
```

🔧 **Restarting Single Service**
```bash
# Modified dashboard code
docker-compose restart dashboard

# Updated producer logic
docker-compose restart news-producer
```

🔧 **Rebuilding Images**
```bash
# Changed Dockerfile
docker-compose build --no-cache dashboard
docker-compose up -d dashboard
```

🔧 **Viewing Logs**
```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs -f kafka
```

🔧 **Starting Infrastructure Only**
```bash
# Start kafka and postgres, but not producers
docker-compose up -d kafka postgres
```

🔧 **Development/Debugging**
```bash
# Start specific service with overrides
docker-compose up -d --build news-producer
```

---

## Common Scenarios

### Scenario 1: Starting Fresh

**❌ Don't do this:**
```bash
docker-compose up -d
# Missing: producers, Flink job, health checks
```

**✅ Do this:**
```bash
./start_data_pipeline.sh
# Everything handled automatically
```

---

### Scenario 2: Modified Producer Code

**✅ Quick iteration:**
```bash
# Edit producer/news_producer.py
nano producer/news_producer.py

# Restart just that service
docker-compose restart news-producer

# Check logs
docker logs market_news_producer -f
```

**Note:** If you changed dependencies, rebuild:
```bash
docker-compose build --no-cache news-producer
docker-compose up -d news-producer
```

---

### Scenario 3: Something Went Wrong

**✅ Nuclear option (full reset):**
```bash
# Stop and remove everything
docker-compose --profile producers down -v

# Start fresh
./start_data_pipeline.sh
```

**✅ Graceful restart (keep data):**
```bash
docker-compose --profile producers down
./start_data_pipeline.sh
```

---

### Scenario 4: Checking Flink Job

**Using script:**
```bash
./start_data_pipeline.sh
# Automatically checks and submits if needed
```

**Using docker-compose (manual):**
```bash
# Start services
docker-compose --profile producers up -d

# Wait for Flink to be ready
sleep 30

# Check if job exists
docker exec market_jobmanager ./bin/flink list

# Submit manually if needed
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

---

### Scenario 5: Changing Stock Symbols

**✅ Edit .env and restart producers:**
```bash
# Edit .env
nano .env
# Change: STOCK_SYMBOLS=NVDA,AMD,INTC

# Restart affected services
docker-compose restart news-producer price-producer price-consumer

# Check logs
docker logs market_price_producer -f
```

---

### Scenario 6: Updating Dashboard Code

**✅ Quick restart (if only Python changes):**
```bash
# Edit dashboard/app.py
nano dashboard/app.py

# Restart
docker-compose restart dashboard

# View in browser: http://localhost:8502
```

**✅ Rebuild (if requirements changed):**
```bash
# Edit dashboard/requirements.txt
nano dashboard/requirements.txt

# Rebuild
docker-compose build --no-cache dashboard
docker-compose up -d dashboard
```

---

## Troubleshooting

### Issue: Started with docker-compose, Getting NoBrokersAvailable

**Problem:**
```bash
docker-compose --profile producers up -d
# Producers crash with: NoBrokersAvailable
```

**Why it happened:**
- Producers started before Kafka was ready
- No health checks

**Fix:**
```bash
# Stop
docker-compose --profile producers down

# Use script instead
./start_data_pipeline.sh
```

---

### Issue: Flink Job Not Running After docker-compose up

**Problem:**
```bash
docker-compose --profile producers up -d
# Flink started, but no job running
```

**Why it happened:**
- docker-compose doesn't submit jobs

**Fix:**
```bash
# Submit manually
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# OR restart with script
./start_data_pipeline.sh
```

---

### Issue: Ollama Connection Fails After docker-compose up

**Problem:**
```bash
docker-compose --profile producers up -d
# Dashboard can't reach Ollama
```

**Why it happened:**
- `WINDOWS_HOST_IP` not set
- Dashboard uses default IP (172.17.0.1)

**Fix:**
```bash
# Stop
docker-compose --profile producers down

# Use script (detects correct IP)
./start_data_pipeline.sh
```

---

### Issue: Want to Use docker-compose but Need Health Checks

**Solution: Manual health checks**

```bash
# Start infrastructure
docker-compose up -d kafka postgres jobmanager

# Wait for Kafka
echo "Waiting for Kafka..."
until docker exec market_kafka kafka-broker-api-versions --bootstrap-server localhost:9092 &> /dev/null; do
    echo -n "."
    sleep 2
done
echo " Ready!"

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
until docker exec market_postgres pg_isready -U market_user -d market_mood &> /dev/null; do
    echo -n "."
    sleep 2
done
echo " Ready!"

# Now start producers
docker-compose --profile producers up -d
```

**Better solution:** Just use `./start_data_pipeline.sh` 😊

---

## Best Practices

### ✅ Do This

1. **Use the script for normal operations**
   ```bash
   ./start_data_pipeline.sh
   ```

2. **Use docker-compose for granular control**
   ```bash
   docker-compose restart dashboard
   ```

3. **Stop with docker-compose**
   ```bash
   docker-compose --profile producers down
   ```

4. **View logs with docker-compose**
   ```bash
   docker-compose logs -f news-producer
   ```

5. **Rebuild specific services with docker-compose**
   ```bash
   docker-compose build --no-cache dashboard
   ```

### ❌ Don't Do This

1. **Don't start cold with docker-compose**
   ```bash
   # BAD: No health checks, no Flink job
   docker-compose --profile producers up -d
   ```

2. **Don't manually set WINDOWS_HOST_IP**
   ```bash
   # BAD: Might be wrong, script detects automatically
   export WINDOWS_HOST_IP=192.168.1.100
   docker-compose up -d
   ```

3. **Don't forget profiles**
   ```bash
   # BAD: Doesn't start producers
   docker-compose up -d
   
   # GOOD: Starts producers too
   docker-compose --profile producers up -d
   ```

---

## Quick Reference

### Common Commands

| Task | Command |
|------|---------|
| **Start everything** | `./start_data_pipeline.sh` |
| **Stop everything** | `docker-compose --profile producers down` |
| **Restart service** | `docker-compose restart <name>` |
| **View logs** | `docker-compose logs -f <name>` |
| **Rebuild image** | `docker-compose build --no-cache <name>` |
| **Check status** | `docker ps --filter "name=market_"` |
| **Submit Flink job** | `docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py` |
| **Full reset** | `docker-compose --profile producers down -v && ./start_data_pipeline.sh` |

---

## Summary

**start_data_pipeline.sh:**
- 🎯 **For beginners and daily use**
- ✅ Handles everything automatically
- ⏱️ Takes 2-3 minutes
- 🛡️ Prevents common issues
- 📊 Detailed status reporting

**docker-compose:**
- 🔧 **For developers and specific tasks**
- 🎛️ Fine-grained control
- ⚡ Fast for single-service changes
- 🔍 Standard Docker tool
- 📝 Requires manual steps

**Best approach:** Use the script to start, use docker-compose for management.

---

*Last Updated: February 2026*  
*Related: [GETTING_STARTED.md](GETTING_STARTED.md), [TROUBLESHOOTING.md](TROUBLESHOOTING.md)*

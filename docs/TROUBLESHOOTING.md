# 🔧 Troubleshooting Guide - Market Mood Ring

**Complete Guide to Diagnosing and Fixing Common Issues**

This guide covers all common problems you might encounter and their solutions, organized by category.

---

## 📋 Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Startup Issues](#startup-issues)
3. [Container Issues](#container-issues)
4. [Producer Issues](#producer-issues)
5. [Flink Issues](#flink-issues)
6. [Database Issues](#database-issues)
7. [Dashboard Issues](#dashboard-issues)
8. [Ollama/AI Issues](#ollamai-issues)
9. [Network Issues](#network-issues)
10. [Performance Issues](#performance-issues)
11. [Data Issues](#data-issues)
12. [Recovery Procedures](#recovery-procedures)

---

## Quick Diagnostics

### Run This First

```bash
# Check Docker status
docker info

# Check all containers
docker ps --filter "name=market_"

# Check for errors in startup script output
./start_data_pipeline.sh | grep -E "ERROR|FAIL"

# View recent logs from all services
docker-compose logs --tail=50
```

### Health Check Script

Create a quick diagnostic script:

```bash
#!/bin/bash
echo "=== Market Mood Ring Health Check ==="
echo ""

echo "1. Docker Status:"
docker info > /dev/null 2>&1 && echo "✅ Docker is running" || echo "❌ Docker is NOT running"

echo ""
echo "2. Container Status:"
docker ps --filter "name=market_" --format "{{.Names}}: {{.Status}}"

echo ""
echo "3. Kafka Health:"
docker exec market_kafka kafka-broker-api-versions --bootstrap-server localhost:9092 > /dev/null 2>&1 \
  && echo "✅ Kafka is healthy" || echo "❌ Kafka is NOT healthy"

echo ""
echo "4. PostgreSQL Health:"
docker exec market_postgres pg_isready -U market_user -d market_mood > /dev/null 2>&1 \
  && echo "✅ PostgreSQL is healthy" || echo "❌ PostgreSQL is NOT healthy"

echo ""
echo "5. Flink Job Status:"
docker exec market_jobmanager ./bin/flink list 2>/dev/null | grep -q "RUNNING" \
  && echo "✅ Flink job is running" || echo "❌ No Flink job running"

echo ""
echo "6. Data Collection:"
PRICE_COUNT=$(docker exec market_postgres psql -U market_user -d market_mood -t -c "SELECT COUNT(*) FROM stock_prices;" 2>/dev/null | tr -d ' ')
echo "Stock prices in DB: $PRICE_COUNT"

SENTIMENT_COUNT=$(docker exec market_postgres psql -U market_user -d market_mood -t -c "SELECT COUNT(*) FROM sentiment_log;" 2>/dev/null | tr -d ' ')
echo "Sentiment records in DB: $SENTIMENT_COUNT"
```

Save as `health_check.sh`, make executable, and run:

```bash
chmod +x health_check.sh
./health_check.sh
```

---

## Startup Issues

### Issue: "FINNHUB_API_KEY is not set"

**Symptoms:**
```
❌ ERROR: FINNHUB_API_KEY is not set in .env file
```

**Cause:** The `.env` file doesn't contain a valid API key.

**Solution:**

1. **Check if .env exists:**
   ```bash
   ls -la .env
   ```

2. **If missing, create from template:**
   ```bash
   cp .env.example .env
   ```

3. **Edit the file:**
   ```bash
   nano .env
   ```

4. **Add your actual key:**
   ```bash
   FINNHUB_API_KEY=your_actual_key_from_finnhub_dashboard
   ```

5. **Verify:**
   ```bash
   grep FINNHUB_API_KEY .env
   # Should NOT show: "your_key_here" or "your_finnhub_api_key_here"
   ```

6. **Re-run startup script:**
   ```bash
   ./start_data_pipeline.sh
   ```

---

### Issue: "Docker is not running"

**Symptoms:**
```
❌ ERROR: Docker is not running!
```

**Cause:** Docker Desktop is not started or Docker daemon is stopped.

**Solution:**

**Windows (WSL2):**
```powershell
# Start Docker Desktop from Start Menu
# Wait for notification: "Docker Desktop is running"

# Verify in WSL terminal:
docker info
```

**macOS:**
```bash
# Launch Docker Desktop from Applications
# Wait for whale icon to stop animating

# Verify:
docker info
```

**Linux:**
```bash
# Start Docker service
sudo systemctl start docker

# Check status
sudo systemctl status docker

# Enable on boot
sudo systemctl enable docker
```

**Still not working?**
```bash
# Check for permission issues
sudo usermod -aG docker $USER

# Log out and back in, then:
docker info
```

---

### Issue: "docker-compose: command not found"

**Symptoms:**
```
❌ ERROR: docker-compose is not installed!
```

**Cause:** docker-compose is not installed or not in PATH.

**Solution:**

**Docker Desktop (Windows/Mac):**
- docker-compose should come with Docker Desktop
- Reinstall Docker Desktop if missing

**Linux:**
```bash
# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
```

**Alternative (Python pip):**
```bash
pip install docker-compose
```

---

### Issue: "Required file not found"

**Symptoms:**
```
❌ ERROR: Required file 'docker-compose.yaml' not found!
```

**Cause:** Running script from wrong directory.

**Solution:**

```bash
# Check current directory
pwd

# Should be: /path/to/market-mood-ring

# If not, navigate to project root
cd /path/to/market-mood-ring

# Verify files exist
ls -la docker-compose.yaml start_data_pipeline.sh

# Run script
./start_data_pipeline.sh
```

---

## Container Issues

### Issue: KeyError: 'ContainerConfig'

**Symptoms:**
```
KeyError: 'ContainerConfig'
docker-compose up fails
```

**Cause:** Corrupted container metadata from previous runs.

**Solution:**

```bash
# 1. Find corrupted containers
docker ps -a --filter "name=market_" --format "{{.Names}}" | grep -E "^[a-f0-9]{12}_market_"

# 2. Remove them
docker ps -a --filter "name=market_" --format "{{.Names}}" | grep -E "^[a-f0-9]{12}_market_" | xargs docker rm -f

# 3. Clean up networks
docker-compose --profile producers down

# 4. Restart
./start_data_pipeline.sh
```

**The startup script now handles this automatically!**

---

### Issue: Containers Restart Loop

**Symptoms:**
```
docker ps shows "Restarting (1) 30 seconds ago"
```

**Cause:** Container keeps crashing immediately after start.

**Solution:**

```bash
# 1. Check logs for the crashing container
docker logs <container_name> --tail 100

# 2. Common fixes based on error:

# If "NoBrokersAvailable":
# Wait for Kafka to be ready, or restart:
docker-compose restart <container_name>

# If "Connection refused" to PostgreSQL:
docker exec market_postgres pg_isready -U market_user -d market_mood
# If not ready, wait 30 seconds

# If "Permission denied":
# Check volume mounts in docker-compose.yaml

# 3. Force recreate
docker-compose up -d --force-recreate <container_name>
```

---

### Issue: Container Exits Immediately

**Symptoms:**
```
docker ps -a shows "Exited (1) 2 minutes ago"
```

**Cause:** Application error or missing dependencies.

**Solution:**

```bash
# 1. View full logs
docker logs <container_name>

# 2. Check exit code
docker inspect <container_name> --format='{{.State.ExitCode}}'

# Common exit codes:
# 1 - Application error (check logs)
# 137 - Out of memory (increase Docker memory)
# 139 - Segmentation fault (rebuild image)
# 126 - Permission denied
# 127 - Command not found

# 3. For exit code 137 (OOM):
# Increase Docker Desktop memory:
# Settings → Resources → Memory → 8GB+

# 4. Rebuild image
docker-compose build --no-cache <service_name>
docker-compose up -d <service_name>
```

---

## Producer Issues

### Issue: "NoBrokersAvailable"

**Symptoms:**
```
kafka.errors.NoBrokersAvailable: NoBrokersAvailable
Producers exit with code 1
```

**Cause:** Producers started before Kafka was ready.

**Solution:**

**The new startup script handles this automatically with health checks!**

**Manual fix if needed:**
```bash
# 1. Stop everything
docker-compose --profile producers down

# 2. Start infrastructure only
docker-compose up -d kafka postgres jobmanager

# 3. Wait for Kafka (30 seconds)
sleep 30

# 4. Verify Kafka is ready
docker exec market_kafka kafka-broker-api-versions --bootstrap-server localhost:9092

# 5. Start producers
docker-compose --profile producers up -d

# OR just use the script:
./start_data_pipeline.sh
```

---

### Issue: Producers Not Fetching Data

**Symptoms:**
```
docker logs market_news_producer
# Shows no "Published:" messages
```

**Cause:** API key invalid, rate limit, or network issue.

**Solution:**

```bash
# 1. Check API key is valid
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=${FINNHUB_API_KEY}"

# Should return JSON with price data
# If error: "Invalid API key" → Fix .env file

# 2. Check producer logs for errors
docker logs market_news_producer --tail 50

# Common errors:

# "401 Unauthorized" → Invalid API key
nano .env  # Fix FINNHUB_API_KEY

# "429 Too Many Requests" → Rate limited
# Free tier: 60 calls/minute
# Wait 1 minute or upgrade plan

# "Connection timeout" → Network issue
# Check internet connection
curl -I https://finnhub.io

# 3. Restart producers
docker-compose restart news-producer price-producer
```

---

### Issue: Producers Crash After Few Cycles

**Symptoms:**
```
Producers work for 5-10 minutes then exit
```

**Cause:** Memory leak, uncaught exception, or API error.

**Solution:**

```bash
# 1. Check memory usage
docker stats market_news_producer

# If memory constantly increases → Memory leak

# 2. View crash logs
docker logs market_news_producer

# 3. If Python error, check code
nano producer/news_producer.py

# 4. Restart with auto-restart policy
# Edit docker-compose.yaml:
restart: unless-stopped  # Add under producer services

# 5. Apply changes
docker-compose up -d news-producer price-producer
```

---

## Flink Issues

### Issue: Flink Job Not Submitted

**Symptoms:**
```
./bin/flink list
# Shows: "No running jobs"
```

**Cause:** Job failed to submit or crashed.

**Solution:**

```bash
# 1. Check JobManager logs
docker logs market_jobmanager --tail 100

# 2. Manually submit job
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# Look for:
# "Job has been submitted with JobID..." ✅
# "ERROR" or "Exception" ❌

# 3. If submission fails, check Python syntax
docker exec market_jobmanager python3 -m py_compile /opt/flink/usrlib/flink_sentiment.py

# 4. Check NLTK data is downloaded
docker exec market_jobmanager python3 -c "import nltk; nltk.data.find('vader_lexicon')"

# If not found, rebuild Flink image:
docker-compose build --no-cache jobmanager
docker-compose up -d jobmanager taskmanager

# 5. Resubmit
./start_data_pipeline.sh
```

---

### Issue: Flink Job Fails/Crashes

**Symptoms:**
```
Flink UI shows job status: FAILED
Or job disappears from list
```

**Cause:** Exception in processing, Kafka connection lost, or DB error.

**Solution:**

```bash
# 1. Check Flink UI for exception
# Open: http://localhost:8081
# Navigate to: Jobs → Click failed job → Exceptions tab

# 2. Check JobManager logs
docker logs market_jobmanager | grep -i error

# 3. Check TaskManager logs
docker logs market_taskmanager | grep -i error

# Common errors:

# "Topic does not exist" →
docker exec market_kafka kafka-topics --list --bootstrap-server localhost:9092
# Should show: stock_news, stock_prices

# "Connection refused" to Kafka →
docker logs market_kafka
# Check Kafka is healthy

# "Database connection failed" →
docker exec market_postgres pg_isready -U market_user -d market_mood

# 4. Cancel and restart job
docker exec market_jobmanager ./bin/flink cancel <job-id>
./start_data_pipeline.sh
```

---

### Issue: Flink UI Not Accessible

**Symptoms:**
```
http://localhost:8081 not loading
```

**Cause:** JobManager not started or port conflict.

**Solution:**

```bash
# 1. Check JobManager is running
docker ps | grep jobmanager

# If not running:
docker-compose up -d jobmanager

# 2. Check JobManager logs
docker logs market_jobmanager --tail 50

# 3. Verify port mapping
docker port market_jobmanager
# Should show: 8081/tcp -> 0.0.0.0:8081

# 4. Check for port conflict
lsof -i :8081  # Linux/Mac
netstat -ano | findstr :8081  # Windows

# If port in use, change in docker-compose.yaml:
ports:
  - "8082:8081"  # Use different external port

# 5. Restart
docker-compose restart jobmanager

# Access at: http://localhost:8082
```

---

## Database Issues

### Issue: Cannot Connect to PostgreSQL

**Symptoms:**
```
FATAL: password authentication failed
Or: Connection refused
```

**Cause:** Wrong credentials or PostgreSQL not ready.

**Solution:**

```bash
# 1. Check PostgreSQL is running
docker ps | grep postgres

# 2. Check health
docker exec market_postgres pg_isready -U market_user -d market_mood

# If "no response":
docker logs market_postgres --tail 50

# 3. Verify credentials match
cat docker-compose.yaml | grep -A 4 "POSTGRES_"
cat .env | grep POSTGRES  # If using .env

# 4. Test connection
docker exec -it market_postgres psql -U market_user -d market_mood

# If works: Credential issue in application
# If fails: Database issue

# 5. Reset PostgreSQL (CAUTION: Deletes data)
docker-compose stop postgres
docker volume rm market_mood_ring_postgres_data
docker-compose up -d postgres
```

---

### Issue: Tables Not Created

**Symptoms:**
```
psql: ERROR:  relation "stock_prices" does not exist
```

**Cause:** init.sql didn't run or failed.

**Solution:**

```bash
# 1. Check if init.sql exists
cat init.sql

# 2. Check PostgreSQL logs for init errors
docker logs market_postgres | grep -i "error"

# 3. Manually run init.sql
docker exec -i market_postgres psql -U market_user -d market_mood < init.sql

# 4. Verify tables created
docker exec market_postgres psql -U market_user -d market_mood -c "\dt"

# Should list:
# - stock_prices
# - sentiment_log
# - financial_knowledge

# 5. If pgvector extension missing
docker exec market_postgres psql -U market_user -d market_mood -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

### Issue: Database Filling Up Quickly

**Symptoms:**
```
Disk space decreasing rapidly
PostgreSQL volume size growing
```

**Cause:** No data retention policy, too many symbols tracked.

**Solution:**

```bash
# 1. Check database size
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT 
  pg_size_pretty(pg_database_size('market_mood')) as total_size,
  pg_size_pretty(pg_total_relation_size('stock_prices')) as prices_size,
  pg_size_pretty(pg_total_relation_size('sentiment_log')) as sentiment_size;
"

# 2. Check row counts
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT 
  (SELECT COUNT(*) FROM stock_prices) as prices,
  (SELECT COUNT(*) FROM sentiment_log) as sentiment,
  (SELECT COUNT(*) FROM financial_knowledge) as knowledge;
"

# 3. Implement data retention (keep last 7 days)
docker exec market_postgres psql -U market_user -d market_mood -c "
DELETE FROM stock_prices WHERE timestamp < NOW() - INTERVAL '7 days';
DELETE FROM sentiment_log WHERE timestamp < NOW() - INTERVAL '7 days';
VACUUM FULL;
"

# 4. Create cleanup script (add to cron)
cat > cleanup_old_data.sh << 'EOF'
#!/bin/bash
docker exec market_postgres psql -U market_user -d market_mood << SQL
DELETE FROM stock_prices WHERE timestamp < NOW() - INTERVAL '7 days';
DELETE FROM sentiment_log WHERE timestamp < NOW() - INTERVAL '7 days';
VACUUM;
SQL
EOF

chmod +x cleanup_old_data.sh

# Run weekly:
crontab -e
# Add: 0 2 * * 0 /path/to/cleanup_old_data.sh
```

---

## Dashboard Issues

### Issue: Dashboard Not Loading

**Symptoms:**
```
http://localhost:8502 shows "Connection refused"
Or browser hangs loading
```

**Cause:** Dashboard container not running or crashed.

**Solution:**

```bash
# 1. Check dashboard status
docker ps | grep dashboard

# If not running:
docker-compose up -d dashboard

# 2. Check logs
docker logs market_dashboard --tail 50

# Common errors:

# "ModuleNotFoundError" →
docker-compose build --no-cache dashboard
docker-compose up -d dashboard

# "Address already in use" →
# Change port in docker-compose.yaml:
ports:
  - "8503:8501"

# 3. Test from inside container
docker exec market_dashboard curl -s http://localhost:8501

# If works: Port mapping issue
# If fails: Application issue

# 4. Rebuild dashboard
docker-compose build --no-cache dashboard
docker-compose up -d dashboard
```

---

### Issue: Dashboard Shows "No Data Available"

**Symptoms:**
```
Dashboard loads but charts are empty
"No data available" messages
```

**Cause:** Database empty, wrong credentials, or producers not running.

**Solution:**

```bash
# 1. Check if data exists in database
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT COUNT(*) FROM stock_prices;
SELECT COUNT(*) FROM sentiment_log;
"

# If 0 or very low:
# → Producers not running or just started

# 2. Check producers are working
docker logs market_price_producer --tail 20
docker logs market_news_producer --tail 20

# Should see: "Published: AAPL @ $..." messages

# 3. Wait 3-5 minutes for data collection
# Producers fetch every 60 seconds

# 4. Check dashboard database connection
docker logs market_dashboard | grep -i "database\|postgres"

# 5. Verify dashboard environment variables
docker exec market_dashboard env | grep POSTGRES

# Should match docker-compose.yaml settings

# 6. Restart dashboard
docker-compose restart dashboard

# Refresh browser
```

---

### Issue: Dashboard Crashes/Restarts

**Symptoms:**
```
Dashboard keeps restarting
docker ps shows "Restarting" status
```

**Cause:** Python exception, out of memory, or dependency issue.

**Solution:**

```bash
# 1. Check logs for exception
docker logs market_dashboard --tail 100

# 2. Common issues:

# "MemoryError" →
# Increase Docker memory (Settings → Resources)

# "ImportError" or "ModuleNotFoundError" →
# Rebuild with no cache
docker-compose build --no-cache dashboard
docker-compose up -d dashboard

# "Database connection failed" →
# Check PostgreSQL is running
docker ps | grep postgres

# 3. Test dashboard code manually
docker exec -it market_dashboard python3 -c "
import streamlit as st
import psycopg2
print('Imports OK')
"

# 4. Check resource usage
docker stats market_dashboard

# If high memory usage: Optimize queries or increase limits
```

---

## Ollama/AI Issues

### Issue: "Cannot reach Ollama on Windows Host"

**Symptoms:**
```
AI Analyst page shows:
"Cannot reach Ollama. Please ensure Ollama is running..."
```

**Cause:** Ollama not installed, not running, or firewall blocking.

**Solution:**

**Step 1: Install Ollama on Windows**
```powershell
# Download from: https://ollama.com/download
# Run installer
```

**Step 2: Pull Model**
```powershell
ollama pull llama3
```

**Step 3: Configure Network Access**
```powershell
# Set environment variable (Windows)
# Search → "Environment Variables" → System Variables → New

Variable: OLLAMA_HOST
Value: 0.0.0.0:11434

# OR via PowerShell:
[System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'Machine')
```

**Step 4: Restart Ollama**
```powershell
# Close Ollama from system tray
# Restart from Start Menu
```

**Step 5: Configure Firewall**
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "Ollama Allow" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
```

**Step 6: Test from WSL**
```bash
# Should return model list
curl http://$(hostname).local:11434/api/tags

# Or test with Windows IP
curl http://192.168.50.156:11434/api/tags
```

**Step 7: Restart Pipeline**
```bash
docker-compose --profile producers down
./start_data_pipeline.sh
```

---

### Issue: Ollama Responses Very Slow

**Symptoms:**
```
AI Analyst takes 30+ seconds to respond
```

**Cause:** Running on CPU instead of GPU.

**Solution:**

**Check if GPU is available:**
```powershell
# Windows (PowerShell)
nvidia-smi
```

**If you have NVIDIA GPU:**
```powershell
# Ollama should auto-detect GPU
# Check Ollama logs for "CUDA" or "GPU"
```

**If no GPU (expected behavior):**
- CPU inference for llama3 (8B params) takes 20-30 seconds
- This is normal
- Consider using smaller model:
  ```powershell
  ollama pull phi
  ```
  
**Or use cloud LLM:**
- See [docs/setup/LLM_API_INTEGRATION.md](setup/LLM_API_INTEGRATION.md)

---

### Issue: host.docker.internal Not Resolving

**Symptoms:**
```
Dashboard logs: "Connection refused: host.docker.internal:11434"
```

**Cause:** Wrong IP mapping in docker-compose.yaml.

**Solution:**

```bash
# 1. Check what IP host.docker.internal resolves to
docker exec market_dashboard cat /etc/hosts | grep host.docker.internal

# Should show Windows host IP like: 192.168.50.156

# 2. If shows 172.17.0.1 (wrong):
# The startup script should fix this automatically

# 3. Manual fix if needed:
# Stop everything
docker-compose --profile producers down

# Run startup script (sets WINDOWS_HOST_IP)
./start_data_pipeline.sh

# 4. Verify fix
docker exec market_dashboard cat /etc/hosts | grep host.docker.internal
# Should now show correct IP

# 5. Test connectivity
docker exec market_dashboard curl -s http://host.docker.internal:11434/api/tags
# Should return model list
```

---

## Network Issues

### Issue: Ports Already in Use

**Symptoms:**
```
ERROR: for kafka  Cannot start service kafka: 
Bind for 0.0.0.0:9092 failed: port is already allocated
```

**Cause:** Another service using the same port.

**Solution:**

```bash
# 1. Find what's using the port
# Linux/Mac:
lsof -i :9092

# Windows (PowerShell):
netstat -ano | findstr :9092

# 2. Stop conflicting service or change port

# Option A: Kill the process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Option B: Change port in docker-compose.yaml
# Edit and restart
nano docker-compose.yaml
# Change "9092:9092" to "9093:9092"

docker-compose up -d
```

**Common port conflicts:**
- 5432 (PostgreSQL) - Usually other PostgreSQL instance
- 8502 (Dashboard) - Another Streamlit app
- 9092 (Kafka) - Another Kafka instance
- 8081 (Flink) - Another Flink instance
- 11434 (Ollama) - Ollama on different setup

---

### Issue: Containers Can't Communicate

**Symptoms:**
```
Producer logs: "Connection refused: kafka:29092"
```

**Cause:** Containers not on same Docker network.

**Solution:**

```bash
# 1. Check network exists
docker network ls | grep market_network

# 2. Inspect network
docker network inspect market_mood_ring_market_network

# Should list all containers

# 3. If missing or wrong:
docker-compose --profile producers down
docker network prune
./start_data_pipeline.sh

# 4. Verify containers are connected
docker network inspect market_mood_ring_market_network | grep -A 1 "Name"

# Should show: market_kafka, market_postgres, etc.
```

---

## Performance Issues

### Issue: High CPU Usage

**Symptoms:**
```
docker stats shows 100% CPU
System becoming slow
```

**Cause:** Too many containers, inefficient queries, or infinite loop.

**Solution:**

```bash
# 1. Identify culprit
docker stats --no-stream

# 2. Common causes:

# Flink using high CPU (normal during processing)
# → Reduce parallelism in docker-compose.yaml

# Producer using high CPU (abnormal)
# → Check for infinite loop in logs
docker logs market_news_producer --tail 100

# Dashboard using high CPU
# → Optimize database queries
# → Increase auto-refresh interval

# 3. Limit CPU per container
# Edit docker-compose.yaml, add under service:
deploy:
  resources:
    limits:
      cpus: '1.0'

# 4. Restart affected service
docker-compose up -d <service_name>
```

---

### Issue: High Memory Usage

**Symptoms:**
```
docker stats shows high memory
System swapping
```

**Cause:** Memory leak, large datasets, or insufficient Docker allocation.

**Solution:**

```bash
# 1. Check memory usage
docker stats --no-stream

# 2. Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory
# Set to 8GB or more

# 3. Limit per container
# Edit docker-compose.yaml:
deploy:
  resources:
    limits:
      memory: 2G

# 4. Implement database cleanup (see Database Issues)

# 5. Restart containers
docker-compose restart
```

---

## Data Issues

### Issue: Duplicate Data in Database

**Symptoms:**
```
Same timestamp/symbol appears multiple times
```

**Cause:** Producer restarted mid-cycle or no primary key constraint.

**Solution:**

```bash
# 1. Check for duplicates
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT symbol, timestamp, COUNT(*) 
FROM stock_prices 
GROUP BY symbol, timestamp 
HAVING COUNT(*) > 1;
"

# 2. Remove duplicates (keep latest)
docker exec market_postgres psql -U market_user -d market_mood -c "
DELETE FROM stock_prices a USING stock_prices b
WHERE a.id < b.id 
AND a.symbol = b.symbol 
AND a.timestamp = b.timestamp;
"

# 3. Add unique constraint to prevent future duplicates
docker exec market_postgres psql -U market_user -d market_mood -c "
ALTER TABLE stock_prices 
ADD CONSTRAINT unique_symbol_timestamp UNIQUE (symbol, timestamp);
"
```

---

### Issue: Missing Data for Certain Stocks

**Symptoms:**
```
Dashboard shows data for AAPL, MSFT but not TSLA
```

**Cause:** API error for specific symbol or symbol not in list.

**Solution:**

```bash
# 1. Check which symbols are configured
cat producer/tickers.json
# Or check .env:
grep STOCK_SYMBOLS .env

# 2. Check producer logs for errors
docker logs market_news_producer | grep TSLA
docker logs market_price_producer | grep TSLA

# 3. Test API for specific symbol
curl "https://finnhub.io/api/v1/quote?symbol=TSLA&token=${FINNHUB_API_KEY}"

# If error or empty: Symbol might be delisted or API issue

# 4. Check database
docker exec market_postgres psql -U market_user -d market_mood -c "
SELECT DISTINCT symbol FROM stock_prices ORDER BY symbol;
"

# 5. Restart producers to retry
docker-compose restart news-producer price-producer
```

---

## Recovery Procedures

### Full Reset (Nuclear Option)

**⚠️ WARNING: This deletes ALL data!**

```bash
# 1. Stop everything
docker-compose --profile producers down

# 2. Remove volumes (deletes data)
docker volume rm market_mood_ring_postgres_data
docker volume rm market_mood_ring_ollama_data  # If using containerized Ollama

# 3. Remove network
docker network rm market_mood_ring_market_network

# 4. Clean up any orphaned containers
docker container prune -f

# 5. Start fresh
./start_data_pipeline.sh
```

---

### Graceful Restart (Keeps Data)

```bash
# 1. Stop services gracefully
docker-compose --profile producers stop

# 2. Wait for cleanup
sleep 5

# 3. Start again
./start_data_pipeline.sh
```

---

### Rebuild All Images

**Use when code changes or dependencies updated:**

```bash
# 1. Stop everything
docker-compose --profile producers down

# 2. Remove old images
docker-compose rm -f

# 3. Rebuild from scratch
docker-compose build --no-cache

# 4. Start with new images
./start_data_pipeline.sh
```

---

### Reset Just Database (Keep Containers)

```bash
# 1. Stop producers and Flink (to prevent writes)
docker-compose stop news-producer price-producer price-consumer rag-ingest
docker exec market_jobmanager ./bin/flink cancel $(docker exec market_jobmanager ./bin/flink list | grep -oP '(?<=: )\w+')

# 2. Truncate tables
docker exec market_postgres psql -U market_user -d market_mood -c "
TRUNCATE TABLE stock_prices, sentiment_log, financial_knowledge CASCADE;
"

# 3. Restart everything
./start_data_pipeline.sh
```

---

## Getting Additional Help

### Collect Debug Information

When asking for help, provide:

```bash
#!/bin/bash
# Save as collect_debug_info.sh

echo "=== Market Mood Ring Debug Info ===" > debug_info.txt
echo "" >> debug_info.txt

echo "1. System Info:" >> debug_info.txt
uname -a >> debug_info.txt
docker --version >> debug_info.txt
docker-compose --version >> debug_info.txt
echo "" >> debug_info.txt

echo "2. Container Status:" >> debug_info.txt
docker ps --filter "name=market_" >> debug_info.txt
echo "" >> debug_info.txt

echo "3. Recent Logs:" >> debug_info.txt
docker-compose logs --tail=50 >> debug_info.txt
echo "" >> debug_info.txt

echo "4. Environment (sanitized):" >> debug_info.txt
cat .env | grep -v "API_KEY" >> debug_info.txt
echo "" >> debug_info.txt

echo "Debug info saved to debug_info.txt"
cat debug_info.txt
```

---

### Related Documentation

- **Getting Started:** [docs/GETTING_STARTED.md](GETTING_STARTED.md)
- **Architecture:** [docs/architecture/SYSTEM_ARCHITECTURE.md](architecture/SYSTEM_ARCHITECTURE.md)
- **Environment Setup:** [docs/setup/ENV_FILE_GUIDE.md](setup/ENV_FILE_GUIDE.md)
- **Specific Fixes:**
  - [Flink Kafka Fix](troubleshooting/FLINK_KAFKA_CONNECTOR_FIX.md)
  - [PostgreSQL Fix](troubleshooting/FIX_POSTGRES_CREDENTIALS.md)
  - [Dashboard No Data](troubleshooting/DASHBOARD_NO_DATA_TROUBLESHOOTING.md)

---

*Last Updated: February 2026*  
*For questions, create an issue on GitHub*

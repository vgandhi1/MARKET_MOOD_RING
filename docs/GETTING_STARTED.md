# 🚀 Getting Started - Market Mood Ring

**Complete Beginner's Guide to Setting Up and Running the Pipeline**

This guide will walk you through every step needed to get the Market Mood Ring pipeline running, from installation to troubleshooting.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Detailed Setup Guide](#detailed-setup-guide)
4. [Understanding the Components](#understanding-the-components)
5. [Verification & Testing](#verification--testing)
6. [Common Issues & Solutions](#common-issues--solutions)
7. [Next Steps](#next-steps)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose | Installation Link |
|----------|----------------|---------|-------------------|
| **Docker Desktop** | 20.10+ | Run containers | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Python** | 3.9+ | Development & scripts | [python.org](https://www.python.org/downloads/) |
| **Git** | 2.0+ | Clone repository | [git-scm.com](https://git-scm.com/downloads) |
| **WSL2** (Windows) | Latest | Linux environment | [Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/install) |

### System Requirements

- **RAM:** Minimum 8GB (16GB recommended)
- **Disk Space:** 10GB free
- **OS:** Windows 10/11 (WSL2), macOS, or Linux
- **Internet:** Stable connection for API calls

### API Keys Needed

1. **Finnhub API Key** (Required) - FREE
   - Sign up: [https://finnhub.io/register](https://finnhub.io/register)
   - Navigate to Dashboard → API Key
   - Copy your API key (starts with a long string)

2. **Ollama** (Optional - for AI Analyst)
   - Windows: Download from [ollama.com](https://ollama.com/)
   - Enables local AI chatbot feature

---

## Quick Start (5 Minutes)

**For users who want to get running immediately:**

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/market-mood-ring.git
cd market-mood-ring

# 2. Create environment file
cp .env.example .env
nano .env  # Add your FINNHUB_API_KEY

# 3. Start the pipeline
chmod +x start_data_pipeline.sh
./start_data_pipeline.sh

# 4. Open dashboard in browser
# http://localhost:8502
```

**That's it!** The script handles everything automatically.

---

## Detailed Setup Guide

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/market-mood-ring.git

# Navigate to the directory
cd market-mood-ring

# Verify files are present
ls -la
```

**You should see:**
- `docker-compose.yaml`
- `start_data_pipeline.sh`
- `.env.example`
- Directories: `producer/`, `flink_jobs/`, `dashboard/`

---

### Step 2: Set Up Environment Variables

#### 2.1 Create the .env File

```bash
# Copy the example file
cp .env.example .env
```

#### 2.2 Edit with Your API Key

**Option A - Using nano (recommended for beginners):**
```bash
nano .env
```

**Option B - Using vim:**
```bash
vim .env
```

**Option C - Using VS Code:**
```bash
code .env
```

#### 2.3 Configure the File

Edit the `.env` file to look like this:

```bash
# Market Mood Ring - Environment Variables

# ============================================
# PHASE 1: ETL Pipeline (Required)
# ============================================

# Finnhub API Key (REQUIRED - Replace with your actual key)
FINNHUB_API_KEY=your_actual_api_key_here_from_finnhub

# Optional: Custom Stock Symbols (comma-separated)
# Leave blank to use default 6 stocks
# STOCK_SYMBOLS=AAPL,MSFT,TSLA,GOOGL,AMZN,RIVN

# ============================================
# PHASE 2: LLM Integration (Optional)
# ============================================

# Default: Use local Ollama
LLM_PROVIDER=ollama
```

**Save and exit:**
- In nano: Press `Ctrl+X`, then `Y`, then `Enter`
- In vim: Press `Esc`, type `:wq`, press `Enter`

#### 2.4 Verify Your API Key

```bash
# Check that the key is set (should show your actual key)
grep FINNHUB_API_KEY .env
```

**✅ Good:** `FINNHUB_API_KEY=abcdef123456789...`  
**❌ Bad:** `FINNHUB_API_KEY=your_key_here` (still placeholder)

---

### Step 3: Start Docker Desktop

#### Windows (WSL2)
1. Launch Docker Desktop from Start Menu
2. Wait for "Docker Desktop is running" notification
3. Verify in WSL terminal:
   ```bash
   docker info
   ```

#### macOS
1. Launch Docker Desktop from Applications
2. Wait for whale icon in menu bar to stop animating
3. Verify in terminal:
   ```bash
   docker info
   ```

#### Linux
```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot (optional)
sudo systemctl enable docker

# Verify
docker info
```

---

### Step 4: Start the Pipeline

#### 4.1 Make the Script Executable

```bash
chmod +x start_data_pipeline.sh
```

#### 4.2 Run the Startup Script

```bash
./start_data_pipeline.sh
```

**What happens:**

```
🚀 Starting Market Mood Ring Data Pipeline
==========================================

📋 Step 1/6: Running pre-flight checks...
   ✅ All pre-flight checks passed

📋 Step 2/6: Detecting Windows Host IP for Ollama connection...
   ✅ Resolved host.docker.internal to: 192.168.50.156

📋 Step 3/6: Checking for old containers...
   ✅ No cleanup needed

📋 Step 4/6: Starting all services...
   Creating network...
   Creating market_kafka
   Creating market_postgres
   ...
   ✅ Docker containers started

📋 Step 5/6: Waiting for services to become healthy...
   ✅ Kafka is ready
   ✅ PostgreSQL is ready
   ✅ Flink JobManager is ready

📋 Step 6/6: Checking Flink job status...
   ✅ Flink sentiment job submitted successfully

================================================================
✅ Pipeline is fully active!
================================================================

📊 Service Status:
   market_dashboard: Up 2 minutes
   market_kafka: Up 2 minutes (healthy)
   market_news_producer: Up 2 minutes
   ...

🔗 Access Points:
   📊 Dashboard:    http://localhost:8502
   🌊 Flink UI:     http://localhost:8081
   🗄️  PostgreSQL:   localhost:5432
   📨 Kafka:        localhost:9092
```

**⏱️ Total time: 2-3 minutes** (first run may take longer to download images)

---

### Step 5: Access the Dashboard

#### 5.1 Open Your Browser

Navigate to: **http://localhost:8502**

#### 5.2 Explore the Dashboard

**Page 1: 📊 Live Dashboard**
- Real-time price charts (72-hour history)
- Sentiment scores for each stock
- Latest news headlines with sentiment analysis
- Auto-refreshes every 30 seconds

**Page 2: 💬 AI Analyst** (if Ollama is configured)
- Ask questions about market movements
- Get AI-powered analysis
- Example: "Why is TSLA moving today?"

---

## Understanding the Components

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR PIPELINE                         │
└─────────────────────────────────────────────────────────┘

1. DATA SOURCES
   └─ Finnhub API → News & Prices

2. INGESTION LAYER (Python Producers)
   ├─ news_producer.py    → Fetches news every 60s
   ├─ price_producer.py   → Fetches prices every 60s
   └─ rag_ingest.py       → Creates embeddings for AI

3. MESSAGE QUEUE
   └─ Apache Kafka → Streams data

4. PROCESSING LAYER
   └─ Apache Flink → Sentiment analysis (NLTK)

5. STORAGE LAYER
   └─ PostgreSQL → Stores everything

6. AI LAYER (Optional)
   └─ Ollama (Llama 3) → Chatbot

7. UI LAYER
   └─ Streamlit Dashboard → Visualization
```

### What Each Container Does

| Container | Purpose | Port | Status Check |
|-----------|---------|------|--------------|
| `market_kafka` | Message broker | 9092 | `docker logs market_kafka` |
| `market_postgres` | Database | 5432 | `docker exec market_postgres pg_isready` |
| `market_jobmanager` | Flink coordinator | 8081 | http://localhost:8081 |
| `market_taskmanager` | Flink worker | - | Check JobManager UI |
| `market_news_producer` | Fetches news | - | `docker logs market_news_producer` |
| `market_price_producer` | Fetches prices | - | `docker logs market_price_producer` |
| `market_price_consumer` | Saves prices to DB | - | `docker logs market_price_consumer` |
| `market_rag_ingest` | Creates embeddings | - | `docker logs market_rag_ingest` |
| `market_dashboard` | Web UI | 8502 | http://localhost:8502 |

---

## Verification & Testing

### Check All Services Are Running

```bash
# View all containers
docker ps --filter "name=market_"

# Should show 9 containers with status "Up"
```

### Check Producer Logs

```bash
# View news producer (should show "Cycle complete")
docker logs market_news_producer --tail 20

# View price producer (should show "Published: AAPL @ $...")
docker logs market_price_producer --tail 20
```

**✅ Good Output:**
```
✅ Published: AAPL @ $274.62
✅ Published: MSFT @ $413.60
⏳ Waiting 60 seconds before next fetch cycle...
```

### Check Flink Job

```bash
# List running Flink jobs
docker exec market_jobmanager ./bin/flink list

# Should show: insert-into_default_catalog.default_database.sentiment_sink (RUNNING)
```

### Check Database

```bash
# Connect to PostgreSQL
docker exec -it market_postgres psql -U market_user -d market_mood

# Run queries
SELECT COUNT(*) FROM stock_prices;      -- Should show increasing count
SELECT COUNT(*) FROM sentiment_log;     -- Should show data after a few minutes
SELECT COUNT(*) FROM financial_knowledge;  -- Should show embedded news

# Exit
\q
```

### Test API Connectivity

```bash
# Test Finnhub API (should return stock data)
curl -s "https://finnhub.io/api/v1/quote?symbol=AAPL&token=${FINNHUB_API_KEY}" | python3 -m json.tool
```

---

## Common Issues & Solutions

### Issue 1: "FINNHUB_API_KEY is not set"

**Cause:** The .env file doesn't have a valid API key.

**Solution:**
```bash
# Open .env file
nano .env

# Make sure you have:
FINNHUB_API_KEY=your_actual_key_from_finnhub_dashboard

# NOT:
FINNHUB_API_KEY=your_key_here  # ❌ This is a placeholder!
```

---

### Issue 2: "Docker is not running"

**Cause:** Docker Desktop is not started.

**Solution:**
```bash
# Windows/Mac: Launch Docker Desktop application
# Wait for it to fully start (whale icon stops animating)

# Linux: Start Docker service
sudo systemctl start docker

# Verify
docker info
```

---

### Issue 3: "NoBrokersAvailable" Error

**Cause:** Producers started before Kafka was ready.

**Solution:**
```bash
# The new script handles this automatically, but if you see this:

# Stop everything
docker-compose --profile producers down

# Start again using the script
./start_data_pipeline.sh
```

---

### Issue 4: "Cannot reach Ollama" (AI Analyst)

**Cause:** Ollama is not running on Windows host or firewall is blocking.

**Solution:**

1. **Install Ollama on Windows:**
   ```powershell
   # Download from: https://ollama.com/
   ```

2. **Pull the model:**
   ```powershell
   ollama pull llama3
   ```

3. **Configure network access:**
   ```powershell
   # Set environment variable (Windows)
   setx OLLAMA_HOST "0.0.0.0:11434"
   
   # Restart Ollama service
   ```

4. **Allow firewall:**
   ```powershell
   # Run as Administrator
   New-NetFirewallRule -DisplayName "Ollama Allow" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
   ```

5. **Restart the dashboard:**
   ```bash
   docker-compose restart dashboard
   ```

---

### Issue 5: Port 8502 Already in Use

**Cause:** Another application is using port 8502.

**Solution:**

**Option A - Change the port:**
```bash
# Edit docker-compose.yaml
nano docker-compose.yaml

# Find dashboard service, change:
ports:
  - "8503:8501"  # Changed from 8502

# Restart
docker-compose restart dashboard

# Access at http://localhost:8503
```

**Option B - Stop the conflicting service:**
```bash
# Find what's using the port
lsof -i :8502  # Linux/Mac
netstat -ano | findstr :8502  # Windows

# Stop that process
```

---

### Issue 6: No Data Showing in Dashboard

**Cause:** Producers haven't collected data yet, or database connection failed.

**Solution:**

1. **Wait 2-3 minutes** for initial data collection
2. **Check producer logs:**
   ```bash
   docker logs market_price_producer --tail 20
   docker logs market_news_producer --tail 20
   ```
3. **Verify database has data:**
   ```bash
   docker exec market_postgres psql -U market_user -d market_mood -c "SELECT COUNT(*) FROM stock_prices;"
   ```
4. **Check dashboard logs:**
   ```bash
   docker logs market_dashboard
   ```

---

## Next Steps

### 1. Customize Stock Symbols

Edit `.env` to track your favorite stocks:

```bash
STOCK_SYMBOLS=NVDA,AMD,INTC,AAPL,GOOGL
```

Then restart:
```bash
docker-compose restart news-producer price-producer
```

### 2. Set Up Ollama for AI Analyst

Follow the guide: [docs/setup/LLM_API_INTEGRATION.md](setup/LLM_API_INTEGRATION.md)

### 3. Monitor with Flink UI

- **URL:** http://localhost:8081
- **View:** Job graphs, metrics, task managers
- **Debug:** Check for backpressure or failures

### 4. Explore the Database

```bash
# Connect to database
docker exec -it market_postgres psql -U market_user -d market_mood

# Useful queries:
\dt                    # List all tables
\d+ stock_prices       # Describe table schema
SELECT * FROM sentiment_log ORDER BY timestamp DESC LIMIT 10;
```

### 5. Scale the Pipeline

Increase Flink parallelism in `docker-compose.yaml`:

```yaml
environment:
  - |
    FLINK_PROPERTIES=
    taskmanager.numberOfTaskSlots: 4  # Increase from 2
    parallelism.default: 2             # Increase from 1
```

---

## Useful Commands Reference

### Start & Stop

```bash
# Start everything
./start_data_pipeline.sh

# Stop everything
docker-compose --profile producers down

# Stop but keep data
docker-compose --profile producers stop

# Restart a specific service
docker-compose restart news-producer
```

### Monitoring

```bash
# View all logs (follow mode)
docker-compose logs -f

# View specific service logs
docker logs market_news_producer -f

# View last N lines
docker logs market_kafka --tail 50

# Check container status
docker ps --filter "name=market_"

# Check resource usage
docker stats
```

### Troubleshooting

```bash
# Check Flink jobs
docker exec market_jobmanager ./bin/flink list

# Restart Flink job
docker exec market_jobmanager ./bin/flink cancel <job-id>
./start_data_pipeline.sh  # Resubmits automatically

# Connect to database
docker exec -it market_postgres psql -U market_user -d market_mood

# Test Kafka
docker exec market_kafka kafka-topics --list --bootstrap-server localhost:9092

# Remove all containers and start fresh
docker-compose --profile producers down -v
./start_data_pipeline.sh
```

---

## Getting Help

### Documentation

- **Main README:** [README.md](../README.md)
- **Architecture:** [docs/architecture/SYSTEM_ARCHITECTURE.md](architecture/SYSTEM_ARCHITECTURE.md)
- **Troubleshooting:** [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Environment Setup:** [docs/setup/ENV_FILE_GUIDE.md](setup/ENV_FILE_GUIDE.md)

### Common Resources

- **Finnhub API Docs:** https://finnhub.io/docs/api
- **Docker Docs:** https://docs.docker.com/
- **Flink Docs:** https://flink.apache.org/
- **Ollama Docs:** https://github.com/ollama/ollama

### Debug Logs

When reporting issues, include:

```bash
# System info
docker --version
docker-compose --version
python3 --version

# Container status
docker ps --filter "name=market_"

# Relevant logs
docker logs market_news_producer --tail 100
docker logs market_kafka --tail 50
```

---

## Success Checklist

✅ Docker Desktop is running  
✅ `.env` file created with valid `FINNHUB_API_KEY`  
✅ All 9 containers are running (`docker ps`)  
✅ Producers are fetching data (check logs)  
✅ Flink job is running (check http://localhost:8081)  
✅ Dashboard is accessible (http://localhost:8502)  
✅ Data is appearing in the dashboard  

**If all checked: You're ready to analyze the market! 🎉**

---

*Last Updated: February 2026*  
*For questions or issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)*

# 🚀 Setup Workflow

**⚠️ Note:** This is an older workflow guide. For the most up-to-date setup instructions, see **[GETTING_STARTED.md](../GETTING_STARTED.md)**.

---

## ✅ Recommended Setup (2026 Method)

**Use the automated startup script:**

```bash
# 1. Create .env file
cp .env.example .env
nano .env  # Add your FINNHUB_API_KEY

# 2. Run the startup script
./start_data_pipeline.sh
```

**That's it!** The script handles everything automatically.

See [GETTING_STARTED.md](../GETTING_STARTED.md) for detailed instructions.

---

## Alternative Setup Methods

### Method 1: Docker Compose with Profiles (Manual)

```bash
# 1. Setup environment variables
cp .env.example .env
# Edit .env and add FINNHUB_API_KEY

# 2. Start all services (infrastructure + producers)
docker-compose --profile producers up -d

# 3. Wait for services to be ready (30-60 seconds)
sleep 60

# 4. Submit Flink job manually
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# 5. Access dashboard
# http://localhost:8502
```

### Method 2: Local Development + Docker

```bash
# 1. Create virtual environment (optional, for local development)
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# 2. Install dependencies (optional, for local development)
pip install -r requirements.txt

# 3. Setup .env
cp .env.example .env
# Edit and add FINNHUB_API_KEY

# 4. Start Docker containers
docker-compose --profile producers up -d

# 5. Submit Flink job
docker exec market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

---

## ⚠️ Original UV Workflow (Deprecated)

**Note:** UV setup is no longer required. The Docker containers handle all dependencies.

<details>
<summary>Click to view original UV workflow (for reference only)</summary>

### Step 1: Create Virtual Environment with UV

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### Step 2: Install Python Packages

```bash
# Install all dependencies from requirements.txt
uv pip install -r requirements.txt

# Verify installation
pip list
```

### Step 3: Setup Environment Variables

```bash
# Create .env file
cat > .env << EOF
FINNHUB_API_KEY=your_finnhub_api_key_here
STOCK_SYMBOLS=AAPL,MSFT,TSLA,GOOGL,AMZN
EOF
```

### Step 4: Start Docker Containers

```bash
# Build and start all services
docker-compose up -d --build
```

### Step 5: Run Producers

```bash
# Terminal 1 - News Producer
docker-compose run --rm producer python news_producer.py

# Terminal 2 - Price Producer
docker-compose run --rm producer python price_producer.py

# Terminal 3 - Price Consumer
docker-compose run --rm producer python price_consumer.py
```

</details>

---

## Why Use the Startup Script?

### ✅ Advantages of `./start_data_pipeline.sh`:
- **Automated** - All steps handled for you
- **Validation** - Checks .env, files, Docker status
- **Sequencing** - Waits for services to be healthy
- **Error Handling** - Clear error messages
- **Flink Job** - Automatically submitted
- **Status Reporting** - Shows what's running

### ⚠️ Manual Docker Compose Issues:
- No pre-flight checks
- Race conditions (producers before Kafka ready)
- Manual Flink job submission required
- No IP detection for Ollama
- Generic error messages

See [DOCKER_VS_SCRIPT_GUIDE.md](../DOCKER_VS_SCRIPT_GUIDE.md) for detailed comparison.

---

## Development Workflow

### Local Testing (Optional)

If you want to test scripts locally before Docker:

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Test locally (requires Kafka running)
python producer/news_producer.py
python producer/price_producer.py

# 4. Run dashboard locally
streamlit run dashboard/app.py
```

### Docker Deployment

```bash
# Use the startup script (recommended)
./start_data_pipeline.sh

# OR manual docker-compose (see Method 1 above)
```

---

## File Structure After Setup

```
Market_Mood_Ring/
├── .env                      # Your environment variables (created)
├── .env.example              # Template
├── requirements.txt          # Python dependencies
├── start_data_pipeline.sh    # ⭐ Startup script (use this!)
├── docker-compose.yaml       # Docker orchestration
│
├── producer/                 # Data ingestion
│   ├── news_producer.py
│   ├── price_producer.py
│   ├── price_consumer.py
│   └── rag_ingest.py
│
├── flink_jobs/               # Stream processing
│   └── flink_sentiment.py
│
├── dashboard/                # UI
│   └── app.py
│
└── docs/                     # Documentation
    ├── GETTING_STARTED.md    # ⭐ Modern guide
    └── ...
```

---

## Summary

**Recommended Approach (2026):**
1. ✅ Create `.env` with FINNHUB_API_KEY
2. ✅ Run `./start_data_pipeline.sh`
3. ✅ Access dashboard at http://localhost:8502

**Benefits:**
- ✅ Fast setup (2-3 minutes)
- ✅ Automated validation
- ✅ Proper service sequencing
- ✅ Clear status reporting

**For detailed walkthrough:** [GETTING_STARTED.md](../GETTING_STARTED.md)  
**For troubleshooting:** [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

---

*Last Updated: February 2026*  
*Status: Modernized with startup script*

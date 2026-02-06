# 🚀 Setup Workflow - UV + Docker

## Recommended Setup Process

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

---

## Why This Workflow?

### UV for Local Development:
- ✅ **Fast installation** - UV is 10-100x faster than pip
- ✅ **Local testing** - Test scripts locally before Docker
- ✅ **IDE support** - Better autocomplete and type checking
- ✅ **Development workflow** - Edit code, test locally, then deploy

### Docker for Deployment:
- ✅ **Consistent environment** - Same setup everywhere
- ✅ **Isolation** - No conflicts with system Python
- ✅ **Production ready** - Containerized deployment
- ✅ **Service orchestration** - All services managed together

---

## Quick Setup Script

Use the provided `setup.sh` script:

```bash
# Make executable
chmod +x setup.sh

# Run setup
./setup.sh
```

This will:
1. Check if UV is installed (install if needed)
2. Create virtual environment
3. Install all dependencies
4. Show next steps

---

## Development Workflow

### Local Development (UV):
```bash
# Activate venv
source .venv/bin/activate

# Test scripts locally (from project root with venv activated)
python producer/news_producer.py
python producer/price_producer.py

# Run dashboard locally
streamlit run dashboard/app.py
```

### Docker Deployment:
```bash
# Start infrastructure
docker-compose up -d

# Run producers in containers (files are mounted to /app/)
docker-compose run --rm producer python news_producer.py
```

---

## Benefits of This Approach

1. **Local Development:**
   - Fast iteration with UV
   - Test changes quickly
   - Better debugging experience

2. **Docker Deployment:**
   - Consistent production environment
   - All services orchestrated
   - Easy scaling and management

3. **Best of Both Worlds:**
   - Develop locally with UV
   - Deploy with Docker
   - Same dependencies in both

---

## File Structure After Setup

```
Market_Mood_Ring/
├── .venv/                    # UV virtual environment (created)
│   └── lib/python3.9/site-packages/  # Installed packages
├── .env                      # Environment variables (create this)
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script
└── ...
```

---

## Summary

**Workflow:**
1. ✅ Create venv with UV
2. ✅ Install requirements.txt with UV
3. ✅ Setup .env file
4. ✅ Run docker-compose

**Benefits:**
- Fast local development
- Consistent Docker deployment
- Best practices for Python projects

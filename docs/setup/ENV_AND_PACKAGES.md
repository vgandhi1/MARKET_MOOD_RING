# 🔑 Environment Variables & Packages Quick Reference

## Environment Variables (Configuration)

### What They Are:
- **Configuration values** (API keys, database credentials, etc.)
- **NOT installed packages** - just settings passed to containers

### Where They're Defined:

1. **`.env` file** (project root) - Create this file:
   ```bash
   FINNHUB_API_KEY=your_key_here
   STOCK_SYMBOLS=AAPL,MSFT,TSLA
   ```

2. **docker-compose.yaml** - Reads from `.env` and passes to containers:
   ```yaml
   environment:
     - FINNHUB_API_KEY=${FINNHUB_API_KEY}  # From .env file
   ```

### How They're Used:
- Passed to containers at **runtime** (when container starts)
- Available as environment variables inside containers
- Accessed in Python: `os.getenv('FINNHUB_API_KEY')`

---

## Python Packages (Dependencies)

### What They Are:
- **Libraries and frameworks** (streamlit, pandas, kafka-python, etc.)
- **Installed** into the container during image build

### Where They're Defined:

**`requirements.txt`** (project root):
```txt
streamlit>=1.28.0
pandas>=2.0.0
psycopg2-binary>=2.9.9
kafka-python>=2.0.2
sentence-transformers>=2.2.2
requests>=2.31.0
plotly>=5.17.0
```

### How They're Installed:

**During Docker image build** (in Dockerfile):
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

**Installation location:** `/usr/local/lib/python3.9/site-packages/` inside container

---

## Installation Locations Summary

| Item | Location | When Installed |
|------|----------|----------------|
| **Environment Variables** | `.env` file → Container environment | Runtime (container start) |
| **Python Packages** | `requirements.txt` → `/usr/local/lib/python3.9/site-packages/` | Build time (image creation) |
| **System Packages** | `/usr/bin/`, `/usr/lib/` | Build time (image creation) |
| **Application Code** | `/app/` | Build time (image creation) |

---

## Streamlit Installation Details

### Where:
- **Package:** `/usr/local/lib/python3.9/site-packages/streamlit/`
- **CLI:** `/usr/local/bin/streamlit`

### How:
1. Listed in `requirements.txt`: `streamlit>=1.28.0`
2. Installed during Docker build: `pip install -r requirements.txt`
3. Available when container runs

### Verification:
```bash
# Check Streamlit is installed
docker exec -it market_dashboard pip list | grep streamlit

# Check Streamlit version
docker exec -it market_dashboard python3 -c "import streamlit; print(streamlit.__version__)"

# Check Streamlit location
docker exec -it market_dashboard python3 -c "import streamlit; print(streamlit.__file__)"
```

---

## Complete Setup Flow

### 1. Create `.env` file:
```bash
FINNHUB_API_KEY=your_key_here
```

### 2. Build images (installs packages):
```bash
docker-compose build
# or
docker-compose up -d --build
```

**What happens:**
- Reads `requirements.txt`
- Installs all Python packages into image
- Streamlit, pandas, kafka-python, etc. are installed

### 3. Start containers (loads environment variables):
```bash
docker-compose up -d
```

**What happens:**
- Reads `.env` file
- Passes environment variables to containers
- Containers start with packages already installed

---

## Key Differences

| Aspect | Environment Variables | Python Packages |
|--------|---------------------|-----------------|
| **Purpose** | Configuration | Dependencies |
| **File** | `.env` | `requirements.txt` |
| **When** | Runtime | Build time |
| **Where** | Container environment | `/usr/local/lib/python3.9/site-packages/` |
| **Example** | `FINNHUB_API_KEY=abc123` | `streamlit>=1.28.0` |

---

## Summary

1. ✅ **Environment packages:** Yes, we have `requirements.txt` with all Python packages
2. ✅ **Installation location:** Inside Docker containers at `/usr/local/lib/python3.9/site-packages/`
3. ✅ **Streamlit:** Installed via `pip install streamlit` during Docker build
4. ✅ **Environment variables:** Defined in `.env` file, passed at runtime

See `INSTALLATION_EXPLAINED.md` for detailed explanation.

# 📦 Installation Explained

## Question 1: Don't we have environment packages?

### Answer: **Yes! We have `requirements.txt` with all Python packages**

**Location:** `requirements.txt` (project root)

**Contents:**
```txt
# Core dependencies
requests>=2.31.0
pandas>=2.0.0

# Database
psycopg2-binary>=2.9.9

# Kafka
kafka-python>=2.0.2

# Vector embeddings (Phase 2: RAG)
sentence-transformers>=2.2.2

# Dashboard
streamlit>=1.28.0
plotly>=5.17.0
```

**Note:** This is a **consolidated** requirements file used by both producer and dashboard services.

---

## Question 2: Where are we installing packages in docker-compose containers?

### Answer: **Inside Docker containers, during image build**

### Installation Process:

#### Step 1: Docker Build (Image Creation)

When you run `docker-compose up -d --build`:

1. **Dashboard Container:**
   ```dockerfile
   # From dashboard/Dockerfile
   FROM python:3.9-slim          # Base image with Python 3.9
   WORKDIR /app                   # Set working directory to /app
   
   # Install system packages (apt-get)
   RUN apt-get update && \
       apt-get install -y gcc postgresql-client
   
   # Install Python packages (pip)
   COPY requirements.txt .        # Copy requirements.txt to /app/
   RUN pip install -r requirements.txt  # Install packages in /app/
   ```

2. **Producer Container:**
   ```dockerfile
   # From producer/Dockerfile
   FROM python:3.9-slim          # Base image with Python 3.9
   WORKDIR /app                   # Set working directory to /app
   
   # Install system packages (apt-get)
   RUN apt-get update && \
       apt-get install -y gcc postgresql-client
   
   # Install Python packages (pip)
   COPY requirements.txt .        # Copy requirements.txt to /app/
   RUN pip install -r requirements.txt  # Install packages in /app/
   ```

### Installation Locations:

| Package Type | Installation Location | How |
|-------------|---------------------|-----|
| **System packages** (gcc, postgresql-client) | `/usr/bin/`, `/usr/lib/` | `apt-get install` |
| **Python packages** (streamlit, pandas, etc.) | `/usr/local/lib/python3.9/site-packages/` | `pip install` |
| **Application code** | `/app/` | `COPY` command |

### Where Packages Are Installed:

```
Container Filesystem:
├── /app/                          # Working directory
│   ├── app.py (dashboard)         # Application code
│   └── *.py (producer)            # Application code
│
├── /usr/local/lib/python3.9/      # Python installation
│   └── site-packages/              # Python packages installed here
│       ├── streamlit/              # Streamlit package
│       ├── pandas/                 # Pandas package
│       ├── psycopg2/               # PostgreSQL driver
│       └── ...                     # All other packages
│
└── /usr/bin/                       # System binaries
    ├── python3                     # Python interpreter
    ├── pip                         # pip installer
    └── gcc                         # C compiler
```

### Installation Happens During:

1. **Image Build** (`docker-compose build` or `docker-compose up --build`)
   - Packages are installed **inside the image**
   - Image is saved to Docker's image cache
   - Can be reused for multiple containers

2. **Container Runtime**
   - Packages are **already installed** in the image
   - No installation happens when container starts
   - Container just runs the application

---

## Question 3: Where and how is Streamlit installed?

### Answer: **Installed via pip during Docker image build**

### Streamlit Installation Process:

#### Step-by-Step:

1. **Base Image:**
   ```dockerfile
   FROM python:3.9-slim
   ```
   - Provides Python 3.9 and pip
   - Location: `/usr/local/bin/python3`

2. **Copy Requirements:**
   ```dockerfile
   COPY requirements.txt .
   ```
   - Copies `requirements.txt` to `/app/requirements.txt` in container

3. **Install Streamlit:**
   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```
   - Reads `requirements.txt` which contains `streamlit>=1.28.0`
   - Downloads and installs Streamlit from PyPI
   - Installs to: `/usr/local/lib/python3.9/site-packages/streamlit/`

4. **Verify Installation:**
   ```bash
   # Inside container
   python3 -c "import streamlit; print(streamlit.__version__)"
   # Output: 1.28.0 (or higher)
   ```

### Streamlit Installation Location:

```
Container: market_dashboard
├── /usr/local/lib/python3.9/site-packages/
│   └── streamlit/                    # Streamlit package
│       ├── __init__.py
│       ├── _config.py
│       ├── _main.py
│       └── ...                        # All Streamlit modules
│
└── /usr/local/bin/
    └── streamlit                       # Streamlit CLI command
```

### How Streamlit Runs:

```dockerfile
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**What happens:**
1. Container starts
2. Executes: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
3. Streamlit CLI (installed in `/usr/local/bin/streamlit`) runs
4. Streamlit server starts on port 8501
5. Accessible at `http://localhost:8502` (mapped from container port 8501)

---

## Complete Installation Flow

### For Dashboard:

```
1. docker-compose up -d --build
   ↓
2. Docker reads dashboard/Dockerfile
   ↓
3. Builds image: market_mood_ring-dashboard
   ├── Installs system packages (gcc, postgresql-client)
   ├── Copies requirements.txt
   ├── Installs Python packages (streamlit, pandas, plotly, etc.)
   └── Copies app.py
   ↓
4. Creates container from image
   ↓
5. Container runs: streamlit run app.py
   ↓
6. Streamlit server starts on port 8501
   ↓
7. Accessible at http://localhost:8502
```

### For Producer:

```
1. docker-compose run producer python news_producer.py
   ↓
2. Docker reads producer/Dockerfile
   ↓
3. Builds image: market_mood_ring-producer (if not exists)
   ├── Installs system packages (gcc, postgresql-client)
   ├── Copies requirements.txt
   ├── Installs Python packages (kafka-python, psycopg2, etc.)
   └── Copies *.py files
   ↓
4. Creates container from image
   ↓
5. Container runs: python news_producer.py
   ↓
6. Script executes using installed packages
```

---

## Environment Variables vs Packages

### Environment Variables (`.env` file):
- **Purpose:** Configuration (API keys, database credentials)
- **Location:** Project root `.env` file
- **Usage:** Passed to containers via `environment:` in docker-compose.yaml
- **Example:**
  ```bash
  FINNHUB_API_KEY=your_key_here
  POSTGRES_DB=market_mood
  ```

### Python Packages (`requirements.txt`):
- **Purpose:** Dependencies (libraries, frameworks)
- **Location:** Project root `requirements.txt`
- **Usage:** Installed via `pip install -r requirements.txt` in Dockerfile
- **Example:**
  ```txt
  streamlit>=1.28.0
  pandas>=2.0.0
  ```

---

## Summary

1. **Environment packages:** ✅ Yes, `requirements.txt` contains all Python packages
2. **Installation location:** Inside Docker containers at `/usr/local/lib/python3.9/site-packages/`
3. **Streamlit installation:** Via `pip install streamlit` during Docker image build
4. **When installed:** During `docker-compose build` or `docker-compose up --build`
5. **Where installed:** In the Docker image, reused by all containers from that image

---

## Verification Commands

### Check installed packages in container:
```bash
# Dashboard container
docker exec -it market_dashboard pip list

# Producer container
docker exec -it market_producer pip list
```

### Check Streamlit version:
```bash
docker exec -it market_dashboard python3 -c "import streamlit; print(streamlit.__version__)"
```

### Check where packages are installed:
```bash
docker exec -it market_dashboard python3 -c "import streamlit; print(streamlit.__file__)"
# Output: /usr/local/lib/python3.9/site-packages/streamlit/__init__.py
```

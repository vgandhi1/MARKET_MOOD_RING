# 🤔 Why Docker Installs Packages Through requirements.txt

## The Core Question

**"We already installed packages with UV venv, why does Docker install them again?"**

## Answer: **Docker Containers Have Separate Python Environments**

### Two Separate Environments:

1. **Your Host Machine (UV venv):**
   - Location: `./venv/` on your computer
   - Purpose: Local development and testing
   - Access: You can run scripts directly: `python producer/news_producer.py` (from project root)

2. **Docker Container:**
   - Location: Inside the container (`/usr/local/lib/python3.9/site-packages/`)
   - Purpose: Isolated, consistent runtime environment
   - Access: Only accessible from inside the container

### They Don't Share Packages!

```
Your Computer:
├── .venv/                    # UV virtual environment
│   └── lib/python3.9/site-packages/  # Packages installed here
│       ├── streamlit/
│       ├── pandas/
│       └── ...
│
└── Docker Container (market_dashboard):
    └── /usr/local/lib/python3.9/site-packages/  # Separate location!
        ├── streamlit/        # Must be installed here too
        ├── pandas/           # Must be installed here too
        └── ...
```

### Why This Separation?

✅ **Isolation:** Container can't access your host's Python packages  
✅ **Consistency:** Same packages in container regardless of host setup  
✅ **Portability:** Container works the same on any machine  
✅ **Reproducibility:** Exact same environment every time  

---

## The Installation Process

### When You Run `docker-compose up -d --build`:

1. **Docker reads Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim          # Fresh Python 3.9 (no packages)
   COPY requirements.txt .        # Copy requirements file
   RUN pip install -r requirements.txt  # Install packages INSIDE container
   ```

2. **Creates a NEW Python environment:**
   - Starts with base Python image (no packages)
   - Installs packages from `requirements.txt`
   - Packages go into container's Python environment

3. **Your UV venv is NOT used:**
   - Docker doesn't know about your `.venv/` directory
   - Container has its own isolated filesystem
   - Must install packages separately

---

## Why Both Are Needed

### UV venv (Local Development):
- ✅ Fast iteration
- ✅ Test code locally
- ✅ IDE autocomplete
- ✅ Debugging

### Docker (Deployment):
- ✅ Consistent environment
- ✅ Production-ready
- ✅ Isolated from host
- ✅ Same setup everywhere

---

## Current Issue: Timeout During Docker Build

The build is failing because it's trying to download **PyTorch (torch)** - a huge package (888 MB) that times out.

**Root Cause:** `sentence-transformers` requires `torch`, but `sentence-transformers` is only needed for **Phase 2** (RAG pipeline).

**Solution:** Split requirements into Phase 1 and Phase 2, or make Phase 2 dependencies optional.

---

## Summary

1. **Docker installs packages** because containers have separate Python environments
2. **Your UV venv** is on your host machine, containers can't access it
3. **Both are needed:** UV for local dev, Docker for deployment
4. **Current issue:** Phase 2 dependencies (sentence-transformers/torch) causing timeout

**Think of it like this:**
- UV venv = Your local workspace
- Docker container = A separate computer that needs its own setup

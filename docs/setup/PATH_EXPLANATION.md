# 📁 Path Explanation: Why `producer/` vs Direct Path?

## The Issue

You ran:
```bash
docker-compose run --rm producer python producer/news_producer.py
# Error: can't open file '/app/producer/news_producer.py'
```

But the correct command is:
```bash
docker-compose run --rm producer python news_producer.py
```

## Why?

### Volume Mount Override

In `docker-compose.yaml`:
```yaml
producer:
  volumes:
    - ./producer:/app  # ← Mounts producer directory to /app
```

**What this means:**
- Host directory: `./producer/` (on your computer)
- Container directory: `/app/` (inside container)
- Files from `./producer/` are mounted **directly** into `/app/`

### File Structure Inside Container

```
Container: /app/
├── news_producer.py      # ← Directly in /app/, not /app/producer/
├── price_producer.py
├── price_consumer.py
├── rag_ingest.py
├── tickers.json
└── Dockerfile
```

### Why Not `/app/producer/`?

The volume mount **overrides** what was copied during build:
- **Build time:** `COPY producer/*.py .` copies to `/app/`
- **Runtime:** Volume mount `./producer:/app` mounts to `/app/`
- **Result:** Files are at `/app/news_producer.py`, not `/app/producer/news_producer.py`

## Correct Commands

```bash
# ✅ Correct - Files are directly in /app/
docker-compose run --rm producer python news_producer.py
docker-compose run --rm producer python price_producer.py
docker-compose run --rm producer python price_consumer.py

# ❌ Wrong - No producer/ subdirectory
docker-compose run --rm producer python producer/news_producer.py
```

## Summary

- **Volume mount:** `./producer:/app` → Files go directly to `/app/`
- **Working directory:** `/app` (set in Dockerfile)
- **File location:** `/app/news_producer.py` (not `/app/producer/news_producer.py`)
- **Command:** `python news_producer.py` (not `python producer/news_producer.py`)

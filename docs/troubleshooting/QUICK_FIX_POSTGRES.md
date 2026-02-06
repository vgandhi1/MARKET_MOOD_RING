# ⚡ Quick Fix: PostgreSQL Credentials

## Problem
```
password authentication failed for user "market_user"
```

## Cause
PostgreSQL volume was created with old credentials (`vibe_user`), but code expects `market_user`.

## Quick Fix (2 commands)

```bash
# 1. Stop and remove volume
docker-compose down -v

# 2. Start fresh
docker-compose up -d --build
```

The `-v` flag removes volumes, so PostgreSQL will recreate with new credentials from docker-compose.yaml.

## Or Use the Fix Script

```bash
./fix_postgres.sh
```

This script will:
1. Stop containers
2. Remove old volume
3. Start PostgreSQL fresh
4. Verify connection
5. Start all services

## After Fixing

Verify it works:
```bash
docker exec market_postgres psql -U market_user -d market_mood -c "\dt"
```

Then run producers:
```bash
docker-compose run --rm producer python news_producer.py
```

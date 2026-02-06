# 🔧 Fix PostgreSQL Credentials Issue

## Problem

PostgreSQL authentication error:
```
password authentication failed for user "market_user"
```

## Root Cause

The PostgreSQL container was created with **old credentials** (`vibe_user`/`vibe_password`) and the data persists in the `postgres_data` volume. When we changed to `market_user`/`market_password`, the existing database still has the old user.

## Solution: Recreate PostgreSQL with New Credentials

### Option 1: Remove Volume and Recreate (Recommended - Fresh Start)

```bash
# Stop all containers
docker-compose down

# Remove the postgres_data volume (WARNING: This deletes all data!)
docker volume rm market_mood_ring_postgres_data

# Start fresh with new credentials
docker-compose up -d postgres

# Wait for PostgreSQL to initialize
sleep 5

# Verify new user exists
docker exec market_postgres psql -U market_user -d market_mood -c "\du"

# Start all services
docker-compose up -d
```

### Option 2: Update Existing Database (Keep Data)

If you have important data you want to keep:

```bash
# Connect as postgres superuser
docker exec -it market_postgres psql -U postgres

# Create new user
CREATE USER market_user WITH PASSWORD 'market_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE market_mood TO market_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO market_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO market_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO market_user;

# Exit
\q
```

### Option 3: Quick Fix Script

```bash
#!/bin/bash
# Stop containers
docker-compose down

# Remove volume
docker volume rm market_mood_ring_postgres_data 2>/dev/null || true

# Start fresh
docker-compose up -d --build

echo "✅ PostgreSQL recreated with new credentials"
echo "Database: market_mood"
echo "User: market_user"
echo "Password: market_password"
```

## Verification

After fixing, verify connection:

```bash
# Test connection
docker exec market_postgres psql -U market_user -d market_mood -c "SELECT version();"

# Check tables
docker exec market_postgres psql -U market_user -d market_mood -c "\dt"
```

## Prevention

To avoid this in the future:
- Always use `docker-compose down -v` to remove volumes when changing credentials
- Or use a migration script to update existing databases

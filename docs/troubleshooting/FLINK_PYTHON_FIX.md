# 🔧 Flink Python Fix

## Problem

Flink job submission fails with:
```
Cannot run program "python": error=2, No such file or directory
```

## Root Cause

Flink expects `python` command, but the container only has `python3` installed.

## Solution

Added symlink in `Dockerfile.flink`:
```dockerfile
# Create symlink: python -> python3 (required by Flink)
RUN ln -s /usr/bin/python3 /usr/bin/python
```

## How to Apply Fix

### Option 1: Rebuild Flink Containers

```bash
# Stop Flink services
docker-compose stop jobmanager taskmanager

# Rebuild with fix
docker-compose build jobmanager taskmanager

# Start services
docker-compose up -d jobmanager taskmanager

# Wait for services to be ready
sleep 10

# Verify python symlink exists
docker exec market_taskmanager which python

# Submit Flink job
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

### Option 2: Quick Rebuild All

```bash
docker-compose up -d --build jobmanager taskmanager
```

## Verification

After rebuilding, verify:

```bash
# Check python command exists
docker exec market_taskmanager which python
# Should output: /usr/bin/python

# Check python3 still works
docker exec market_taskmanager which python3
# Should output: /usr/bin/python3

# Check they're linked
docker exec market_taskmanager ls -la /usr/bin/python
# Should show: python -> python3
```

## Submit Flink Job

Once containers are rebuilt:

```bash
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py
```

Expected output:
```
Job has been submitted with JobID: <job-id>
```

Check job status:
```bash
docker exec market_jobmanager ./bin/flink list
```

Or visit Flink dashboard: http://localhost:8081

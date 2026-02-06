# 🔧 Port 8501 Conflict - Resolution Guide

## Problem
Port 8501 is already allocated by another container: `crypto-etl-streamlit-dashboard`

## Solution Options

### Option 1: Stop the Conflicting Container (Recommended)

```bash
# Stop the other container
docker stop crypto-etl-streamlit-dashboard

# Remove it (optional, if you don't need it)
docker rm crypto-etl-streamlit-dashboard

# Then restart Market Mood Ring
docker-compose up -d
```

### Option 2: Change Market Mood Ring Port

If you need both dashboards running, change Market Mood Ring to use a different port.

Edit `docker-compose.yaml` and change:
```yaml
ports:
  - "8501:8501"  # Change to different port
```

To:
```yaml
ports:
  - "8502:8501"  # Use port 8502 instead
```

Then access dashboard at: http://localhost:8502

## Already Fixed

✅ Removed obsolete `version` attribute from docker-compose.yaml  
✅ Cleaned up stale `vibe_dashboard` container

## Next Steps

1. Choose Option 1 or Option 2 above
2. Run: `docker-compose up -d`
3. Access dashboard at the appropriate port

# 🔍 Docker Compose Profiles Explained

## What is `profiles`?

**`profiles`** is a Docker Compose feature that allows you to mark services that should **NOT start automatically** with `docker-compose up`.

## How It Works

### In docker-compose.yaml:

```yaml
producer:
  profiles:
    - producers  # ← This is just a label/name
```

### What Happens:

1. **`docker-compose up -d`** (without profile):
   - ❌ Producer service is **SKIPPED** (doesn't start)
   - ✅ Other services start normally
   - ✅ Producer image is still **BUILT** (ready to use)

2. **`docker-compose run producer`**:
   - ✅ Works **regardless of profiles**
   - ✅ Creates and starts container
   - ✅ Profiles don't affect `run` command

3. **`docker-compose --profile producers up -d`**:
   - ✅ Producer service **WILL start** automatically
   - ✅ All services start together

## Why "producers" (plural) when service is "producer" (singular)?

**Answer:** The profile name is just a **label** - it can be anything!

- Profile name: `producers` (plural) - just a label
- Service name: `producer` (singular) - actual service name
- They don't have to match!

### Common Profile Names:
- `producers` - Makes sense (multiple producer scripts)
- `workers` - Generic worker services
- `dev` - Development-only services
- `test` - Testing services

## The Key Difference

| Command | Profiles Affect? | Producer Starts? |
|---------|-----------------|------------------|
| `docker-compose up -d` | ✅ Yes | ❌ No (skipped) |
| `docker-compose --profile producers up -d` | ✅ Yes | ✅ Yes (starts) |
| `docker-compose run producer python script.py` | ❌ No | ✅ Yes (always works) |

## Why Use Profiles?

**Purpose:** Keep producer services **out of the default startup**

**Benefits:**
- ✅ Infrastructure starts quickly (`docker-compose up -d`)
- ✅ Producers only start when you explicitly need them
- ✅ Can run multiple producer scripts independently
- ✅ Avoids conflicts (don't want all producers starting at once)

## Current Setup

```yaml
producer:
  profiles:
    - producers  # ← Label: "producers" (can be anything)
```

**What this means:**
- Service name: `producer` (used in `docker-compose run producer`)
- Profile label: `producers` (used in `docker-compose --profile producers up`)
- They're independent!

## Should We Change It?

### Option 1: Keep as-is ✅ (Recommended)
- Profile name `producers` makes sense (multiple producer scripts)
- Service name `producer` is singular (one service definition)
- Clear separation between label and service name

### Option 2: Match them
```yaml
producer:
  profiles:
    - producer  # Match service name
```
- More consistent naming
- But less descriptive (doesn't indicate multiple scripts)

### Option 3: Remove profiles
```yaml
producer:
  # No profiles - starts automatically
```
- Simpler
- But all producers would start together (not what we want)

## Recommendation

**Keep it as-is!** The current setup is correct:
- Profile `producers` (plural) indicates multiple producer scripts
- Service `producer` (singular) is the service definition
- `docker-compose run producer` works perfectly
- Profiles prevent auto-start (which is what we want)

## Summary

1. **`profiles: - producers`** = Label to prevent auto-start
2. **`docker-compose run producer`** = Works regardless of profiles
3. **Profile name vs Service name** = They're independent, don't need to match
4. **Current setup** = Correct and working as intended

---

**TL;DR:** Profile name is just a label. `docker-compose run producer` works fine because `run` ignores profiles. The profile only affects `docker-compose up`.

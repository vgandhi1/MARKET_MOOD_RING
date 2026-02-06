# 🐳 Docker Compose Behavior Explained

## Question 1: What does `docker-compose up -d` do with the producer service?

### Answer: **It BUILDS the image but DOESN'T start the container**

### Detailed Breakdown:

#### Step 1: `docker-compose up -d` Execution

When you run `docker-compose up -d`:

1. **Reads docker-compose.yaml**
   - Finds all services defined
   - Checks for `profiles` attribute

2. **Producer Service Analysis:**
   ```yaml
   producer:
     profiles:
       - producers  # ← This is just a label (can be anything)
   ```

3. **What Happens:**
   - ✅ **BUILDS the image** using `producer/Dockerfile`
   - ✅ Creates the image: `market_mood_ring-producer`
   - ❌ **DOES NOT start a container** (because of `profiles`)
   - ❌ Producer container is **skipped** unless profile is activated

4. **Other Services:**
   - ✅ Zookeeper, Kafka, Postgres, Flink, Dashboard **all start**
   - ✅ Their containers are created and started

### Important Note About Profiles:

- **Profile name** (`producers`) is just a **label** - it can be anything
- **Service name** (`producer`) is what you use in `docker-compose run producer`
- **They don't need to match!**
- `docker-compose run producer` works **regardless of profiles** - profiles only affect `docker-compose up`

### Why `profiles`?

The `profiles` feature allows you to:
- **Define services** that aren't started by default
- **Build images** for services you might use later
- **Start them explicitly** when needed

### Producer Service Status After `docker-compose up -d`:

```bash
# Check if producer container exists
docker ps -a | grep producer
# Result: No container (because profiles prevented it from starting)

# But the IMAGE exists
docker images | grep producer
# Result: market_mood_ring-producer (image is built)
```

---

## Question 2: Why does `docker-compose run producer` create more containers?

### Answer: **Each `run` command creates a NEW one-off container**

### Detailed Breakdown:

#### What `docker-compose run` Does:

1. **Creates a NEW container** (doesn't reuse existing ones)
2. **Runs your command** inside that container
3. **Container persists** after command finishes (unless you use `--rm`)

#### Example Sequence:

```bash
# First run
docker-compose run producer python news_producer.py
# Creates: market_mood_ring-producer-run-abc123

# Second run (different terminal)
docker-compose run producer python price_producer.py
# Creates: market_mood_ring-producer-run-def456

# Third run (another terminal)
docker-compose run producer python price_consumer.py
# Creates: market_mood_ring-producer-run-ghi789
```

**Result:** 3 separate containers, all running simultaneously!

### Why Separate Containers?

- ✅ **Isolation:** Each script runs independently
- ✅ **Logs:** Can see logs per script: `docker logs container-name`
- ✅ **Flexibility:** Can stop/start each independently
- ✅ **Debugging:** Easier to debug individual processes

### Container Lifecycle:

```
docker-compose run producer python news_producer.py
  ↓
Creates container: market_mood_ring-producer-run-{random-id}
  ↓
Runs: python news_producer.py (infinite loop)
  ↓
Container keeps running (even after you Ctrl+C in terminal)
  ↓
Container becomes "orphan" (not managed by docker-compose)
```

### The Problem: Orphan Containers

After running multiple `docker-compose run` commands:
- Multiple containers exist
- They're not tracked by docker-compose
- They become "orphans"
- Need cleanup: `docker-compose down --remove-orphans`

---

## Summary Table

| Command | Producer Image | Producer Container | Other Services |
|---------|---------------|-------------------|----------------|
| `docker-compose up -d` | ✅ Built | ❌ Not started (profiles) | ✅ Started |
| `docker-compose run producer python script.py` | ✅ Uses existing | ✅ Creates NEW container | ✅ Still running |
| `docker-compose run producer python script2.py` | ✅ Uses existing | ✅ Creates ANOTHER container | ✅ Still running |

---

## Key Takeaways

1. **`docker-compose up -d`:**
   - Builds producer image ✅
   - Doesn't start producer container (profiles) ❌
   - Starts all other services ✅

2. **`docker-compose run producer`:**
   - Creates a NEW container each time
   - Uses the built image
   - Container persists after command
   - Creates orphans if not cleaned up

3. **Best Practice:**
   - Use `docker-compose up -d` to start infrastructure
   - Use `docker-compose run --rm producer` to avoid orphans
   - Or use `docker-compose down --remove-orphans` to clean up

---

## Alternative: Use `--rm` Flag

To avoid orphan containers:

```bash
docker-compose run --rm producer python news_producer.py
```

The `--rm` flag automatically removes the container when it stops.

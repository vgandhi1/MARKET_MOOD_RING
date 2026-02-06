# 🔧 Producer Architecture Explanation

## Question 1: Why do we need `producer/Dockerfile`?

### Answer: Docker Compose needs it to BUILD the image

The `producer/Dockerfile` is **required** because:

1. **docker-compose.yaml references it:**
   ```yaml
   producer:
     build:
       context: ./producer
       dockerfile: Dockerfile  # ← References this file
   ```

2. **Docker Compose uses it to build the image:**
   - When you run `docker-compose run producer python news_producer.py`
   - Docker Compose first builds the image using the Dockerfile
   - Then creates a container from that image
   - Then runs your command inside that container

3. **What the Dockerfile does:**
   - Sets up Python 3.9 environment
   - Installs system dependencies (gcc, postgresql-client)
   - Installs Python packages from `requirements.txt`
   - Copies all Python files into the container
   - Sets default command (can be overridden)

### Without the Dockerfile:
- Docker Compose wouldn't know how to build the producer image
- You'd get an error: "dockerfile not found"

### The Dockerfile is the "recipe" for building the producer container

---

## Question 2: Do we need to run the 3 Python files simultaneously?

### Answer: **Yes, but they run independently**

### The 3 Scripts and Their Roles:

1. **`news_producer.py`**
   - **Purpose:** Fetches news from Finnhub API
   - **Output:** Publishes to Kafka `stock_news` topic
   - **Runs:** Continuously (infinite loop)

2. **`price_producer.py`**
   - **Purpose:** Fetches stock prices from Finnhub API
   - **Output:** Publishes to Kafka `stock_prices` topic
   - **Runs:** Continuously (infinite loop)

3. **`price_consumer.py`**
   - **Purpose:** Consumes prices from Kafka
   - **Output:** Writes to PostgreSQL `price_log` table
   - **Runs:** Continuously (infinite loop)

### Data Flow:

```
news_producer.py → Kafka (stock_news) → Flink Job → sentiment_log
price_producer.py → Kafka (stock_prices) → price_consumer.py → price_log
```

### Why Run Simultaneously?

✅ **Independent Processes:** Each script does a different job
- News producer doesn't depend on price producer
- Price consumer needs price producer to have data in Kafka
- They can run in parallel

✅ **Real-time Pipeline:** 
- News and prices are fetched continuously
- Consumer processes prices as they arrive
- All need to run for the system to work

### Current Setup (One-off Containers):

```bash
# Terminal 1
docker-compose run producer python news_producer.py

# Terminal 2  
docker-compose run producer python price_producer.py

# Terminal 3
docker-compose run producer python price_consumer.py
```

**Each creates a separate container** - this is fine! They're independent processes.

---

## Alternative Approaches

### Option 1: Current Approach (One-off Containers) ✅
**Pros:**
- Simple, easy to understand
- Can start/stop each independently
- Easy to debug (see logs per process)

**Cons:**
- Need 3 terminals
- Creates orphan containers (need cleanup)

### Option 2: Separate Services in docker-compose.yaml

You could define them as separate services:

```yaml
services:
  news_producer:
    build:
      context: ./producer
    command: python news_producer.py
    # ... environment, volumes, etc.
  
  price_producer:
    build:
      context: ./producer
    command: python price_producer.py
    # ... environment, volumes, etc.
  
  price_consumer:
    build:
      context: ./producer
    command: python price_consumer.py
    # ... environment, volumes, etc.
```

**Pros:**
- All start with `docker-compose up -d`
- No orphan containers
- Easier to manage

**Cons:**
- More complex docker-compose.yaml
- All start together (less flexible)

### Option 3: Process Manager (Supervisor/PM2)

Run all 3 in one container with a process manager:

```dockerfile
# Install supervisor
RUN apt-get install -y supervisor

# Configure supervisor to run all 3 scripts
COPY supervisord.conf /etc/supervisor/conf.d/
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

**Pros:**
- Single container
- Process management (auto-restart)

**Cons:**
- More complex setup
- Harder to debug individual processes

---

## Recommendation

**Current approach (one-off containers) is fine for Phase 1** because:

1. ✅ Simple and clear
2. ✅ Easy to debug (see logs per script)
3. ✅ Flexible (can start/stop individually)
4. ✅ Works well for development

**For production, consider Option 2** (separate services) for better orchestration.

---

## Summary

1. **Dockerfile is needed:** Docker Compose uses it to build the image
2. **Run simultaneously:** Yes, all 3 scripts need to run for the pipeline to work
3. **Current setup:** One-off containers work fine, just need cleanup with `--remove-orphans`

# Docker and Compose architecture

How Market Mood Ring runs in Docker: services, networking, profiles, and custom images.

**Related:** [DOCKER_VS_SCRIPT_GUIDE.md](../DOCKER_VS_SCRIPT_GUIDE.md) · [PROFILES_EXPLAINED.md](PROFILES_EXPLAINED.md) · `docker-compose.yaml`

---

## Stack overview

| Service | Container | Port | Image / build |
|---------|-----------|------|----------------|
| Kafka (KRaft) | `market_kafka` | 9092 | `confluentinc/cp-kafka:7.6.0` |
| PostgreSQL + pgvector | `market_postgres` | 5432 | `pgvector/pgvector:pg14` |
| Flink JobManager | `market_jobmanager` | 8081 | `Dockerfile.flink` |
| Flink TaskManager | `market_taskmanager` | — | `Dockerfile.flink` |
| Streamlit dashboard | `market_dashboard` | 8502→8501 | `dashboard/Dockerfile` |
| Producers | `market_*_producer` | — | `producer/Dockerfile` (profile `producers`) |

**Not in Docker:** Ollama runs on the **Windows host** at `http://host.docker.internal:11434` for GPU access.

**No Zookeeper:** Kafka uses KRaft mode (`KAFKA_PROCESS_ROLES: broker,controller`).

---

## Network and volumes

- **Network:** `market_network` (bridge) — all services resolve by service name (`kafka`, `postgres`, `jobmanager`).
- **Kafka internal bootstrap:** `kafka:29092` (producers/Flink inside Docker).
- **Kafka host access:** `localhost:9092`.
- **Volume:** `postgres_data` persists DB; `init.sql` runs on first boot.

---

## Custom images

### Flink (`Dockerfile.flink`)

- Base: `flink:1.17-scala_2.12-java11`
- Python 3 + PyFlink + NLTK (`vader_lexicon`, `punkt`)
- `python` → `python3` symlink for PyFlink
- Connector JARs in `/opt/flink/lib/`: Kafka, JDBC, PostgreSQL driver
- Job file: `/opt/flink/usrlib/flink_sentiment.py` (also volume-mounted from `./flink_jobs`)

### Dashboard (`dashboard/Dockerfile`)

- Streamlit app; env: `POSTGRES_*`, `OLLAMA_BASE_URL`
- Volume: `./dashboard:/app` for live code edits

### Producers (`producer/Dockerfile`)

- Shared base `producer`; YAML anchor `&producer_base`
- Volume: `./producer:/app` — scripts live at `/app/news_producer.py` (not `/app/producer/...`)

---

## Compose profiles

| Profile | Effect |
|---------|--------|
| *(default)* | Kafka, Postgres, Flink, dashboard start on `docker-compose up` |
| `producers` | Starts `news-producer`, `price-producer`, `price-consumer`, `rag-ingest` |
| `manual` | Base `producer` toolbox only (inheritance); not started by default |

**`docker-compose up -d`** builds the producer image but does **not** start producer containers unless `--profile producers` is used.

**Recommended:** `./start_data_pipeline.sh` — starts infrastructure, producers, health checks, and Flink job submission.

---

## Environment wiring

From `.env` / `docker-compose.yaml` into containers:

| Variable | Used by |
|----------|---------|
| `FINNHUB_API_KEY` | Producers |
| `STOCK_SYMBOLS` | Producers (optional override) |
| `POSTGRES_*` | Dashboard, producers, Flink JDBC |
| `KAFKA_BOOTSTRAP_SERVERS` | Producers (`kafka:29092`) |
| `WINDOWS_HOST_IP` | Dashboard `extra_hosts` for Ollama |

---

## Common commands

```bash
# Full stack (manual)
docker-compose --profile producers up -d --build

# Infrastructure only
docker-compose up -d kafka postgres jobmanager taskmanager dashboard

# Flink job
docker exec -it market_jobmanager ./bin/flink run -py /opt/flink/usrlib/flink_sentiment.py

# Producer one-off (working dir is /app)
docker-compose run --rm news-producer
```

---

## Producer path gotcha

Volume mount `./producer:/app` means:

```bash
# Correct
docker-compose run --rm producer python news_producer.py

# Wrong — no producer/ subfolder inside container
docker-compose run --rm producer python producer/news_producer.py
```

---

## Rebuild after Dockerfile changes

```bash
docker-compose build jobmanager taskmanager
docker-compose up -d jobmanager taskmanager
```

See **[FLINK_FIXES.md](../troubleshooting/FLINK_FIXES.md)** if connector or Python errors persist.

# Deployment Summary

## Infrastructure (current)

| Service | Container | Port | Notes |
|---------|-----------|------|-------|
| Kafka (KRaft) | `market_kafka` | 9092 | Topics: `stock_news`, `stock_prices` |
| PostgreSQL + pgvector | `market_postgres` | 5432 | DB: `market_mood`, user: `market_user` |
| Flink JobManager | `market_jobmanager` | 8081 | Submits `flink_sentiment.py` |
| Flink TaskManager | `market_taskmanager` | — | Stream processing workers |
| Streamlit dashboard | `market_dashboard` | 8502 | Charts + AI Analyst |
| Producers (profile) | `market_news_producer`, etc. | — | Started via `start_data_pipeline.sh` |

**Ollama** runs on the **Windows host** (not in Docker) at `http://host.docker.internal:11434`.

## Recommended deployment

```bash
cp .env.example .env   # add FINNHUB_API_KEY
chmod +x start_data_pipeline.sh
./start_data_pipeline.sh
```

The script starts infrastructure, producers, submits the Flink job, and verifies connectivity.

## Manual verification

```bash
# Kafka topics
docker exec -it market_kafka kafka-topics --list --bootstrap-server localhost:9092

# Database tables
docker exec -it market_postgres psql -U market_user -d market_mood -c "\dt"

# Flink jobs
docker exec market_jobmanager ./bin/flink list
```

Expected tables: `price_log`, `sentiment_log`, `financial_knowledge`.

## Access URLs

- **Dashboard:** http://localhost:8502
- **Flink UI:** http://localhost:8081
- **PostgreSQL:** `localhost:5432` (`market_user` / `market_password` / `market_mood`)

## Architecture flow

```
Finnhub API → Producers → Kafka (stock_news, stock_prices)
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
            Flink (sentiment)    RAG ingest (embeddings)
                    ↓                   ↓
            sentiment_log        financial_knowledge
                    ↓                   ↓
            Streamlit Dashboard ←→ Ollama (host LLM)
```

## Features deployed

1. Real-time news and price ingestion (Finnhub, 60s polling)
2. Kafka streaming (KRaft, no Zookeeper)
3. Flink NLTK VADER sentiment on `stock_news`
4. pgvector RAG storage and Streamlit AI Analyst
5. 72-hour price charts and live sentiment table

**Status:** Production-ready for portfolio/demo use.

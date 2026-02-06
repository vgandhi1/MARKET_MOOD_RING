# 🏗️ System Architecture Overview

## High-Level Architecture

```mermaid
graph TB
    subgraph "External APIs"
        FINNHUB[Finnhub API<br/>News & Prices]
    end
    
    subgraph "Ingestion Layer"
        NP[news_producer.py<br/>Fetches News]
        PP[price_producer.py<br/>Fetches Prices]
        NP --> FINNHUB
        PP --> FINNHUB
    end
    
    subgraph "Message Queue"
        KAFKA[Apache Kafka<br/>Topics: stock_news, stock_prices]
        NP -->|JSON| KAFKA
        PP -->|JSON| KAFKA
    end
    
    subgraph "Processing Layer"
        FLINK[Apache Flink<br/>Sentiment Analysis<br/>NLTK Vader]
        PC[price_consumer.py<br/>Price Persistence]
        KAFKA -->|Consume| FLINK
        KAFKA -->|Consume| PC
    end
    
    subgraph "Storage Layer"
        PG[(PostgreSQL<br/>market_mood<br/>pgvector)]
        FLINK -->|Sentiment Scores| PG
        PC -->|Price Data| PG
    end
    
    subgraph "Presentation Layer"
        DASH[Streamlit Dashboard<br/>Port 8502]
        PG -->|Query| DASH
    end
    
    USER[👤 User] -->|View & Interact| DASH
    
    style FINNHUB fill:#e1f5ff
    style KAFKA fill:#ffeb3b
    style FLINK fill:#4caf50
    style PG fill:#2196f3
    style DASH fill:#ff9800
```

---

## Data Flow Diagram

### Phase 1: ETL Pipeline

```mermaid
sequenceDiagram
    participant API as Finnhub API
    participant NP as news_producer.py
    participant PP as price_producer.py
    participant K as Kafka
    participant PC as price_consumer.py
    participant F as Flink Job
    participant DB as PostgreSQL
    participant D as Dashboard
    
    loop Every Cycle
        NP->>API: Fetch News
        API-->>NP: News Headlines
        NP->>K: Publish to stock_news
    end
    
    loop Every Cycle
        PP->>API: Fetch Prices
        API-->>PP: Stock Prices
        PP->>K: Publish to stock_prices
    end
    
    loop Continuous
        K->>PC: Consume stock_prices
        PC->>DB: INSERT price_log
    end
    
    loop Continuous
        K->>F: Consume stock_news
        F->>F: Analyze Sentiment (NLTK)
        F->>DB: INSERT sentiment_log
    end
    
    loop User Request
        D->>DB: SELECT price_log
        D->>DB: SELECT sentiment_log
        DB-->>D: Return Data
        D-->>USER: Display Charts
    end
```

---

## Component Interaction

### Service Communication

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                  (market_network)                        │
│                                                          │
│  ┌────────────┐                                         │
│  │ Zookeeper  │◄────────────────┐                      │
│  │   :2181    │                  │                      │
│  └────────────┘                  │                      │
│         ▲                         │                      │
│         │                         │                      │
│  ┌──────┴──────┐          ┌──────▼──────┐             │
│  │    Kafka    │          │   Kafka      │             │
│  │   :29092    │          │   :9092      │             │
│  │  (internal) │          │  (external)  │             │
│  └──────┬──────┘          └─────────────┘             │
│         │                                                │
│    ┌────┴────┐                                          │
│    │         │                                           │
│  ┌─▼──┐   ┌─▼──┐                                        │
│  │NP  │   │PP  │                                        │
│  └─┬──┘   └─┬──┘                                        │
│    │        │                                            │
│    └───┬────┘                                            │
│        │                                                  │
│    ┌───▼────┐                                            │
│    │ Kafka  │                                            │
│    └───┬────┘                                            │
│        │                                                  │
│    ┌───┴────┐                                            │
│    │        │                                            │
│  ┌─▼──┐  ┌─▼────┐                                       │
│  │PC  │  │Flink │                                       │
│  └─┬──┘  └─┬────┘                                       │
│    │       │                                             │
│    └───┬───┘                                             │
│        │                                                 │
│    ┌───▼──────┐                                          │
│    │PostgreSQL│                                          │
│    │  :5432   │                                          │
│    └───┬──────┘                                          │
│        │                                                 │
│    ┌───▼──────┐                                          │
│    │Dashboard │                                          │
│    │  :8502   │                                          │
│    └──────────┘                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Infrastructure Layer
- **Container Orchestration:** Docker Compose
- **Message Broker:** Apache Kafka 7.5.0
- **Coordination:** Zookeeper 7.5.0
- **Database:** PostgreSQL 14 with pgvector

### Processing Layer
- **Stream Processing:** Apache Flink 1.17
- **Language:** Python 3.9 (PyFlink)
- **NLP Library:** NLTK Vader Sentiment

### Application Layer
- **UI Framework:** Streamlit
- **Visualization:** Plotly
- **Data Processing:** Pandas

### Data Sources
- **Financial Data:** Finnhub API
- **Stock Coverage:** 30+ US stocks (NYSE, NASDAQ)

---

## Phase Architecture Comparison

### Phase 1: ETL Pipeline (Current)

```
Finnhub → Producers → Kafka → Flink → PostgreSQL → Dashboard
```

**Components:**
- ✅ Data ingestion
- ✅ Stream processing
- ✅ Sentiment analysis
- ✅ Data visualization
- ❌ No LLM/AI
- ❌ No vector embeddings

---

### Phase 2: LLM Integration

```
Finnhub → Producers → Kafka → Flink → PostgreSQL → Dashboard
                              ↓
                         RAG Pipeline → Vector Store → LLM API
```

**Additional Components:**
- ✅ Vector embeddings (sentence-transformers)
- ✅ RAG pipeline
- ✅ LLM integration (cloud API)
- ✅ AI chat interface

---

### Phase 3: Ollama Integration

```
Finnhub → Producers → Kafka → Flink → PostgreSQL → Dashboard
                              ↓
                         RAG Pipeline → Vector Store → Ollama (Local)
```

**Additional Components:**
- ✅ Ollama server (local)
- ✅ Llama 3 model
- ✅ Private, fast AI responses

---

## Scalability Considerations

### Horizontal Scaling

**Kafka:**
- Multiple partitions per topic
- Consumer groups for parallel processing

**Flink:**
- Multiple task managers
- Parallel processing slots

**PostgreSQL:**
- Read replicas
- Connection pooling

### Vertical Scaling

- Increase container resources
- Optimize Flink parallelism
- Database indexing

---

## Security Considerations

### Network Isolation
- Docker bridge network
- Internal service communication only
- External ports only where needed

### Credentials
- Environment variables (.env file)
- Not committed to repository
- Per-service credentials

### Data Privacy
- Phase 1: No external LLM calls
- Phase 3: Local LLM (complete privacy)

---

## Monitoring & Observability

### Flink Dashboard
- Job status and metrics
- Throughput and latency
- Error tracking

### Database Queries
- Query performance
- Table sizes
- Connection counts

### Container Logs
- `docker-compose logs`
- Per-service logging
- Error tracking

---

## Deployment Architecture

### Development
- Local Docker Compose
- Volume mounts for live reloading
- Debug-friendly configuration

### Production (Future)
- Kubernetes deployment
- Service mesh (Istio)
- Monitoring (Prometheus, Grafana)
- Logging (ELK stack)

---

## Summary

The Market Mood Ring architecture follows a modern microservices pattern:

1. **Ingestion:** Python producers fetch data from APIs
2. **Streaming:** Kafka buffers and distributes messages
3. **Processing:** Flink performs real-time transformations
4. **Storage:** PostgreSQL persists processed data
5. **Presentation:** Streamlit provides user interface

Each phase adds capabilities incrementally:
- **Phase 1:** Core ETL pipeline
- **Phase 2:** LLM integration
- **Phase 3:** Local LLM deployment

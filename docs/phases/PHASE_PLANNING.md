# 🚀 Market Mood Ring - Phase Planning

## Overview

The Market Mood Ring project is being developed in phases to ensure each component is tested and validated before moving to the next.

---

## 📋 Phase 1: ETL Pipeline with Sentiment Analysis (CURRENT FOCUS)

### Objective
Build and validate the core ETL pipeline with real-time sentiment analysis using NLTK.

### Components

#### ✅ Infrastructure
- **Kafka** - Message streaming (stock_news, stock_prices topics)
- **Zookeeper** - Kafka coordination
- **PostgreSQL** - Data storage (crypto_vibes database)
- **Flink** - Stream processing (JobManager + TaskManager)

#### ✅ Data Ingestion
- **News Producer** - Fetches news from Finnhub API → Kafka `stock_news` topic
- **Price Producer** - Fetches prices from Finnhub API → Kafka `stock_prices` topic
- **Price Consumer** - Consumes prices from Kafka → PostgreSQL `price_log` table

#### ✅ Stream Processing
- **Flink Sentiment Job** - Consumes `stock_news` → Applies NLTK Vader → Writes to `sentiment_log` table

#### ✅ Storage
- **PostgreSQL Tables:**
  - `price_log` - Time series price data
  - `sentiment_log` - News headlines with sentiment scores

#### ✅ Dashboard (Basic)
- **Streamlit Dashboard** - View price charts and sentiment scores
- **No AI Chat** - Will be added in Phase 2

### Phase 1 Deliverables
- [x] Kafka topics created and receiving data
- [x] News and price data flowing through pipeline
- [x] Flink job processing sentiment scores
- [x] Data stored in PostgreSQL
- [x] Dashboard displaying live data
- [ ] End-to-end testing and validation

### Phase 1 Testing Checklist
- [ ] News producer successfully fetching and publishing to Kafka
- [ ] Price producer successfully fetching and publishing to Kafka
- [ ] Price consumer writing to PostgreSQL
- [ ] Flink job calculating sentiment scores correctly
- [ ] Sentiment scores appearing in `sentiment_log` table
- [ ] Dashboard displaying price charts
- [ ] Dashboard displaying sentiment scores
- [ ] Data pipeline running stable for extended period

---

## 🔮 Phase 2: LLM Integration (FUTURE)

### Objective
Add AI-powered analysis using RAG (Retrieval Augmented Generation) with LLM capabilities.

### LLM Options

**Option A: Cloud LLM APIs**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google Gemini
- Hugging Face Inference API
- Azure OpenAI

**Option B: Local LLM (Ollama)**
- Ollama server with Llama 3
- Complete privacy
- No API costs

### Additional Components

#### 🔮 Infrastructure
- **LLM Provider** - Cloud API (OpenAI, Anthropic, etc.) OR Ollama (local)
- **Ollama** - Local LLM service (commented out, enable if using Option B)

#### 🔮 Data Processing
- **RAG Ingestion** - Consumes `stock_news` → Creates embeddings → Stores in `financial_knowledge` table

#### 🔮 AI Features
- **AI Analyst Chat** - Vector search + Ollama generation
- **Semantic Search** - Query news using embeddings
- **Context-Aware Responses** - LLM answers based on retrieved news

### Phase 2 Deliverables
- [ ] LLM provider configured (Cloud API or Ollama)
- [ ] RAG ingestion creating embeddings
- [ ] `financial_knowledge` table populated with vectors
- [ ] AI chat interface functional
- [ ] Vector search working correctly
- [ ] LLM generating context-aware responses
- [ ] Environment variables configured for chosen LLM provider

### Phase 2 Prerequisites
- ✅ Phase 1 fully tested and stable
- ✅ Sufficient news data collected
- ✅ Database performance validated
- ✅ LLM provider chosen (Cloud API or Ollama)
- ✅ API keys obtained (if using Cloud API)
- ✅ Requirements installed (see `docs/setup/REQUIREMENTS_BY_PHASE.md`)

---

## 🏗️ Architecture by Phase

### Phase 1 Architecture
```
Finnhub API → Producers → Kafka Topics
                    ↓
            Flink (Sentiment)
                    ↓
            PostgreSQL (price_log, sentiment_log)
                    ↓
            Streamlit Dashboard (Charts + Tables)
```

### Phase 2 Architecture (Future)
```
Phase 1 Pipeline
        +
RAG Ingestion → financial_knowledge (vectors)
        +
LLM Provider ← Vector Search ← Streamlit Chat
  (Cloud API or Ollama)
```

**LLM Provider Options:**
- **Cloud:** OpenAI, Anthropic, Google Gemini, etc.
- **Local:** Ollama with Llama 3

---

## 📝 Implementation Notes

### Docker Compose
- **Phase 1:** Ollama services commented out with `#`
- **Phase 2:** 
  - **Cloud LLM:** No Docker changes needed
  - **Ollama:** Uncomment Ollama services when ready

### Code Organization
- **Phase 1:** Focus on ETL and sentiment analysis
- **Phase 2:** RAG and AI features ready but not active
- **LLM Integration:** See `docs/setup/LLM_API_INTEGRATION.md` for provider setup

### Testing Strategy
- **Phase 1:** Test each component independently, then end-to-end
- **Phase 2:** Test RAG pipeline separately, then integrate with Phase 1

---

## 🎯 Current Status

**Active Phase:** Combined Development (Phase 1 + Ollama)
**Focus:** Full Pipeline Testing (ETL + AI Analyst)
**Next Steps:**
1. Verify Kafka/Flink pipeline health.
2. Verify Ollama connection and Llama 3 model download.
3. Test AI Analyst chat responses.

---

**Last Updated:** Phase planning established

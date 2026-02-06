# 📦 Requirements by Phase

## Overview

This document explains Python package requirements for each phase of the Market Mood Ring project.

---

## 📋 Phase 1: ETL Pipeline (Current)

**Status:** ✅ Active  
**Focus:** Data ingestion, stream processing, and visualization

### Requirements File

**File:** `requirements.txt` (root directory)

```txt
# Market Mood Ring - Phase 1 Requirements
# ETL Pipeline with Sentiment Analysis

# Core dependencies
requests>=2.31.0
pandas>=2.0.0

# Database
psycopg2-binary>=2.9.9

# Kafka
kafka-python>=2.0.2

# Dashboard
streamlit>=1.28.0
plotly>=5.17.0

# Note: sentence-transformers and torch are NOT included (Phase 2 only)
```

### Package Breakdown

| Package | Purpose | Used By |
|---------|---------|---------|
| `requests` | HTTP client for Finnhub API | `news_producer.py`, `price_producer.py` |
| `pandas` | Data manipulation | `dashboard/app.py` |
| `psycopg2-binary` | PostgreSQL driver | `price_consumer.py`, `dashboard/app.py` |
| `kafka-python` | Kafka client | All producers, `price_consumer.py` |
| `streamlit` | Web UI framework | `dashboard/app.py` |
| `plotly` | Interactive charts | `dashboard/app.py` |

### Installation

```bash
# Using UV (recommended)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### Docker Installation

Packages are installed during Docker build:
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

---

## 🔮 Phase 2: LLM Integration (Future)

**Status:** 🔜 Planned  
**Focus:** Add LLM capabilities (Cloud API or Local Model)

### Option A: Cloud LLM APIs

**File:** `requirements-phase2-llm-api.txt` (new file)

```txt
# Market Mood Ring - Phase 2: LLM API Integration
# Install Phase 1 requirements first: pip install -r requirements.txt
# Then install Phase 2: pip install -r requirements-phase2-llm-api.txt

# Vector embeddings (required for RAG)
sentence-transformers>=2.2.2

# LLM API Clients (choose one or more)
# Option 1: OpenAI
openai>=1.0.0

# Option 2: Anthropic Claude
anthropic>=0.18.0

# Option 3: Google Gemini
google-generativeai>=0.3.0

# Option 4: Hugging Face Inference API
huggingface-hub>=0.20.0
transformers>=4.41.0

# Option 5: Azure OpenAI
openai>=1.0.0  # Same as OpenAI, configure with Azure endpoint
```

### Option B: Local LLM (Ollama)

**File:** `requirements-phase2-ollama.txt` (new file)

```txt
# Market Mood Ring - Phase 2: Ollama Integration
# Install Phase 1 requirements first: pip install -r requirements.txt
# Then install Phase 2: pip install -r requirements-phase2-ollama.txt

# Vector embeddings (required for RAG)
sentence-transformers>=2.2.2

# Ollama Python client
ollama>=0.1.0

# Note: Ollama server runs in Docker container
# This package is only for Python client to communicate with Ollama
```

### Combined Phase 2 Requirements

**File:** `requirements-phase2.txt` (current file)

```txt
# Market Mood Ring - Phase 2 Requirements
# Additional dependencies for RAG Pipeline

# Vector embeddings (requires torch - large download ~888MB)
sentence-transformers>=2.2.2

# Note: Install Phase 1 requirements first, then add Phase 2:
# pip install -r requirements-phase1.txt
# pip install -r requirements-phase2.txt
```

### Package Breakdown

| Package | Purpose | Phase 2 Option |
|---------|---------|----------------|
| `sentence-transformers` | Vector embeddings for RAG | Both (Required) |
| `openai` | OpenAI API client | Cloud API |
| `anthropic` | Anthropic Claude API | Cloud API |
| `google-generativeai` | Google Gemini API | Cloud API |
| `huggingface-hub` | Hugging Face Inference | Cloud API |
| `ollama` | Ollama Python client | Local LLM |

### Installation Examples

#### Cloud LLM (OpenAI)

```bash
# Install Phase 1
pip install -r requirements.txt

# Install Phase 2 with OpenAI
pip install sentence-transformers>=2.2.2
pip install openai>=1.0.0
```

#### Cloud LLM (Anthropic)

```bash
# Install Phase 1
pip install -r requirements.txt

# Install Phase 2 with Anthropic
pip install sentence-transformers>=2.2.2
pip install anthropic>=0.18.0
```

#### Local LLM (Ollama)

```bash
# Install Phase 1
pip install -r requirements.txt

# Install Phase 2 with Ollama
pip install sentence-transformers>=2.2.2
pip install ollama>=0.1.0
```

---

## 🦙 Phase 3: Ollama Integration (Future)

**Status:** 🔜 Planned  
**Focus:** Local LLM deployment with Ollama

### Requirements

**File:** `requirements-phase3.txt` (new file)

```txt
# Market Mood Ring - Phase 3: Ollama Integration
# Install Phase 1 and Phase 2 requirements first

# Ollama Python client (if not already installed)
ollama>=0.1.0

# Note: Phase 3 uses same requirements as Phase 2 (Ollama option)
# Main difference is Ollama server runs in Docker container
```

### Package Breakdown

| Package | Purpose | Notes |
|---------|---------|-------|
| `ollama` | Ollama Python client | Communicates with Ollama Docker container |
| `sentence-transformers` | Vector embeddings | Required from Phase 2 |

### Installation

```bash
# Install Phase 1
pip install -r requirements.txt

# Install Phase 2 (Ollama option)
pip install -r requirements-phase2-ollama.txt

# Phase 3 uses same packages as Phase 2 (Ollama)
# No additional Python packages needed
```

---

## 📊 Requirements Comparison

| Package | Phase 1 | Phase 2 (Cloud) | Phase 2 (Ollama) | Phase 3 |
|---------|---------|-----------------|------------------|---------|
| `requests` | ✅ | ✅ | ✅ | ✅ |
| `pandas` | ✅ | ✅ | ✅ | ✅ |
| `psycopg2-binary` | ✅ | ✅ | ✅ | ✅ |
| `kafka-python` | ✅ | ✅ | ✅ | ✅ |
| `streamlit` | ✅ | ✅ | ✅ | ✅ |
| `plotly` | ✅ | ✅ | ✅ | ✅ |
| `sentence-transformers` | ❌ | ✅ | ✅ | ✅ |
| `openai` | ❌ | ✅ (optional) | ❌ | ❌ |
| `anthropic` | ❌ | ✅ (optional) | ❌ | ❌ |
| `ollama` | ❌ | ✅ (optional) | ✅ | ✅ |

---

## 🔧 Installation Workflow

### Phase 1 Setup

```bash
# Create virtual environment
uv venv
source .venv/bin/activate

# Install Phase 1 requirements
uv pip install -r requirements.txt

# Verify installation
pip list
```

### Phase 2 Setup (Cloud LLM)

```bash
# Ensure Phase 1 is installed
pip install -r requirements.txt

# Install vector embeddings
pip install sentence-transformers>=2.2.2

# Install LLM API client (choose one)
pip install openai>=1.0.0          # OpenAI
# OR
pip install anthropic>=0.18.0      # Anthropic
# OR
pip install google-generativeai>=0.3.0  # Google Gemini
```

### Phase 2 Setup (Ollama)

```bash
# Ensure Phase 1 is installed
pip install -r requirements.txt

# Install vector embeddings
pip install sentence-transformers>=2.2.2

# Install Ollama client
pip install ollama>=0.1.0

# Start Ollama Docker container
docker-compose up -d ollama
```

### Phase 3 Setup

```bash
# Same as Phase 2 (Ollama)
# No additional Python packages needed
```

---

## 📝 Docker Requirements

### Phase 1 Dockerfile

**File:** `dashboard/Dockerfile` and `producer/Dockerfile`

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

### Phase 2 Dockerfile Update

**Option A: Cloud LLM**

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Phase 2 dependencies
RUN pip install --no-cache-dir sentence-transformers>=2.2.2
RUN pip install --no-cache-dir openai>=1.0.0  # or anthropic, etc.
```

**Option B: Ollama**

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Phase 2 dependencies
RUN pip install --no-cache-dir sentence-transformers>=2.2.2
RUN pip install --no-cache-dir ollama>=0.1.0
```

---

## 🔑 Environment Variables

### Phase 1

```bash
FINNHUB_API_KEY=your_key_here
STOCK_SYMBOLS=AAPL,MSFT,TSLA  # Optional
```

### Phase 2 (Cloud LLM)

```bash
# Phase 1 variables
FINNHUB_API_KEY=your_key_here

# LLM API keys (choose based on provider)
OPENAI_API_KEY=your_openai_key        # For OpenAI
ANTHROPIC_API_KEY=your_anthropic_key  # For Anthropic
GOOGLE_API_KEY=your_google_key        # For Google Gemini
HUGGINGFACE_API_KEY=your_hf_key       # For Hugging Face
```

### Phase 2/3 (Ollama)

```bash
# Phase 1 variables
FINNHUB_API_KEY=your_key_here

# Ollama (no API key needed, runs locally)
OLLAMA_BASE_URL=http://ollama:11434  # Default
```

---

## 📦 Package Size Considerations

### Phase 1
- **Total Size:** ~50-100 MB
- **Installation Time:** 1-2 minutes
- **Dependencies:** Lightweight

### Phase 2 (Cloud LLM)
- **Additional Size:** ~100-200 MB (sentence-transformers)
- **Installation Time:** 2-5 minutes
- **Dependencies:** Moderate (includes torch)

### Phase 2 (Ollama)
- **Additional Size:** ~100-200 MB (sentence-transformers + ollama)
- **Installation Time:** 2-5 minutes
- **Dependencies:** Moderate

### Phase 3
- **Same as Phase 2 (Ollama)**
- **No additional packages**

---

## 🚀 Quick Reference

### Install All Phases (Cloud LLM Path)

```bash
# Phase 1
pip install -r requirements.txt

# Phase 2
pip install sentence-transformers>=2.2.2
pip install openai>=1.0.0  # or your preferred LLM API

# Phase 3: Same as Phase 2
```

### Install All Phases (Ollama Path)

```bash
# Phase 1
pip install -r requirements.txt

# Phase 2
pip install sentence-transformers>=2.2.2
pip install ollama>=0.1.0

# Phase 3: Same as Phase 2
```

---

## 📝 Notes

1. **Phase 1 is standalone** - Can run without Phase 2/3 packages
2. **Phase 2 requires Phase 1** - Install Phase 1 first
3. **Choose LLM provider** - Cloud API or Ollama (not both required)
4. **Docker builds** - Update Dockerfiles when adding Phase 2 packages
5. **Environment variables** - Set appropriate API keys for chosen LLM provider

---

## 🔗 Related Documentation

- [Setup Workflow](SETUP_WORKFLOW.md)
- [Phase Planning](../phases/PHASE_PLANNING.md)
- [Installation Explained](INSTALLATION_EXPLAINED.md)

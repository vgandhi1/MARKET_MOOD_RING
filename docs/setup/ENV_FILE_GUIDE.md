# 🔑 Environment Variables (.env) Guide

## Overview

This guide explains all environment variables needed for Market Mood Ring across all phases.

---

## 📁 File Location

**Create `.env` file in project root:**

```bash
# Copy template
cp .env.example .env

# Edit with your values
nano .env  # or use your preferred editor
```

**Important:** `.env` is in `.gitignore` - never commit it to version control!

---

## 📋 Phase 1: ETL Pipeline (Required)

### Required Variables

```bash
# Finnhub API Key (Required)
FINNHUB_API_KEY=your_finnhub_api_key_here
```

**How to get:**
1. Sign up at [finnhub.io](https://finnhub.io/)
2. Get free API key from dashboard
3. Copy to `.env` file

### Optional Variables

```bash
# Custom Stock Symbols (Optional)
# If not set, uses default 30 tickers from producer/tickers.json
STOCK_SYMBOLS=AAPL,MSFT,TSLA,GOOGL,AMZN
```

---

## 🔮 Phase 2: LLM Integration (Optional)

### LLM Provider Selection

```bash
# Choose your LLM provider
LLM_PROVIDER=openai  # Options: openai, anthropic, google, huggingface, azure, ollama
```

### Provider-Specific API Keys

#### Option 1: OpenAI

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**How to get:**
1. Sign up at [platform.openai.com](https://platform.openai.com/)
2. Go to API Keys section
3. Create new secret key
4. Copy to `.env`

**Models available:**
- `gpt-4` - Most capable
- `gpt-3.5-turbo` - Cost-effective

---

#### Option 2: Anthropic Claude

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
```

**How to get:**
1. Sign up at [console.anthropic.com](https://console.anthropic.com/)
2. Navigate to API Keys
3. Create new key
4. Copy to `.env`

**Models available:**
- `claude-3-opus-20240229` - Most capable
- `claude-3-sonnet-20240229` - Balanced
- `claude-3-haiku-20240307` - Fastest

---

#### Option 3: Google Gemini

```bash
LLM_PROVIDER=google
GOOGLE_API_KEY=your-google-api-key-here
```

**How to get:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Copy to `.env`

**Models available:**
- `gemini-pro` - General purpose
- `gemini-pro-vision` - Multimodal

---

#### Option 4: Hugging Face

```bash
LLM_PROVIDER=huggingface
HUGGINGFACE_API_KEY=hf_your-huggingface-api-key-here
```

**How to get:**
1. Sign up at [huggingface.co](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Create new token
4. Copy to `.env`

**Popular models:**
- `mistralai/Mixtral-8x7B-Instruct-v0.1`
- `meta-llama/Llama-2-70b-chat-hf`

---

#### Option 5: Azure OpenAI

```bash
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**How to get:**
1. Create Azure OpenAI resource in Azure Portal
2. Get endpoint URL
3. Get API key from Keys section
4. Copy all three values to `.env`

---

#### Option 6: Ollama (Local)

```bash
LLM_PROVIDER=ollama
# No API key needed - runs locally in Docker container
# Optional: Customize base URL (default: http://ollama:11434)
# OLLAMA_BASE_URL=http://ollama:11434
```

**Setup:**
1. Uncomment Ollama service in `docker-compose.yaml`
2. Start Ollama: `docker-compose up -d ollama`
3. Initialize model: `docker exec -it market_ollama ollama run llama3`
4. No API key needed!

---

## 📊 Complete .env Example

### Phase 1 Only

```bash
# Phase 1: ETL Pipeline
FINNHUB_API_KEY=your_finnhub_api_key_here
# STOCK_SYMBOLS=AAPL,MSFT,TSLA  # Optional
```

### Phase 2 with OpenAI

```bash
# Phase 1
FINNHUB_API_KEY=your_finnhub_api_key_here

# Phase 2: LLM Integration
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### Phase 2 with Anthropic

```bash
# Phase 1
FINNHUB_API_KEY=your_finnhub_api_key_here

# Phase 2: LLM Integration
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
```

### Phase 2 with Ollama

```bash
# Phase 1
FINNHUB_API_KEY=your_finnhub_api_key_here

# Phase 2: LLM Integration (Local)
LLM_PROVIDER=ollama
# No API key needed for Ollama
```

---

## 🔒 Security Best Practices

### 1. Never Commit .env

**Verify `.gitignore` includes:**
```
.env
.env.local
.env.*.local
```

### 2. Use .env.example Template

```bash
# Copy template
cp .env.example .env

# Edit with your actual keys
nano .env
```

### 3. Environment-Specific Files

```bash
.env              # Local development (gitignored)
.env.example      # Template (committed)
.env.production   # Production (gitignored, set on server)
```

### 4. Key Rotation

- Rotate API keys regularly
- Revoke old keys when creating new ones
- Monitor API usage for suspicious activity

---

## 🔍 Variable Reference

### Phase 1 Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FINNHUB_API_KEY` | ✅ Yes | - | Finnhub API key for stock data |
| `STOCK_SYMBOLS` | ❌ No | `tickers.json` | Comma-separated stock symbols |

### Phase 2 Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LLM_PROVIDER` | ✅ Yes* | `ollama` | LLM provider choice |
| `OPENAI_API_KEY` | ✅ If OpenAI | - | OpenAI API key |
| `ANTHROPIC_API_KEY` | ✅ If Anthropic | - | Anthropic API key |
| `GOOGLE_API_KEY` | ✅ If Google | - | Google Gemini API key |
| `HUGGINGFACE_API_KEY` | ✅ If Hugging Face | - | Hugging Face API key |
| `AZURE_OPENAI_ENDPOINT` | ✅ If Azure | - | Azure OpenAI endpoint |
| `AZURE_OPENAI_API_KEY` | ✅ If Azure | - | Azure OpenAI API key |
| `AZURE_OPENAI_API_VERSION` | ✅ If Azure | `2024-02-15-preview` | Azure API version |
| `OLLAMA_BASE_URL` | ❌ No | `http://ollama:11434` | Ollama server URL |

*Required only if using Phase 2 features

---

## 🧪 Testing Environment Variables

### Check Variables Are Loaded

```bash
# In Python
import os
print(os.getenv('FINNHUB_API_KEY'))
print(os.getenv('LLM_PROVIDER'))
```

### Docker Compose

```bash
# Variables are automatically loaded from .env
docker-compose up -d

# Verify in container
docker exec market_producer env | grep FINNHUB
```

---

## 📝 Quick Setup Checklist

### Phase 1 Setup

- [ ] Copy `.env.example` to `.env`
- [ ] Add `FINNHUB_API_KEY` to `.env`
- [ ] (Optional) Set `STOCK_SYMBOLS` if customizing
- [ ] Verify `.env` is in `.gitignore`

### Phase 2 Setup

- [ ] Choose LLM provider
- [ ] Get API key from chosen provider
- [ ] Set `LLM_PROVIDER` in `.env`
- [ ] Set provider-specific API key in `.env`
- [ ] (If Ollama) Start Ollama container and initialize model

---

## 🔗 Related Documentation

- [LLM API Integration](LLM_API_INTEGRATION.md) - Detailed LLM setup
- [Requirements by Phase](REQUIREMENTS_BY_PHASE.md) - Package requirements
- [Setup Workflow](SETUP_WORKFLOW.md) - Complete setup process

---

## 💡 Tips

1. **Start with Phase 1:** Only need `FINNHUB_API_KEY` initially
2. **Add Phase 2 later:** Can add LLM variables when ready
3. **Test locally first:** Use `.env` for local development
4. **Use secrets in production:** Use environment variables or secret managers
5. **Keep template updated:** Update `.env.example` when adding new variables

---

## 🚨 Common Issues

### Issue: API Key Not Found

**Symptom:** `KeyError: 'FINNHUB_API_KEY'`

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check variable is set
cat .env | grep FINNHUB_API_KEY

# Verify .env is loaded
python -c "import os; print(os.getenv('FINNHUB_API_KEY'))"
```

### Issue: LLM Provider Not Working

**Symptom:** LLM calls failing

**Solution:**
```bash
# Check LLM_PROVIDER is set
echo $LLM_PROVIDER

# Check provider-specific key is set
# For OpenAI:
echo $OPENAI_API_KEY

# Verify key format (should start with 'sk-' for OpenAI)
```

---

## Summary

**Phase 1:** Only `FINNHUB_API_KEY` required  
**Phase 2:** `LLM_PROVIDER` + provider-specific API key  
**Ollama:** No API key needed (runs locally)

Always use `.env.example` as a template and never commit `.env` to version control!

# 🤖 LLM API Integration Guide

## Overview

This guide explains how to integrate various LLM APIs into Market Mood Ring Phase 2, providing alternatives to Ollama for users who prefer cloud-based LLM services.

---

## 🎯 LLM Provider Options

### 1. OpenAI (GPT-4, GPT-3.5)

**Best for:** High-quality responses, fast inference  
**Cost:** Pay-per-use  
**API:** REST API

#### Installation

```bash
pip install openai>=1.0.0
```

#### Configuration

**Environment Variable:**
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

**Code Example:**

```python
import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Generate response
response = client.chat.completions.create(
    model="gpt-4",  # or "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ],
    temperature=0.7,
    max_tokens=500
)

answer = response.choices[0].message.content
```

#### Models Available
- `gpt-4` - Most capable, slower, expensive
- `gpt-4-turbo` - Faster GPT-4 variant
- `gpt-3.5-turbo` - Fast, cost-effective

#### Pricing (Approximate)
- GPT-4: $0.03/1K input tokens, $0.06/1K output tokens
- GPT-3.5-turbo: $0.0015/1K input tokens, $0.002/1K output tokens

---

### 2. Anthropic (Claude)

**Best for:** Long context, detailed analysis  
**Cost:** Pay-per-use  
**API:** REST API

#### Installation

```bash
pip install anthropic>=0.18.0
```

#### Configuration

**Environment Variable:**
```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

**Code Example:**

```python
import os
import anthropic

# Initialize client
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Generate response
message = client.messages.create(
    model="claude-3-opus-20240229",  # or "claude-3-sonnet-20240229"
    max_tokens=500,
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_question}
    ]
)

answer = message.content[0].text
```

#### Models Available
- `claude-3-opus-20240229` - Most capable
- `claude-3-sonnet-20240229` - Balanced performance
- `claude-3-haiku-20240307` - Fastest, most cost-effective

#### Pricing (Approximate)
- Claude 3 Opus: $15/1M input tokens, $75/1M output tokens
- Claude 3 Sonnet: $3/1M input tokens, $15/1M output tokens
- Claude 3 Haiku: $0.25/1M input tokens, $1.25/1M output tokens

---

### 3. Google Gemini

**Best for:** Multimodal capabilities, Google ecosystem  
**Cost:** Free tier available, then pay-per-use  
**API:** REST API

#### Installation

```bash
pip install google-generativeai>=0.3.0
```

#### Configuration

**Environment Variable:**
```bash
GOOGLE_API_KEY=your-api-key-here
```

**Code Example:**

```python
import os
import google.generativeai as genai

# Configure API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Initialize model
model = genai.GenerativeModel('gemini-pro')

# Generate response
response = model.generate_content(
    f"{system_prompt}\n\nUser Question: {user_question}"
)

answer = response.text
```

#### Models Available
- `gemini-pro` - General purpose
- `gemini-pro-vision` - Multimodal (text + images)

#### Pricing (Approximate)
- Free tier: 60 requests/minute
- Paid: $0.00025/1K characters input, $0.0005/1K characters output

---

### 4. Hugging Face Inference API

**Best for:** Open-source models, cost-effective  
**Cost:** Free tier, then pay-per-use  
**API:** REST API

#### Installation

```bash
pip install huggingface-hub>=0.20.0
pip install transformers>=4.41.0
```

#### Configuration

**Environment Variable:**
```bash
HUGGINGFACE_API_KEY=hf_your-api-key-here
```

**Code Example:**

```python
import os
from huggingface_hub import InferenceClient

# Initialize client
client = InferenceClient(
    token=os.getenv('HUGGINGFACE_API_KEY'),
    model="mistralai/Mixtral-8x7B-Instruct-v0.1"
)

# Generate response
response = client.text_generation(
    f"{system_prompt}\n\nUser: {user_question}\n\nAssistant:",
    max_new_tokens=500,
    temperature=0.7
)

answer = response
```

#### Popular Models
- `mistralai/Mixtral-8x7B-Instruct-v0.1` - High quality
- `meta-llama/Llama-2-70b-chat-hf` - Llama 2
- `google/flan-t5-xxl` - Cost-effective

#### Pricing (Approximate)
- Free tier: Limited requests
- Paid: Varies by model ($0.0001-$0.01 per request)

---

### 5. Azure OpenAI

**Best for:** Enterprise, Azure integration  
**Cost:** Pay-per-use  
**API:** REST API (OpenAI compatible)

#### Installation

```bash
pip install openai>=1.0.0
```

#### Configuration

**Environment Variables:**
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Code Example:**

```python
import os
from openai import AzureOpenAI

# Initialize client
client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

# Generate response (same as OpenAI)
response = client.chat.completions.create(
    model="gpt-4",  # Your deployment name
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
)

answer = response.choices[0].message.content
```

---

## 🔄 Integration with Market Mood Ring

### Dashboard Integration Example

**File:** `dashboard/app.py` (Phase 2)

```python
import os
import streamlit as st

# LLM Provider Selection
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')  # openai, anthropic, ollama, etc.

def get_llm_response(context_text, user_question):
    """Get LLM response based on provider"""
    
    system_prompt = f"""You are a Real-Time Financial Sentiment Analyst.
Your goal is to explain market movements to a user based ONLY on the news context provided.

CONTEXT FROM LIVE DATABASE:
{context_text}

USER QUESTION:
{user_question}

INSTRUCTIONS:
1. Analyze the 'CONTEXT' provided above.
2. Be concise (under 3 sentences).
3. Explain financial jargon simply (ELI5 style).
4. End with a "Vibe Check" summary."""
    
    if LLM_PROVIDER == 'openai':
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    elif LLM_PROVIDER == 'anthropic':
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_question}]
        )
        return message.content[0].text
    
    elif LLM_PROVIDER == 'ollama':
        import requests
        response = requests.post(
            "http://ollama:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"{system_prompt}\n\n{user_question}",
                "stream": False
            }
        )
        return response.json()['response']
    
    else:
        return "LLM provider not configured"
```

---

## 📊 Provider Comparison

| Provider | Best For | Cost | Speed | Quality | Setup Difficulty |
|----------|----------|------|-------|---------|-----------------|
| **OpenAI** | General use | Medium | Fast | High | Easy |
| **Anthropic** | Long context | Medium-High | Medium | Very High | Easy |
| **Google Gemini** | Multimodal | Low (free tier) | Fast | High | Easy |
| **Hugging Face** | Open-source | Low | Varies | Medium-High | Medium |
| **Azure OpenAI** | Enterprise | Medium | Fast | High | Medium |
| **Ollama** | Privacy/Local | Free | Medium | High | Medium |

---

## 🔧 Configuration Guide

### Step 1: Choose Provider

Consider:
- **Budget:** Free (Ollama, Gemini free tier) vs Paid
- **Privacy:** Local (Ollama) vs Cloud
- **Performance:** Speed vs Quality
- **Features:** Multimodal, long context, etc.

### Step 2: Install Packages

```bash
# Install Phase 1
pip install -r requirements.txt

# Install Phase 2 base (vector embeddings)
pip install sentence-transformers>=2.2.2

# Install chosen LLM provider
pip install openai>=1.0.0          # OpenAI
# OR
pip install anthropic>=0.18.0      # Anthropic
# OR
pip install google-generativeai>=0.3.0  # Google
# OR
pip install ollama>=0.1.0          # Ollama
```

### Step 3: Set Environment Variables

**Create/Update `.env` file:**

```bash
# Phase 1
FINNHUB_API_KEY=your_key

# Phase 2 - LLM Provider
LLM_PROVIDER=openai  # or anthropic, google, ollama

# Provider-specific keys
OPENAI_API_KEY=sk-...          # For OpenAI
ANTHROPIC_API_KEY=sk-ant-...   # For Anthropic
GOOGLE_API_KEY=...             # For Google
# Ollama doesn't need API key
```

### Step 4: Update Code

Modify `dashboard/app.py` to use chosen provider (see integration example above).

---

## 💡 Recommendations

### For Development/Testing
- **Ollama** - Free, local, no API keys needed
- **Google Gemini** - Free tier available

### For Production (Cloud)
- **OpenAI GPT-3.5** - Best balance of cost/quality
- **Anthropic Claude Haiku** - Fast and cost-effective

### For Production (Enterprise)
- **Azure OpenAI** - Enterprise features, compliance
- **Anthropic Claude** - Long context, detailed analysis

### For Privacy-Critical
- **Ollama** - Complete local control
- **Self-hosted models** - Via Hugging Face

---

## 🔒 Security Considerations

### API Keys
- Store in `.env` file (not in code)
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys regularly

### Rate Limiting
- Implement retry logic with exponential backoff
- Cache responses when appropriate
- Monitor API usage

### Cost Management
- Set usage limits
- Monitor token usage
- Use appropriate model sizes
- Cache common queries

---

## 📝 Migration Checklist

- [ ] Choose LLM provider
- [ ] Install required packages
- [ ] Set environment variables
- [ ] Update `dashboard/app.py` with provider code
- [ ] Test LLM integration
- [ ] Verify vector search works
- [ ] Test end-to-end flow
- [ ] Monitor costs/usage

---

## 🔗 Related Documentation

- [Requirements by Phase](REQUIREMENTS_BY_PHASE.md)
- [Phase Planning](../phases/PHASE_PLANNING.md)
- [Setup Workflow](SETUP_WORKFLOW.md)

---

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index)
- [Ollama Documentation](https://ollama.ai/docs)

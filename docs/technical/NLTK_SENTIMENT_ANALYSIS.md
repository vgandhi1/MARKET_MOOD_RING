# 📊 NLTK Sentiment Analysis Overview

## What is NLTK?

**NLTK (Natural Language Toolkit)** is a Python library for natural language processing (NLP). It provides tools for text analysis, tokenization, classification, and sentiment analysis.

---

## 🎯 NLTK Vader Sentiment Analyzer

### Overview

**VADER (Valence Aware Dictionary and sEntiment Reasoner)** is a lexicon and rule-based sentiment analysis tool specifically attuned to sentiments expressed in social media.

### Why Vader?

- ✅ **Fast:** No machine learning model training required
- ✅ **Accurate:** Designed for social media and short texts
- ✅ **Real-time:** Perfect for stream processing
- ✅ **No external dependencies:** Works offline
- ✅ **Compound score:** Provides -1.0 to +1.0 sentiment score

---

## 📦 Installation

### In Flink Container

**Dockerfile.flink:**
```dockerfile
RUN pip3 install nltk
RUN python3 -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

### Local Development

```bash
pip install nltk
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

---

## 🔧 Usage in Market Mood Ring

### Flink Job Implementation

**File:** `flink_jobs/flink_sentiment.py`

```python
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize analyzer (runs once per task)
sia = SentimentIntensityAnalyzer()

# User Defined Function (UDF) for Flink
@udf(result_type=DataTypes.FLOAT())
def analyze_sentiment(headline: str):
    # Calculate sentiment scores
    score = sia.polarity_scores(str(headline))
    # Return compound score (-1.0 to +1.0)
    return score['compound']
```

### How It Works

```python
# Example input
headline = "Apple announces groundbreaking new product"

# Analyze sentiment
sia = SentimentIntensityAnalyzer()
scores = sia.polarity_scores(headline)

# Output
{
    'neg': 0.0,      # Negative score (0.0 to 1.0)
    'neu': 0.273,    # Neutral score (0.0 to 1.0)
    'pos': 0.727,    # Positive score (0.0 to 1.0)
    'compound': 0.6369  # Overall sentiment (-1.0 to +1.0)
}
```

---

## 📊 Sentiment Score Interpretation

### Compound Score Range

| Score Range | Sentiment | Interpretation |
|-------------|-----------|----------------|
| **> 0.1** | 🟢 Positive | Bullish, optimistic news |
| **-0.1 to 0.1** | 🟡 Neutral | Factual, no clear sentiment |
| **< -0.1** | 🔴 Negative | Bearish, pessimistic news |

### Example Scores

```python
# Very Positive
"Stock surges 20% on strong earnings" → compound: 0.75

# Positive
"Company reports solid quarterly results" → compound: 0.35

# Neutral
"Company announces quarterly earnings report" → compound: 0.05

# Negative
"Stock drops amid regulatory concerns" → compound: -0.45

# Very Negative
"Company faces major lawsuit and potential bankruptcy" → compound: -0.85
```

---

## 🔍 How Vader Works

### 1. Lexicon-Based Analysis

Vader uses a **pre-built dictionary** of words with sentiment scores:
- Positive words: "good" (+2.1), "excellent" (+2.5), "great" (+1.8)
- Negative words: "bad" (-1.8), "terrible" (-2.5), "awful" (-2.1)
- Neutral words: "the" (0.0), "is" (0.0), "company" (0.0)

### 2. Rule-Based Modifiers

Vader applies linguistic rules:
- **Capitalization:** "GREAT" is more intense than "great"
- **Punctuation:** "Great!!!" is more intense than "Great."
- **Negation:** "not good" flips sentiment
- **Intensifiers:** "very good" amplifies sentiment

### 3. Score Calculation

```python
# Step 1: Tokenize text
tokens = ["Apple", "announces", "groundbreaking", "new", "product"]

# Step 2: Look up sentiment scores
scores = {
    "Apple": 0.0,           # Neutral (company name)
    "announces": 0.0,       # Neutral
    "groundbreaking": +2.1, # Very positive
    "new": +0.5,            # Slightly positive
    "product": 0.0          # Neutral
}

# Step 3: Apply modifiers and calculate compound score
compound = normalize(sum(scores))  # Result: 0.6369
```

---

## 📈 Real-World Examples

### Financial News Headlines

```python
# Bullish News
"Tesla stock jumps 15% after record deliveries" 
→ compound: 0.65 (🟢 Positive)

# Bearish News
"Bank stocks tumble amid interest rate fears"
→ compound: -0.55 (🔴 Negative)

# Neutral News
"Company reports Q4 earnings of $2.50 per share"
→ compound: 0.02 (🟡 Neutral)

# Mixed Sentiment
"Stock rises despite concerns over regulatory changes"
→ compound: 0.15 (🟢 Slightly Positive)
```

---

## ⚡ Performance Characteristics

### Speed

- **Processing Time:** ~0.001-0.01 seconds per headline
- **Throughput:** 100-1000 headlines/second (single core)
- **Scalability:** Can process millions of headlines with Flink parallelism

### Accuracy

- **Social Media:** ~80-90% accuracy
- **News Headlines:** ~75-85% accuracy
- **Financial News:** ~70-80% accuracy (domain-specific)

### Limitations

- **Context:** Doesn't understand full article context
- **Sarcasm:** May misinterpret sarcastic statements
- **Domain-Specific:** Financial jargon may not be in lexicon
- **Length:** Works best with short texts (< 280 characters)

---

## 🔄 Integration with Flink

### Stream Processing Flow

```
Kafka Topic (stock_news)
    ↓
Flink Source (reads JSON)
    ↓
UDF: analyze_sentiment(headline)
    ↓
NLTK Vader Processing
    ↓
Sentiment Score (-1.0 to +1.0)
    ↓
PostgreSQL (sentiment_log table)
```

### Code Flow

```python
# 1. Flink reads from Kafka
CREATE TABLE news_source (
    symbol STRING,
    headline STRING,
    ...
)

# 2. UDF processes each headline
@udf(result_type=DataTypes.FLOAT())
def analyze_sentiment(headline: str):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(headline)
    return score['compound']

# 3. Flink writes to PostgreSQL
INSERT INTO sentiment_sink
SELECT symbol, headline, get_sentiment(headline)
FROM news_source
```

---

## 📚 NLTK Data Downloads

### Required Downloads

```python
import nltk

# Download Vader lexicon (required)
nltk.download('vader_lexicon')

# Download tokenizer (required for some operations)
nltk.download('punkt')
```

### What Gets Downloaded

- **vader_lexicon:** Sentiment word dictionary (~1MB)
- **punkt:** Sentence tokenizer (~1MB)

**Location:** `~/nltk_data/` (or `C:\nltk_data\` on Windows)

---

## 🎨 Visualization in Dashboard

### Sentiment Score Display

```python
# Dashboard query
SELECT 
    symbol, 
    headline, 
    sentiment_score,
    CASE 
        WHEN sentiment_score > 0.1 THEN '🟢 Positive'
        WHEN sentiment_score < -0.1 THEN '🔴 Negative'
        ELSE '🟡 Neutral'
    END as sentiment_label
FROM sentiment_log
ORDER BY created_at DESC
```

### Color Coding

- 🟢 **Green:** Positive sentiment (bullish)
- 🟡 **Yellow:** Neutral sentiment
- 🔴 **Red:** Negative sentiment (bearish)

---

## 🔧 Customization

### Adjusting Thresholds

```python
# Custom thresholds
POSITIVE_THRESHOLD = 0.2   # More strict
NEGATIVE_THRESHOLD = -0.2  # More strict

if score > POSITIVE_THRESHOLD:
    sentiment = "Positive"
elif score < NEGATIVE_THRESHOLD:
    sentiment = "Negative"
else:
    sentiment = "Neutral"
```

### Combining with Other Signals

```python
# Weighted sentiment
weighted_score = (
    sentiment_score * 0.7 +      # News sentiment
    price_change_score * 0.3      # Price movement
)
```

---

## 📊 Comparison with Other Methods

| Method | Speed | Accuracy | Training Required | Best For |
|--------|-------|----------|-------------------|----------|
| **NLTK Vader** | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | ❌ No | Real-time, short texts |
| **BERT** | 🐌 Slow | ⭐⭐⭐⭐⭐ Excellent | ✅ Yes | Deep analysis, long texts |
| **TextBlob** | ⚡⚡ Fast | ⭐⭐ Fair | ❌ No | Simple sentiment |
| **Flair** | 🐌 Slow | ⭐⭐⭐⭐ Very Good | ✅ Yes | Domain-specific |

---

## 💡 Best Practices

### 1. Preprocessing

```python
# Clean text before analysis
headline = headline.strip()
headline = headline.lower()  # Optional: normalize case
```

### 2. Error Handling

```python
def analyze_sentiment(headline: str):
    try:
        if not headline or len(headline.strip()) == 0:
            return 0.0  # Neutral for empty headlines
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(str(headline))
        return score['compound']
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0  # Default to neutral on error
```

### 3. Batch Processing

```python
# Process multiple headlines efficiently
headlines = ["Headline 1", "Headline 2", "Headline 3"]
sia = SentimentIntensityAnalyzer()  # Initialize once

scores = [sia.polarity_scores(h)['compound'] for h in headlines]
```

---

## 🔗 Related Documentation

- [Python Files Architecture](../technical/PYTHON_FILES_ARCHITECTURE.md)
- [Flink Sentiment Job](../../flink_jobs/flink_sentiment.py)
- [Phase Planning](../phases/PHASE_PLANNING.md)

---

## 📚 Additional Resources

- [NLTK Documentation](https://www.nltk.org/)
- [Vader Sentiment Paper](https://ojs.aaai.org/index.php/ICWSM/article/view/14550)
- [NLTK Vader GitHub](https://github.com/cjhutto/vaderSentiment)

---

## Summary

**NLTK Vader** is a fast, rule-based sentiment analyzer perfect for:
- ✅ Real-time stream processing
- ✅ Short text analysis (headlines, tweets)
- ✅ No training data required
- ✅ Financial news sentiment analysis

**In Market Mood Ring:**
- Processes news headlines in real-time via Flink
- Provides sentiment scores (-1.0 to +1.0)
- Enables sentiment-based market analysis
- Powers dashboard sentiment visualization

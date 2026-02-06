# 📈 Stock Configuration Guide

## ✅ Regular Stocks (NOT Crypto)

The Market Mood Ring platform is configured to track **regular US stocks** from Finnhub API, **NOT cryptocurrency**.

### Optimized Stock List (30 tickers for high news volume & liquidity)

The system comes pre-configured with **30 optimized tickers** selected for:
- **High news volume** (essential for NLP sentiment analysis)
- **High liquidity** (better price data)
- **Mix of Magnificent Seven tech stocks, volatile favorites, and stable blue chips**

**Tech Giants (High News Volume):**
- AAPL (Apple), MSFT (Microsoft), GOOGL (Alphabet/Google), AMZN (Amazon)
- META (Meta/Facebook), NVDA (Nvidia - AI hype, excellent for sentiment)
- TSLA (Tesla - extremely sensitive to news/tweets)
- NFLX (Netflix), AMD (Advanced Micro Devices), INTC (Intel)

**Financials & Fintech (Market Health Indicators):**
- JPM (JPMorgan Chase), BAC (Bank of America), GS (Goldman Sachs)
- V (Visa), MA (Mastercard), PYPL (PayPal)
- COIN (Coinbase - correlates with crypto "vibes")

**Consumer & Entertainment (Brand Sentiment):**
- DIS (Disney), NKE (Nike), KO (Coca-Cola), PEP (PepsiCo)
- WMT (Walmart), COST (Costco), SBUX (Starbucks), MCD (McDonald's)

**Industrial & Energy (Macro Trends):**
- BA (Boeing - high news volume regarding safety/production)
- XOM (Exxon Mobil), CVX (Chevron)

**Pharma & Retail Favorites:**
- LLY (Eli Lilly - weight loss drug news drives sentiment)
- PLTR (Palantir - retail investor favorite)

## 🔧 Customizing Stock Symbols

You can customize which stocks to track by setting the `STOCK_SYMBOLS` environment variable.

### Option 1: Via .env file

Add to your `.env` file:
```bash
FINNHUB_API_KEY=your_api_key_here
STOCK_SYMBOLS=AAPL,MSFT,TSLA,GOOGL,AMZN,JPM,JNJ
```

### Option 2: Via docker-compose run

When running producers:
```bash
docker-compose run -e STOCK_SYMBOLS="AAPL,TSLA,GOOGL" producer python news_producer.py
```

### Option 3: Export environment variable

```bash
export STOCK_SYMBOLS="AAPL,MSFT,TSLA"
docker-compose run producer python news_producer.py
```

## 📊 Supported Stock Symbols

The system supports **any US stock symbol** available on Finnhub API, including:
- NYSE stocks (e.g., AAPL, JPM, XOM)
- NASDAQ stocks (e.g., MSFT, GOOGL, TSLA)
- Other US exchanges

**Note:** Crypto symbols (like BTC-USD, ETH-USD) are NOT supported. This platform focuses on traditional equity stocks.

## 🔍 Finding Stock Symbols

To find valid stock symbols:
1. Visit [Finnhub Stock Symbols](https://finnhub.io/docs/api/stock-symbols)
2. Use Finnhub's symbol search API
3. Check Yahoo Finance or other financial data providers

## 📝 Examples

### Track only tech stocks:
```bash
STOCK_SYMBOLS=AAPL,MSFT,GOOGL,AMZN,META,NVDA
```

### Track specific companies:
```bash
STOCK_SYMBOLS=TSLA,AAPL,NFLX
```

### Track finance sector:
```bash
STOCK_SYMBOLS=JPM,BAC,GS,V,MA
```

## ⚠️ Important: Finnhub Rate Limits

**Finnhub Free Tier:** 60 API calls per minute

### News Producer Rate Limits
- **Each symbol = 1 API call** (30 symbols = 30 calls per cycle)
- **Default cycle:** Every 60 seconds (30 calls/minute, safe buffer)
- **Recommendation:** If using custom symbols, ensure cycle time respects the limit
- The system automatically calculates safe cycle time based on number of symbols

### Price Producer Rate Limits
- **Price data (Quote API):** Can track all 30 symbols simultaneously without issues
- **Default cycle:** Every 60 seconds (frequent updates)
- **No rate limit concerns** for price data

### Best Practices
- ✅ Use default 30 symbols: Safe with 60-second cycles
- ✅ Custom symbols: System auto-calculates safe cycle time
- ⚠️ If you add more than 30 symbols: Increase cycle time or reduce symbol count
- ⚠️ Don't run multiple news producers simultaneously (will exceed rate limit)

## ⚙️ How It Works

1. **Default Behavior:** If `STOCK_SYMBOLS` is not set or empty, the system uses the optimized list of 30 stocks
2. **Custom List:** If `STOCK_SYMBOLS` is set, only those symbols are tracked
3. **Case Insensitive:** Symbols are automatically converted to uppercase
4. **Whitespace Handling:** Extra spaces are automatically trimmed
5. **Rate Limit Protection:** News producer automatically adjusts cycle time based on symbol count

## 🚀 Quick Start

1. **Use default stocks** (no configuration needed):
   ```bash
   docker-compose run producer python news_producer.py
   ```

2. **Use custom stocks**:
   ```bash
   echo "STOCK_SYMBOLS=AAPL,TSLA,GOOGL" >> .env
   docker-compose run producer python news_producer.py
   ```

---

**Last Updated:** Configuration supports regular US stocks only (NOT crypto)

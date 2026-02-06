# 📊 Ticker Configuration Guide

## Overview

Stock tickers are now managed via a seed file (`tickers.json`) instead of hardcoded lists. This makes it easy to add, remove, or modify tickers without editing Python code.

## File Location

- **Seed File:** `producer/tickers.json`
- **Format:** JSON with structured ticker data

## How to Modify Tickers

### Option 1: Edit `tickers.json` (Recommended)

Simply edit `producer/tickers.json` to add, remove, or modify tickers:

```json
{
  "description": "Optimized stock tickers for Market Mood Ring",
  "version": "1.0",
  "tickers": [
    {
      "symbol": "AAPL",
      "name": "Apple",
      "sector": "Technology",
      "category": "Tech Giants"
    },
    {
      "symbol": "NEWTICKER",
      "name": "New Company",
      "sector": "Technology",
      "category": "Tech Giants"
    }
  ]
}
```

**To add a ticker:**
1. Add a new object to the `tickers` array
2. Include at minimum: `symbol` field
3. Optional: `name`, `sector`, `category`, `notes`

**To remove a ticker:**
1. Delete the ticker object from the `tickers` array

**To modify a ticker:**
1. Edit the existing ticker object in the `tickers` array

### Option 2: Environment Variable Override

For quick testing or temporary changes, use the `STOCK_SYMBOLS` environment variable:

```bash
# In .env file:
STOCK_SYMBOLS=AAPL,MSFT,TSLA,GOOGL

# Or via command:
docker-compose run -e STOCK_SYMBOLS="AAPL,MSFT" producer python news_producer.py
```

**Priority Order:**
1. `STOCK_SYMBOLS` environment variable (highest priority)
2. `tickers.json` file
3. Default hardcoded list (fallback)

## Ticker File Structure

```json
{
  "description": "Description of the ticker list",
  "version": "1.0",
  "tickers": [
    {
      "symbol": "AAPL",        // Required: Stock ticker symbol
      "name": "Apple",          // Optional: Company name
      "sector": "Technology",  // Optional: Sector classification
      "category": "Tech Giants", // Optional: Category grouping
      "notes": "Optional notes"  // Optional: Additional information
    }
  ]
}
```

## Examples

### Add a New Ticker

```json
{
  "symbol": "IBM",
  "name": "International Business Machines",
  "sector": "Technology",
  "category": "Tech Giants"
}
```

### Remove a Ticker

Simply delete the entire ticker object from the array.

### Modify Existing Ticker

Change any field in the ticker object:

```json
{
  "symbol": "TSLA",
  "name": "Tesla Inc",
  "sector": "Automotive",
  "category": "Tech Giants",
  "notes": "Updated sector classification"
}
```

## Validation

The system will:
- ✅ Load tickers from `tickers.json` if it exists
- ✅ Extract only the `symbol` field (other fields are metadata)
- ✅ Convert symbols to uppercase automatically
- ✅ Fall back to default list if file is missing or invalid
- ✅ Warn if file cannot be loaded

## Rate Limit Considerations

Remember: **Each ticker = 1 API call** for news data.

- **Finnhub Free Tier:** 60 calls/minute
- **30 tickers:** Safe with 60-second cycle (30 calls/min)
- **More tickers:** System auto-adjusts cycle time

See `TICKER_OPTIMIZATION.md` for rate limit details.

## Best Practices

1. **Keep tickers.json in version control** - Easy to track changes
2. **Use descriptive categories** - Helps organize tickers
3. **Add notes for special tickers** - Document why certain tickers are included
4. **Test with small lists first** - Verify changes work before scaling up
5. **Monitor rate limits** - Don't exceed Finnhub limits

## Troubleshooting

**Problem:** Tickers not loading from file
- **Solution:** Check JSON syntax is valid
- **Solution:** Ensure file is in `producer/` directory
- **Solution:** Check file permissions

**Problem:** Want to use different tickers temporarily
- **Solution:** Use `STOCK_SYMBOLS` environment variable

**Problem:** File changes not taking effect
- **Solution:** Restart the producer container
- **Solution:** Check if environment variable is overriding

---

**Last Updated:** Ticker management via seed file

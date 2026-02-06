#!/usr/bin/env python3
"""
News Producer: Fetches regular stock news (NOT crypto) from Finnhub API and publishes to Kafka
Supports all US stock symbols available on Finnhub (AAPL, MSFT, TSLA, etc.)
"""
import os
import time
import json
import requests
from kafka import KafkaProducer
from datetime import datetime
from pathlib import Path

# Configuration
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
TOPIC_NAME = 'stock_news'
TICKERS_FILE = Path(__file__).parent / 'tickers.json'

def load_tickers():
    """
    Load ticker symbols from seed file (tickers.json) or environment variable.
    Priority: STOCK_SYMBOLS env var > tickers.json > default fallback
    """
    # Priority 1: Environment variable override
    symbols_env = os.getenv('STOCK_SYMBOLS', '').strip()
    if symbols_env:
        return [s.strip().upper() for s in symbols_env.split(',') if s.strip()]
    
    # Priority 2: Load from tickers.json seed file
    try:
        if TICKERS_FILE.exists():
            with open(TICKERS_FILE, 'r') as f:
                ticker_data = json.load(f)
                # Extract symbols from ticker objects
                symbols = [ticker['symbol'] for ticker in ticker_data.get('tickers', [])]
                if symbols:
                    print(f"✅ Loaded {len(symbols)} tickers from {TICKERS_FILE.name}")
                    return symbols
    except Exception as e:
        print(f"⚠️  Warning: Could not load tickers.json: {e}")
        print(f"   Falling back to default ticker list")
    
    # Priority 3: Default fallback (if file doesn't exist or is invalid)
    return [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX', 'AMD', 'INTC',
        'JPM', 'BAC', 'GS', 'V', 'MA', 'PYPL', 'COIN',
        'DIS', 'NKE', 'KO', 'PEP', 'WMT', 'COST', 'SBUX', 'MCD',
        'BA', 'XOM', 'CVX', 'LLY', 'PLTR'
    ]

# Load ticker symbols
SYMBOLS = load_tickers()

def get_finnhub_news(symbol, api_key):
    """Fetch news for a symbol from Finnhub API"""
    url = f"https://finnhub.io/api/v1/company-news"
    params = {
        'symbol': symbol,
        'from': datetime.now().strftime('%Y-%m-%d'),
        'to': datetime.now().strftime('%Y-%m-%d'),
        'token': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []

def main():
    if not FINNHUB_API_KEY:
        print("ERROR: FINNHUB_API_KEY environment variable not set!")
        return
    
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        retries=3
    )
    
    num_symbols = len(SYMBOLS)
    print(f"📰 News Producer started. Publishing to topic: {TOPIC_NAME}")
    print(f"Monitoring {num_symbols} symbols: {', '.join(SYMBOLS)}")
    
    # Rate limit warning: Finnhub Free Tier = 60 calls/minute
    # Each symbol = 1 API call, so 30 symbols = 30 calls
    # Recommendation: Run cycle every 60 seconds (30 calls/minute, safe buffer)
    if num_symbols > 30:
        print(f"⚠️  WARNING: {num_symbols} symbols will use {num_symbols} API calls per cycle.")
        print(f"   Finnhub Free Tier limit: 60 calls/minute. Consider reducing symbols or increasing cycle time.")
    
    # Calculate safe cycle time: ensure we stay under 60 calls/minute
    # If we have N symbols, we need at least N/60 minutes between cycles
    # For safety, use 60 seconds (1 minute) minimum
    cycle_time = max(60, int((num_symbols / 60) * 60) + 5)  # Add 5 second buffer
    print(f"⏱️  Rate limit: Running cycle every {cycle_time} seconds ({num_symbols} calls per cycle)")
    
    # Track published headlines to avoid duplicates
    published_headlines = set()
    
    try:
        cycle_count = 0
        while True:
            cycle_count += 1
            print(f"\n🔄 Cycle #{cycle_count} - Fetching news for {num_symbols} symbols...")
            api_calls_made = 0
            
            for symbol in SYMBOLS:
                news_items = get_finnhub_news(symbol, FINNHUB_API_KEY)
                api_calls_made += 1
                
                for news in news_items[:5]:  # Limit to 5 most recent per symbol
                    headline = news.get('headline', '')
                    summary = news.get('summary', '')
                    news_id = news.get('id', 0)
                    
                    # Skip if already published
                    if news_id in published_headlines:
                        continue
                    
                    # Prepare message
                    message = {
                        'symbol': symbol,
                        'headline': headline,
                        'summary': summary or headline,
                        'source': news.get('source', 'Unknown'),
                        'url': news.get('url', ''),
                        'ts': news.get('datetime', int(time.time()))
                    }
                    
                    # Publish to Kafka
                    try:
                        producer.send(TOPIC_NAME, value=message)
                        published_headlines.add(news_id)
                        print(f"✅ Published: {symbol} - {headline[:50]}...")
                    except Exception as e:
                        print(f"❌ Error publishing to Kafka: {e}")
            
            print(f"📊 Cycle complete: Made {api_calls_made} API calls. Waiting {cycle_time} seconds before next cycle...")
            time.sleep(cycle_time)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down news producer...")
    finally:
        producer.close()

if __name__ == '__main__':
    main()

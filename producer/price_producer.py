#!/usr/bin/env python3
"""
Price Producer: Fetches regular stock prices (NOT crypto) from Finnhub API and publishes to Kafka
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
TOPIC_NAME = 'stock_prices'
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

def get_finnhub_quote(symbol, api_key):
    """Fetch current quote for a symbol from Finnhub API"""
    url = f"https://finnhub.io/api/v1/quote"
    params = {
        'symbol': symbol,
        'token': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Finnhub returns: c (current price), h, l, o, pc (previous close)
        if data.get('c') and data['c'] > 0:
            return {
                'symbol': symbol,
                'price': float(data['c']),
                'high': float(data.get('h', 0)),
                'low': float(data.get('l', 0)),
                'open': float(data.get('o', 0)),
                'previous_close': float(data.get('pc', 0)),
                'timestamp': datetime.utcnow().isoformat()
            }
        return None
    except Exception as e:
        print(f"Error fetching quote for {symbol}: {e}")
        return None

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
    print(f"💰 Price Producer started. Publishing to topic: {TOPIC_NAME}")
    print(f"Monitoring {num_symbols} symbols: {', '.join(SYMBOLS)}")
    print(f"💡 Note: Price data uses WebSocket/Quote API - can track all {num_symbols} simultaneously without rate limit issues")
    
    try:
        cycle_count = 0
        while True:
            cycle_count += 1
            print(f"\n🔄 Cycle #{cycle_count} - Fetching prices for {num_symbols} symbols...")
            
            for symbol in SYMBOLS:
                quote = get_finnhub_quote(symbol, FINNHUB_API_KEY)
                
                if quote:
                    try:
                        producer.send(TOPIC_NAME, value=quote)
                        print(f"✅ Published: {symbol} @ ${quote['price']:.2f}")
                    except Exception as e:
                        print(f"❌ Error publishing to Kafka: {e}")
                
                # Small delay between symbols to avoid overwhelming API
                time.sleep(0.2)
            
            # Wait 1 minute before next cycle (prices update frequently)
            print(f"⏳ Waiting 60 seconds before next fetch cycle...")
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down price producer...")
    finally:
        producer.close()

if __name__ == '__main__':
    main()

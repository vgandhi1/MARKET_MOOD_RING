#!/usr/bin/env python3
"""
Price Consumer: Consumes stock prices from Kafka and writes to PostgreSQL
"""
import os
import json
import psycopg2
from kafka import KafkaConsumer

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
TOPIC_NAME = 'stock_prices'
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'market_mood')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'market_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'market_password')

def main():
    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=5432
        )
        cursor = conn.cursor()
        print(f"✅ Connected to PostgreSQL database: {POSTGRES_DB}")
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        return
    
    # Initialize Kafka consumer
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    
    print(f"💰 Price Consumer started. Listening to topic: {TOPIC_NAME}")
    
    try:
        for message in consumer:
            data = message.value
            symbol = data.get('symbol')
            price = data.get('price')
            
            if symbol and price:
                try:
                    cursor.execute(
                        "INSERT INTO price_log (symbol, price, timestamp) VALUES (%s, %s, NOW())",
                        (symbol, price)
                    )
                    conn.commit()
                    print(f"✅ Stored: {symbol} @ ${price:.2f}")
                except Exception as e:
                    print(f"❌ Error inserting price: {e}")
                    conn.rollback()
            else:
                print(f"⚠️ Invalid message format: {data}")
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down price consumer...")
    finally:
        cursor.close()
        conn.close()
        consumer.close()

if __name__ == '__main__':
    main()

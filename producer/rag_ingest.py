# producer/rag_ingest.py
# PHASE 2: RAG Pipeline - Creates embeddings and stores in financial_knowledge table
# This script is ready but not used in Phase 1
# Uncomment financial_knowledge table in init.sql before using this script

from kafka import KafkaConsumer
import psycopg2
import json
from sentence_transformers import SentenceTransformer

# 1. Load a small, free embedding model
# 'all-MiniLM-L6-v2' is fast and perfect for this
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Connect to DB
conn = psycopg2.connect("dbname=market_mood user=market_user password=market_password host=postgres")
cursor = conn.cursor()

consumer = KafkaConsumer('stock_news', bootstrap_servers='kafka:29092')

print("🧠 The Professor is listening...")

for msg in consumer:
    data = json.loads(msg.value.decode('utf-8'))
    
    # Create a rich text chunk
    # e.g. "Apple (AAPL) Headline: New Headset Released. Summary: Apple announced..."
    text_content = f"{data['symbol']} Headline: {data['headline']}. Summary: {data['summary']}"
    
    # 3. Create Vector (The Magic)
    vector = model.encode(text_content).tolist()
    
    # 4. Save to pgvector
    cursor.execute(
        "INSERT INTO financial_knowledge (symbol, content, embedding) VALUES (%s, %s, %s)",
        (data['symbol'], text_content, vector)
    )
    conn.commit()
    print(f"Stored knowledge for {data['symbol']}")
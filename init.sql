-- Initialize PostgreSQL database for Market Mood Ring
-- Database: market_mood
-- This script runs automatically when the postgres container starts for the first time
-- via docker-entrypoint-initdb.d

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Note: User creation is handled by POSTGRES_USER env var in docker-compose.yaml
-- Grant privileges on schema
GRANT ALL PRIVILEGES ON SCHEMA public TO market_user;

-- Table 1: price_log (Time Series)
CREATE TABLE IF NOT EXISTS price_log (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: sentiment_log (Enriched Data)
CREATE TABLE IF NOT EXISTS sentiment_log (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    headline TEXT NOT NULL,
    sentiment_score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: financial_knowledge (Vector Store) - PHASE 2: RAG Pipeline
-- Enabled for Combined Phase Development
CREATE TABLE IF NOT EXISTS financial_knowledge (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    content TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant table privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO market_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO market_user;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_price_log_symbol_timestamp ON price_log(symbol, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_sentiment_log_symbol ON sentiment_log(symbol);
-- PHASE 2: Enabled for RAG pipeline
CREATE INDEX IF NOT EXISTS idx_financial_knowledge_symbol ON financial_knowledge(symbol);
CREATE INDEX IF NOT EXISTS idx_financial_knowledge_embedding ON financial_knowledge USING ivfflat (embedding vector_cosine_ops);

-- Tables created successfully
-- You can verify with: \dt

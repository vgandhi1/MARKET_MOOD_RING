from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, DataTypes
from pyflink.table.udf import udf
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# 1. Define the Sentiment Logic (UDF - User Defined Function)
@udf(result_type=DataTypes.FLOAT())
def analyze_sentiment(headline: str):
    # This runs INSIDE the Flink cluster
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(str(headline))
    return score['compound'] # Returns float between -1 (Negative) and +1 (Positive)

def sentiment_job():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(env)

    # 2. Define Source (Kafka)
    t_env.execute_sql("""
        CREATE TABLE news_source (
            symbol STRING,
            headline STRING,
            summary STRING,
            ts DOUBLE
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'stock_news',
            'properties.bootstrap.servers' = 'kafka:29092',
            'properties.group.id' = 'flink-sentiment-consumer',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        )
    """)

    # 3. Define Sink (Postgres)
    t_env.execute_sql("""
        CREATE TABLE sentiment_sink (
            symbol STRING,
            headline STRING,
            sentiment_score FLOAT
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/market_mood',
            'table-name' = 'sentiment_log',
            'username' = 'market_user',
            'password' = 'market_password'
        )
    """)

    # 4. Register the UDF
    t_env.create_temporary_function("get_sentiment", analyze_sentiment)

    # 5. Process & Write
    # We read Kafka -> Apply Function -> Write to DB
    t_env.execute_sql("""
        INSERT INTO sentiment_sink
        SELECT 
            symbol, 
            headline, 
            get_sentiment(headline) 
        FROM news_source
    """)

if __name__ == '__main__':
    sentiment_job()
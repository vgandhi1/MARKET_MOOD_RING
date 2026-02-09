import streamlit as st
import psycopg2
# PHASE 2: Enabled for Combined Phase Development
from sentence_transformers import SentenceTransformer
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os

# Page Configuration
st.set_page_config(
    page_title="Market Mood Ring",
    page_icon="🦍",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# PHASE 2: Enabled for Combined Phase Development
# Load embedding model (cached)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# Database connection (cached)
@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="market_mood",
            user="market_user",
            password="market_password",
            host="postgres",
            port=5432
        )
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# PHASE 2: Enabled for Combined Phase Development
model = load_model()
conn = get_db_connection()

# Sidebar Navigation
st.sidebar.title("🦍 Market Mood Ring - Combined Phase")
# PHASE 1 & 2 Combined
page = st.sidebar.selectbox(
    "Navigate",
    ["📊 Live Dashboard", "💬 AI Analyst"]
)

# ===== PAGE 1: LIVE DASHBOARD =====
if page == "📊 Live Dashboard":
    st.title("📊 Real-Time Market Dashboard")
    
    if conn is None:
        st.error("⚠️ Cannot connect to database. Please ensure PostgreSQL is running.")
        st.stop()
    
    # Fetch recent prices
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT symbol, price, timestamp 
            FROM price_log 
            WHERE timestamp > NOW() - INTERVAL '72 hours'
            ORDER BY timestamp DESC
            LIMIT 1000
        """)
        price_data = cursor.fetchall()
        
        if price_data:
            df_prices = pd.DataFrame(price_data, columns=['symbol', 'price', 'timestamp'])
            
            # Symbol selector
            symbols = sorted(df_prices['symbol'].unique())
            selected_symbol = st.selectbox("Select Stock Symbol", symbols)
            
            # Filter data for selected symbol
            df_filtered = df_prices[df_prices['symbol'] == selected_symbol].copy()
            df_filtered = df_filtered.sort_values('timestamp')
            
            if not df_filtered.empty:
                # Price Chart
                fig = px.line(
                    df_filtered, 
                    x='timestamp', 
                    y='price',
                    title=f"{selected_symbol} Price Trend (Last 72 Hours)",
                    labels={'price': 'Price ($)', 'timestamp': 'Time'}
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # Latest price
                latest_price = df_filtered.iloc[-1]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${latest_price['price']:.2f}")
                with col2:
                    st.metric("Symbol", latest_price['symbol'])
                with col3:
                    st.metric("Last Update", latest_price['timestamp'].strftime("%H:%M:%S UTC"))
            else:
                st.info(f"No price data available for {selected_symbol} in the last 72 hours.")
        else:
            st.info("No price data available. Start the price producer to see live data.")
            
    except Exception as e:
        st.error(f"Error fetching price data: {e}")
    
    # Recent Sentiment Scores
    st.subheader("📈 Recent Sentiment Scores")
    try:
        cursor.execute("""
            SELECT symbol, headline, sentiment_score, 
                   CASE 
                       WHEN sentiment_score > 0.1 THEN '🟢 Positive'
                       WHEN sentiment_score < -0.1 THEN '🔴 Negative'
                       ELSE '🟡 Neutral'
                   END as sentiment_label
            FROM sentiment_log 
            ORDER BY symbol, sentiment_score DESC
            LIMIT 20
        """)
        sentiment_data = cursor.fetchall()
        
        if sentiment_data:
            df_sentiment = pd.DataFrame(
                sentiment_data, 
                columns=['symbol', 'headline', 'sentiment_score', 'sentiment_label']
            )
            st.dataframe(df_sentiment, use_container_width=True, hide_index=True)
        else:
            st.info("No sentiment data available. Start the Flink job to see sentiment analysis.")
            
    except Exception as e:
        st.error(f"Error fetching sentiment data: {e}")

# ===== PAGE 2: AI ANALYST (PHASE 2) =====
# PHASE 2: Enabled for Combined Phase Development
elif page == "💬 AI Analyst":
    st.title("💬 AI Financial Analyst")
    st.markdown("Ask me about market movements, stock news, or sentiment analysis!")
    
    if conn is None:
        st.error("⚠️ Cannot connect to database. Please ensure PostgreSQL is running.")
        st.stop()
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    prompt = st.chat_input("Ask about stocks, news, or market sentiment...")
    
    if prompt:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.status("🧠 Consulting the Local Oracle...", expanded=False) as status:
                
                # A. Vector Search (The Librarian)
                try:
                    query_vector = model.encode(prompt).tolist()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT content FROM financial_knowledge 
                        ORDER BY embedding <-> %s::vector 
                        LIMIT 3;
                    """, (query_vector,))
                    results = cursor.fetchall()
                    context_text = "\n".join([r[0] for r in results]) if results else "No recent news found."
                except Exception as e:
                    context_text = f"Error retrieving context: {e}"
                    st.warning(f"Vector search error: {e}")
                
                status.update(label="💡 Llama 3 is thinking...", state="running")
                
                # B. Generate Answer (The Mouth) - OLLAMA
                try:
                    full_prompt = f"""You are a Real-Time Financial Sentiment Analyst.
Your goal is to explain market movements to a user based ONLY on the news context provided.

CONTEXT FROM LIVE DATABASE:
{context_text}

USER QUESTION:
{prompt}

INSTRUCTIONS:
1. Analyze the 'CONTEXT' provided above. It contains recent news headlines and sentiment scores.
2. If the user asks "Why is [Stock] moving?", look for positive or negative events in the context.
3. If the context has no relevant news, admit it. Say: "I don't see any recent news for [Stock] in my live database."
4. Be concise (under 3 sentences).
5. Explain financial jargon simply (ELI5 style).
6. End with a "Vibe Check" summary (e.g., "Overall Vibe: 🐻 Bearish due to regulatory fears")."""
                    
                    # Call Local Ollama (Windows Host via Docker internal gateway)
                    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
                    response = requests.post(
                        f"{ollama_base_url}/api/generate",
                        json={
                            "model": "llama3",
                            "prompt": full_prompt,
                            "stream": False
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        bot_reply = response.json()['response']
                    else:
                        bot_reply = f"Error: Ollama returned {response.status_code}. Make sure Ollama is running and llama3 model is pulled."
                        
                except requests.exceptions.ConnectionError:
                    bot_reply = "⚠️ Cannot reach Ollama on Windows Host. Please ensure:\n1. Ollama is running on Windows\n2. Env Var `OLLAMA_HOST=0.0.0.0:11434` is set on Windows\n3. You restarted Ollama after setting the variable."
                except Exception as e:
                    bot_reply = f"I cannot reach Ollama. Error: {e}"
                
                status.update(label="✅ Answer Ready!", state="complete")
            
            # Display Bot Reply
            st.markdown(bot_reply)
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

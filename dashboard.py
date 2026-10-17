import streamlit as st
import duckdb
import pandas as pd
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Using the model that is compatible with your API key
model = genai.GenerativeModel('gemini-3.5-flash-lite')

st.set_page_config(page_title="Live AI Dashboard", page_icon="⚡", layout="wide")
st.title("⚡ Real-Time E-Commerce AI Dashboard")
st.markdown("Monitoring live streaming events from Aiven Kafka.")

# Function to fetch data from DuckDB (with lock-handling)
def get_data():
    for _ in range(3): # Try 3 times if locked
        try:
            # Connect in read-only mode
            conn = duckdb.connect('streaming_data.duckdb', read_only=True)
            df = conn.execute("SELECT * FROM live_events ORDER BY timestamp DESC").df()
            conn.close()
            return df
        except Exception as e:
            # If locked by the consumer, wait 1 second and retry
            time.sleep(1)
    return pd.DataFrame()

df = get_data()

if df.empty:
    st.warning("No data available yet. Make sure your consumer and producer are running, and the database is not locked!")
else:
    # --- KPI METRICS ---
    total_events = len(df)
    total_revenue = df[df['event_type'] == 'purchase']['price'].sum()
    unique_users = df['user_id'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events Streamed", f"{total_events:,}")
    col2.metric("Live Revenue (Purchases)", f"${total_revenue:,.2f}")
    col3.metric("Unique Live Users", f"{unique_users:,}")

    st.divider()

    # --- CHARTS & DATA ---
    col_chart, col_data = st.columns([1, 1])
    
    with col_chart:
        st.subheader("Event Type Distribution")
        event_counts = df['event_type'].value_counts()
        st.bar_chart(event_counts)

    with col_data:
        st.subheader("Latest 15 Events")
        st.dataframe(
            df[['timestamp', 'event_type', 'user_id', 'price']].head(15), 
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # --- AI INTEGRATION ---
    st.subheader("🤖 AI Stream Analysis")
    st.markdown("Click the button below to have Google Gemini analyze the most recent stream data for trends or anomalies.")
    
    if st.button("Analyze Stream with AI"):
        with st.spinner("Gemini is analyzing the live stream..."):
            # Grab the latest 30 events as a text summary for the AI
            recent_data = df.head(30).to_csv(index=False)
            
            prompt = f"""
            You are an expert real-time data analyst monitoring an e-commerce website.
            Here is the most recent stream of user events (CSV format):
            
            {recent_data}
            
            Based on this data, provide a 2-sentence summary of what is currently happening on the site. 
            Highlight any interesting trends (e.g., high value purchases) or anomalies (e.g., lots of users viewing but no one buying).
            Keep it professional and concise.
            """
            
            try:
                response = model.generate_content(prompt)
                st.success("Analysis Complete!")
                st.info(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.warning("Rate limit hit. Waiting 15 seconds before retrying...")
                    time.sleep(15)
                    try:
                        response = model.generate_content(prompt)
                        st.success("Analysis Complete!")
                        st.info(response.text)
                    except Exception as e2:
                        st.error(f"Still hitting rate limit. Please try again in a minute. Error: {e2}")
                else:
                    st.error(f"AI Error: {e}")
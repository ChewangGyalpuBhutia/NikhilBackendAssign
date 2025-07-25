import pandas as pd
import pyxirr
import streamlit as st
import yfinance as yf
import feedparser

# Load preprocessed dataset
df = pd.read_csv('final_dataset.csv')

# --- Compute daily portfolio value across currencies ---
df['Value_USD'] = df['Quantity'] * df['Split_Adjusted_Close']
df['Value_INR'] = df['Quantity'] * df['Split_Adjusted_Close'] * df['USDINR']
df['Value_SGD'] = df['Quantity'] * df['Split_Adjusted_Close'] * df['USDSGD']

# Group by date to get daily total portfolio value
daily_portfolio = df.groupby('Date')[['Value_USD', 'Value_INR', 'Value_SGD']].sum().reset_index()

# --- Load XIRR results from CSV ---
xirr_df = pd.read_csv('xirr_results.csv')

# --- Streamlit UI with Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["Portfolio Dashboard", "Raw Data", "Latest News", "XIRR Values"])

with tab1:
    st.title("Portfolio Dashboard")

    st.header("Daily Portfolio Value")
    st.dataframe(daily_portfolio)

with tab2:
    st.title("Raw Data: final_dataset.csv")
    st.dataframe(df)

with tab3:
    st.title("Latest News for Holdings")

    def fetch_yahoo_rss(symbol, max_news=5):
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
        feed = feedparser.parse(url)
        news_items = []
        for entry in feed.entries[:max_news]:
            news_items.append({
                'title': entry.title,
                'link': entry.link
            })
        return news_items

    for symbol in df['Symbol'].dropna().unique():
        st.subheader(f"News for {symbol}")
        news_items = fetch_yahoo_rss(symbol)
        if news_items:
            for item in news_items:
                st.write(f"- [{item['title']}]({item['link']})")
        else:
            st.write("No news found.")

with tab4:
    st.title("XIRR Values for Each Holding")
    st.markdown("**Note:** XIRR is calculated as of 2025-07-17 using the portfolio value on that date.")
    # Convert XIRR to percentage (if not error)
    xirr_df_display = xirr_df.copy()
    def to_percent(val):
        try:
            return f"{float(val)*100:.2f}%" 
        except:
            return val
    xirr_df_display['XIRR'] = xirr_df_display['XIRR'].apply(to_percent)
    st.dataframe(xirr_df_display)
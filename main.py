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

# --- Compute XIRR for each holding ---
xirr_results = {}
for symbol in df['Symbol'].dropna().unique():
    holding = df[df['Symbol'] == symbol]
    cashflows = holding['Proceeds'].values
    dates = pd.to_datetime(holding['Date/Time'], errors='coerce').values
    if len(cashflows) >= 2:
        try:
            xirr_val = pyxirr.xirr(dates, cashflows)
            xirr_results[symbol] = xirr_val
        except Exception as e:
            xirr_results[symbol] = f"Error: {e}"
    else:
        xirr_results[symbol] = "Not enough data"

# --- Streamlit UI with Tabs ---
tab1, tab2, tab3 = st.tabs(["Portfolio Dashboard", "Raw Data", "Latest News"])

with tab1:
    st.title("Portfolio Dashboard")

    st.header("Daily Portfolio Value")
    st.dataframe(daily_portfolio)

    st.header("XIRR for Each Holding")
    for symbol, xirr_val in xirr_results.items():
        st.write(f"{symbol}: {xirr_val}")

    # st.line_chart(daily_portfolio.set_index('Date')[['Value_USD', 'Value_INR', 'Value_SGD']])

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
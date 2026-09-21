import streamlit as st
import yfinance as yf
import plotly.express as px

TICKERS = ["MSFT", "IBM", "WMT", "JPM", "JNJ"]

st.set_page_config(page_title="Stock Close Prices", layout="wide")
st.title("Stock Close Price - Past Year")

ticker = st.selectbox("Choose a stock", TICKERS)


@st.cache_data(ttl=3600)
def load_prices(symbol: str):
    df = yf.Ticker(symbol).history(period="1y")
    df = df.reset_index()[["Date", "Close"]]
    df["Date"] = df["Date"].dt.tz_localize(None)
    return df


data = load_prices(ticker)

if data.empty:
    st.error(f"No data returned for {ticker}.")
else:
    fig = px.line(data, x="Date", y="Close", title=f"{ticker} Close Price (USD)")
    fig.update_layout(yaxis_title="Close Price (USD)", xaxis_title="Date")
    st.plotly_chart(fig, use_container_width=True)

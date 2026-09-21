import yfinance as yf

TICKERS = ["MSFT", "IBM", "WMT", "JPM", "JNJ"]
OUTPUT = "stock_prices.csv"

frames = []
for symbol in TICKERS:
    hist = yf.Ticker(symbol).history(period="1y").reset_index()
    hist = hist[["Date", "Close"]]
    hist["Date"] = hist["Date"].dt.strftime("%Y-%m-%d")
    hist["Close"] = hist["Close"].round(2)
    hist.insert(0, "Ticker", symbol)
    frames.append(hist)

import pandas as pd

pd.concat(frames, ignore_index=True).to_csv(OUTPUT, index=False)
print(f"Wrote {OUTPUT}")

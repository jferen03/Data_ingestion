import json

import yfinance as yf

TICKERS = ["MSFT", "IBM", "WMT", "JPM", "JNJ"]
OUTPUT = "stock_chart.html"

data = {}
for symbol in TICKERS:
    hist = yf.Ticker(symbol).history(period="1y")
    data[symbol] = {
        "dates": [d.strftime("%Y-%m-%d") for d in hist.index],
        "close": [round(float(c), 2) for c in hist["Close"]],
    }

options = "\n".join(f'      <option value="{t}">{t}</option>' for t in TICKERS)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Stock Close Prices</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    body {{ font-family: sans-serif; margin: 2rem; }}
    select {{ font-size: 1rem; padding: 0.25rem; }}
  </style>
</head>
<body>
  <h1>Stock Close Price - Past Year</h1>
  <label for="ticker">Choose a stock: </label>
  <select id="ticker">
{options}
  </select>
  <div id="chart" style="width:100%;height:500px;"></div>

  <script>
    const data = {json.dumps(data)};

    function draw(symbol) {{
      const d = data[symbol];
      Plotly.newPlot("chart", [{{
        x: d.dates, y: d.close, type: "scatter", mode: "lines", name: symbol
      }}], {{
        title: symbol + " Close Price (USD)",
        xaxis: {{ title: "Date" }},
        yaxis: {{ title: "Close Price (USD)" }}
      }}, {{ responsive: true }});
    }}

    const select = document.getElementById("ticker");
    select.addEventListener("change", () => draw(select.value));
    draw(select.value);
  </script>
</body>
</html>
"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Wrote {OUTPUT}")

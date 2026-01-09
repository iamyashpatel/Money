import yfinance as yf
import pandas as pd

symbol = "HCLTECH"
ticker = symbol + ".NS"

df = yf.download(
    ticker,
    period="30d",
    interval="15m",
    progress=False
)

# Keep last 50 rows
df = df.tail(50)

# Flatten columns
df.columns = df.columns.get_level_values(0)

# ===== TIMEZONE SAFE HANDLING =====
if df.index.tz is None:
    # tz-naive → localize first
    df.index = df.index.tz_localize("UTC")

# tz-aware → convert
df.index = df.index.tz_convert("Asia/Kolkata")

# Optional: make Datetime a column
df.reset_index(inplace=True)

# Save
df.to_csv("HCLTECH_LAST_50_15MIN_IST.csv", index=False)

print("Completed")

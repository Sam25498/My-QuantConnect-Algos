import ta
import pandas as pd

# Load data
data = pd.read_csv("stock_data.csv")

# Calculate RSI
rsi = ta.rsi(data["close"])

# Find pivot lows and pivot highs
pivot_lows = ta.pivot_lows(data["close"], lbL, lbR)
pivot_highs = ta.pivot_highs(data["close"], lbL, lbR)

# Find bullish and bearish signals
regular_bull_signals = (rsi > ta.valuewhen(pivot_lows, rsi, 1)) & (ta.barssince(pivot_lows) >= rangeLower) & (ta.barssince(pivot_lows) <= rangeUpper) & (data["low"] < ta.valuewhen(pivot_lows, data["low"], 1))
hidden_bull_signals = (rsi < ta.valuewhen(pivot_lows, rsi, 1)) & (ta.barssince(pivot_lows) >= rangeLower) & (ta.barssince(pivot_lows) <= rangeUpper) & (data["low"] > ta.valuewhen(pivot_lows, data["low"], 1))
regular_bear_signals = (rsi < ta.valuewhen(pivot_highs, rsi, 1)) & (ta.barssince(pivot_highs) >= rangeLower) & (ta.barssince(pivot_highs) <= rangeUpper) & (data["high"] > ta.valuewhen(pivot_highs, data["high"], 1))
hidden_bear_signals = (rsi > ta.valuewhen(pivot_highs, rsi, 1)) & (ta.barssince(pivot_highs) >= rangeLower) & (ta.barssince(pivot_highs) <= rangeUpper) & (data["high"] < ta.valuewhen(pivot_highs, data["high"], 1))


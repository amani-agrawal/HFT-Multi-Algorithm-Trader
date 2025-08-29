
import yfinance as yf
import joblib
import numpy as np
import time
from strategies.market_maker import run_market_maker
from strategies.mean_reversion import run_mean_reversion_strategy
from strategies.news import run_news_trend
from engine.parser import get_top_of_book
from stream.live_orderbook_streamer import get_live_orderbook
from datetime import datetime
# Define stock tickers to monitor
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

# Load trained model
model = joblib.load("strategy_selector_model.pkl")

# Helper: calculate momentum
def compute_momentum(prices, window=5):
    if len(prices) < window + 1:
        return 0
    return (prices[-1] - prices[-window-1]) / prices[-window-1]

# Extract features using yfinance 1-minute data
def get_features(ticker):
    data = yf.download(ticker, period="1d", interval="1m", progress=False)
    if len(data) < 10:
        raise ValueError(f"Not enough data for {ticker}")

    prices = data["Close"].dropna().values
    open_price = data["Open"].iloc[-1]
    current_price = prices[-1]

    volatility = float(np.std(prices[-10:]))
    momentum = float(compute_momentum(prices, window=10))
    orderbook = get_live_orderbook(ticker)
    best_bid, best_ask = get_top_of_book(orderbook)
    spread = best_ask[0] - best_bid[0]

    return {
        "volatility": volatility,
        "spread": spread,
        "momentum": momentum
    }

# Main loop
def run_all(limit=10):
    for _ in range(limit):
        for ticker in TICKERS:
            run_news_trend()
            print(f"\n--- Processing {ticker} ---")
            try:
                market_data = get_features(ticker)
                features = list(market_data.values())
                strategy = model.predict(features)[0]
                print(f"Selected strategy for {ticker}: {strategy}")

                if strategy == "mean_reversion":
                    run_mean_reversion_strategy(ticker=ticker)
                elif strategy == "market_making":
                    run_market_maker(ticker=ticker)
                else:
                    print("No strategy selected.")
            except Exception as e:
                print(f"Error with {ticker}: {e}")
        time.sleep(60)

if __name__ == "__main__":
    run_all()

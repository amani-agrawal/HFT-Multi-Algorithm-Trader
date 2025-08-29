**Features of this Trading Algorithm:**

- Uses a machine learning classifier ( Random Forest ) trained on market features to choose between mean reversion and market making, while also running the news trend strategies.

- Extracts features like volatility, spread, and orderbook imbalance from live Polygon orderbook data to reflect true market microstructure.

- Parses real-time news using NLP models ( FinBERT and BERT-NER ) to extract sentiment scores and detect company mentions for targeted news-based trading.

- Switches to the news trend strategy when sentiment is strong, volatility is high, and volume spikes indicate market-moving events.

- Activates the mean reversion strategy in low-volatility conditions when prices deviate significantly from their short-term moving averages with neutral sentiment.

- Deploys the market making strategy in tight spread and low volatility conditions, dynamically adjusting spreads and skewing quotes based on inventory.

- Incorporates inventory-aware logic to avoid overexposure by adjusting quoting direction when position size exceeds thresholds.

- Avoids adverse market conditions with volatility checks and a cooldown mechanism to pause quoting during unstable periods.

- Tracks realized and unrealized PnL separately across strategies and logs data for post-trade analysis and strategy evaluation.

- Supports simulated execution by matching quotes against the live top-of-book, enabling live evaluation without actual order placement.

import requests
from config_globals import POLYGON_API
from polygon import RESTClient

def parse_polygon_snapshot(snapshot: dict):
    try:
        quote = snapshot['ticker']['lastQuote']
        bid_price = float(quote['p'])  # bid price
        bid_size = int(quote['s'])     # bid size
        ask_price = float(quote['P'])  # ask price
        ask_size = int(quote['S'])     # ask size

        spread = ask_price - bid_price

        return {
            "bids": (bid_price, bid_size),
            "asks": (ask_price, ask_size),
        }
    except Exception as e:
        print(f"Error parsing snapshot: {e}")
        return {
            "bids": None,
            "asks": None
        }

def get_live_orderbook(ticker: str):
    url = f"https://api.polygon.io/v2/last/nbbo/{ticker}?apiKey={POLYGON_API}"
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()

        bid_price = data['results']['bidPrice']
        bid_size = data['results']['bidSize']
        ask_price = data['results']['askPrice']
        ask_size = data['results']['askSize']
        spread = ask_price - bid_price

        return {
            "bid": (bid_price, bid_size),
            "ask": (ask_price, ask_size),
            "spread": spread
        }
    except Exception as e:
        print(f"Error fetching NBBO from Polygon: {e}")
        return {"bid": None, "ask": None, "spread": None}

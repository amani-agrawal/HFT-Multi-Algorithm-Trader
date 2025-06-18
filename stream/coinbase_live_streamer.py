# binance_live_orderbook.py
import requests

def get_live_orderbook(product_id="BTC-USD", level=2):
    """
    Fetches the current order book from Coinbase's REST API.
    :param product_id: Trading pair (e.g. BTC-USD)
    :param level: 1 = best bid/ask, 2 = full order book (aggregated), 3 = full order book (non-aggregated)
    :return: dict with 'bids' and 'asks'
    """
    url = f"https://api.exchange.coinbase.com/products/{product_id}/book?level={level}"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()

        # Convert to floats and keep only price/qty pairs
        bids = [(float(price), float(qty)) for price, qty, _ in data["bids"]]
        asks = [(float(price), float(qty)) for price, qty, _ in data["asks"]]
    

        return {"bids": bids, "asks": asks}

    except requests.RequestException as e:
        print(f"Error fetching live orderbook: {e}")
        return {"bids": [], "asks": []}

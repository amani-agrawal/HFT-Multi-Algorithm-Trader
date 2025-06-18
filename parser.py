import pandas as pd
from datetime import datetime
from pprint import pprint


def load_orderbook_snapshots(csv_path):
    df = pd.read_csv(csv_path)
    snapshots = []

    for _, row in df.iterrows():
        timestamp = datetime.fromisoformat(row['timestamp'])
        bids = [(float(row[f'bid_price_{i}']), float(row[f'bid_qty_{i}'])) for i in range(1, 11)]
        asks = [(float(row[f'ask_price_{i}']), float(row[f'ask_qty_{i}'])) for i in range(1, 11)]
        snapshots.append({"timestamp": timestamp, "bids": bids, "asks": asks})

    return snapshots

def get_top_of_book(orderbook):
    best_bid = orderbook['bids'][0]
    best_ask = orderbook['asks'][0]
    return best_bid, best_ask
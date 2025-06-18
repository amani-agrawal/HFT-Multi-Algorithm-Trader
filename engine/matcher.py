import random
from stream.coinbase_live_streamer import get_live_orderbook

def simulate_limit_order(order_type, price, qty, max_slippage=1.0):
    orderbook = get_live_orderbook()
    filled = 0.0
    remaining = qty
    trades = []

    book_side = orderbook['asks'] if order_type == 'buy' else orderbook['bids']
    print(f"Trying to {order_type} {qty} BTC at ${price} from {book_side[0]}")

    for level_price, level_qty in book_side:
        # Check if your order is eligible to fill at this level
        if (order_type == 'buy' and price >= level_price) or (order_type == 'sell' and price <= level_price):
            # Compute fill probability
            price_distance = abs(price - level_price)
            fill_prob = max(0.1, 1.0 - price_distance / max_slippage)  # linearly decreases with distance

            # Random fill outcome
            if random.random() < fill_prob:
                trade_qty = min(remaining, level_qty)
                # Apply slippage: make price slightly worse
                slippage = random.uniform(0, max_slippage * 0.05)  # up to 5% of max_slippage
                execution_price = level_price + slippage if order_type == 'buy' else level_price - slippage
                execution_price = max(0.0, execution_price)

                trades.append((execution_price, trade_qty))
                print("Traded")
                filled += trade_qty
                remaining -= trade_qty

            if remaining <= 0:
                break
        else:
            break

    return filled, trades

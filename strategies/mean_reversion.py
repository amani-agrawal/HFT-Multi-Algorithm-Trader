from stream.live_orderbook_streamer import get_live_orderbook
from engine.parser import get_top_of_book
from engine.matcher import simulate_limit_order
from risk_controls import stop_trading
from config_globals import WINDOW, THRESHOLD, MAX_INVENTORY, MIN_NOTIONAL, MAX_DRAWDOWN, TICK_SIZE, INVENTORY_SENSITIVITY
from collections import deque
from time import sleep

def run_mean_reversion_strategy(ticker, duration=120, inventory = 0, cash = 0):
    """
    Executes the mean reversion strategy using a rolling SMA and fixed threshold.
    Returns PnL logs.
    """
    price_buffer = deque(maxlen=WINDOW)
    realized_pnl_log = []
    unrealized_pnl_log = []
    total_pnl_log = []

    for _ in range(duration):
        orderbook = get_live_orderbook(ticker)
        best_bid, best_ask = get_top_of_book(orderbook)
        mid = (best_bid[0] + best_ask[0]) / 2
        price_buffer.append(mid)

        if len(price_buffer) < WINDOW:
            sleep(1)
            continue

        sma = sum(price_buffer) / WINDOW
        deviation = mid - sma
        inv_skew = INVENTORY_SENSITIVITY * inventory

        quote = {}
        if deviation > mid*THRESHOLD and inventory > -MAX_INVENTORY:    #price is above avg and there is space in inventory -- sell high
            print("Deviation: ", deviation)
            sell_price = round(mid + TICK_SIZE - inv_skew, 2)
            if sell_price >= MIN_NOTIONAL:
                quote["sell_order"] = {"price": sell_price, "qty": 1}
        elif deviation < -mid*THRESHOLD and inventory < MAX_INVENTORY:  #price is below avg and there is more cash limit to buy -- buy low
            print("Deviation: ", deviation)
            buy_price = round(mid - TICK_SIZE - inv_skew, 2)
            if buy_price >= MIN_NOTIONAL:
                quote["buy_order"] = {"price": buy_price, "qty": 1}

        trades_buy, trades_sell = [], []
        filled_buy, filled_sell = 0, 0

        if "buy_order" in quote:
            order = quote["buy_order"]
            filled_buy, trades_buy = simulate_limit_order(ticker, "buy", order["price"], order["qty"])

        if "sell_order" in quote:
            order = quote["sell_order"]
            filled_sell, trades_sell = simulate_limit_order(ticker, "sell", order["price"], order["qty"])

        # Update inventory and cash
        cash -= sum(price * qty for price, qty in trades_buy)
        inventory += filled_buy
        cash += sum(price * qty for price, qty in trades_sell)
        inventory -= filled_sell

        # PnL tracking
        unrealized = inventory * mid
        realized = cash

        realized_pnl_log.append(realized)
        unrealized_pnl_log.append(unrealized)
        total_pnl_log.append(realized + unrealized)

        if realized + unrealized < MAX_DRAWDOWN:
            stop_trading(f"Total PnL: {realized + unrealized:.2f}")

        sleep(1)
    
    #Getting the final amount -- Selling the entire inventory
    final_ob = get_live_orderbook(ticker)
    best_bid, best_ask = get_top_of_book(final_ob)
    final_mid = (best_bid[0] + best_ask[0]) / 2

    liquidation_value = inventory * final_mid
    cash += liquidation_value
    inventory = 0.0

    final_realized_pnl = cash

    realized_pnl_log.append(final_realized_pnl)
    unrealized_pnl_log.append(0.0)
    total_pnl_log.append(final_realized_pnl)

    return {
        "realized_pnl_log": realized_pnl_log,
        "unrealized_pnl_log": unrealized_pnl_log,
        "total_pnl_log": total_pnl_log
    }

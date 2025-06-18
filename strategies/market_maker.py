from engine.matcher import simulate_limit_order
from engine.parser import get_top_of_book
from collections import deque
import numpy as np
from time import sleep
from risk_controls import stop_trading
from stream.coinbase_live_streamer import get_live_orderbook
import time
from config_globals import (
    MAX_INVENTORY,
    MAX_DRAWDOWN,
    MAX_SPREAD_PCT,
    MAX_VOLATILITY,
    TICK_SIZE,
    MIN_NOTIONAL,
    COOLDOWN_PERIOD
)

def compute_spread(best_ask, best_bid, alpha=0.9):
    return alpha * (best_ask[0] - best_bid[0])

def round_to_tick(price):
    return round(price / TICK_SIZE) * TICK_SIZE

def quote_spread(orderbook, inventory, spread, qty=0.0001, inventory_sensitivity=0.1):
    best_bid, best_ask = get_top_of_book(orderbook)
    mid_price = (best_bid[0] + best_ask[0]) / 2
    inv_skew = inventory_sensitivity * inventory

    buy_price = mid_price - (spread / 2) + inv_skew
    sell_price = mid_price + (spread / 2) + inv_skew

    buy_price = round_to_tick(buy_price)
    sell_price = round_to_tick(sell_price)

    return {
        "buy_order": {"price": buy_price, "qty": qty},
        "sell_order": {"price": sell_price, "qty": qty}
    }

def run_market_maker(limit):
    inventory = 0
    cash = 0
    realized_pnl_log = []
    unrealized_pnl_log = []
    total_pnl_log = []
    mid_history = deque(maxlen=10)
    volatility = 0

    for _ in range(limit):
        ob_now = get_live_orderbook()
        best_bid, best_ask = get_top_of_book(ob_now)
        mid_price_now = (best_bid[0] + best_ask[0]) / 2
        mid_history.append(mid_price_now)

        #Logging
        unrealized = inventory*mid_price_now
        realized = cash

        realized_pnl_log.append(realized)
        unrealized_pnl_log.append(unrealized)
        total_pnl_log.append(realized + unrealized)

        if realized + unrealized < MAX_DRAWDOWN:
            stop_trading(f"Total realized + unrealized: ${realized + unrealized}")


        #Calculating Spread
        spread = compute_spread(best_ask, best_bid)
        spread_pct = (best_ask[0] - best_bid[0]) / best_bid[0]
        if len(mid_history) == 10:
            volatility = np.std(mid_history)
            spread += 2 * volatility
        if volatility > MAX_VOLATILITY or spread_pct > MAX_SPREAD_PCT:
            print("Not trading due to high volatility/spread.")
            sleep(COOLDOWN_PERIOD)
            continue

        #Getting Quote
        quote = quote_spread(ob_now, inventory, spread)

        trades_buy = []
        trades_sell = []
        filled_buy = 0
        filled_sell = 0

        #Excuting quotes
        if inventory < MAX_INVENTORY and quote["buy_order"]["price"] * quote["buy_order"]["qty"] >= MIN_NOTIONAL:
            filled_buy, trades_buy = simulate_limit_order("buy", quote["buy_order"]["price"], quote["buy_order"]["qty"])

        if inventory > -MAX_INVENTORY and quote["sell_order"]["price"] * quote["sell_order"]["qty"] >= MIN_NOTIONAL:
            filled_sell, trades_sell = simulate_limit_order("sell", quote["sell_order"]["price"], quote["sell_order"]["qty"])

        #Updating according to trades made
        cash -= sum(price * qty for price, qty in trades_buy)
        inventory += filled_buy
        cash += sum(price * qty for price, qty in trades_sell)
        inventory -= filled_sell
        time.sleep(1)

    #Getting the final amount
    final_ob = get_live_orderbook()
    best_bid, best_ask = get_top_of_book(final_ob)
    final_mid = (best_bid[0] + best_ask[0]) / 2

    liquidation_value = inventory * final_mid
    cash += liquidation_value
    inventory = 0.0

    final_realized_pnl = cash

    realized_pnl_log.append(final_realized_pnl)
    unrealized_pnl_log.append(final_realized_pnl)
    total_pnl_log.append(final_realized_pnl)

    return {
        "realized_pnl_log": realized_pnl_log,
        "unrealized_pnl_log": unrealized_pnl_log,
        "total_pnl_log": total_pnl_log,
        "final_realized_pnl": final_realized_pnl,
        "final_inventory": inventory
    }

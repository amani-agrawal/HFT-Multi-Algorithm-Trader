from engine.parser import load_orderbook_snapshots
from engine.matcher import simulate_limit_order
from strategies.market_maker import run_market_maker
import matplotlib.pyplot as plt

def plot_pnl(pnls):
    plt.plot(pnls["realized_pnl_log"], label="Realized PnL")
    plt.plot(pnls["unrealized_pnl_log"], label="Unrealized PnL")
    plt.plot(pnls["total_pnl_log"], label="Total PnL")
    plt.title("PnL Over Time")
    plt.xlabel("Snapshot Index")
    plt.ylabel("PnL (USD)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    limit = input("Enter the number of quote orders you want [default is 1,000]: ")
    if not limit:
        limit = 1000
    else:
        limit = int(limit)
    #Example to run the methods
    pnl_log = run_market_maker(limit)
    plot_pnl(pnl_log)
    pnl_log = run_mean_reversion_strategy(limit)
    plot_pnl(pnl_log)

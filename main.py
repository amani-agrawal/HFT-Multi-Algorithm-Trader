from engine.parser import load_orderbook_snapshots
from engine.matcher import simulate_limit_order, simulate_order
from strategies.market_maker import run_market_maker
from strategies.mean_reversion import run_mean_reversion_strategy
import matplotlib.pyplot as plt
from strategies.news import get_sentiment
from stream.finnub_news_streamer import get_general_news, get_specific_news

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
    '''
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
    '''
    news= get_specific_news("AAPL")
    news= get_general_news("general")

    for i in news:
        result = get_sentiment(i)
        if result[0]!="HOLD":
            simulate_order(result[0], result[1])

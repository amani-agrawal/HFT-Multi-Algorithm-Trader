Features of this market maker:
- Dynamic adjustment of spread to 90% of the actual spread if the spread is tight enough
- Inventory skewing logic to not over-stock the inventory
- Use real world market simulation with probability-based simulations and slippage effects
- Check for volatility before quoting to avoid volatile markets and wide spreads with a cooldown period
- Take live data from coinbase data for latest orderbooks 
- Track all the realized and unrealized profit/loss to log and form a graph for analysis
- Stop loss logic for terminating the program on a certain amount of loss
- Live Evaluation Without Execution: Since the model is not deployed to a live trading environment, order fills are simulated by comparing quoted prices against the current Coinbase order book, specifically matching against the highest bid and lowest ask.

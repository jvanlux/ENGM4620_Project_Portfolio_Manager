from portfolio import Portfolio
from trade_logger import export_trades_to_csv

#testing purposes
my_portfolio = Portfolio()
tfsa = my_portfolio.new_account("TFSA")
my_portfolio.buy_equity_for_account(tfsa)
my_portfolio.sell_equity_for_account(tfsa)
my_portfolio.buy_equity_for_account(tfsa)
my_portfolio.sell_equity_for_account(tfsa)

# Export trades for the tfsa account
export_trades_to_csv(tfsa.trades, "my_trades.csv")

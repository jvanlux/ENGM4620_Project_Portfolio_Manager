import csv
import os

def log_trade(action, ticker, price, quantity, date, trades):
    """
    This function creates a dictionary to store the trade data, showing the Action
    as BUY or SELL the stock ticker, the trade price, the quanitity of stocks purchased
    or sold, and the date of the transaction.
    """

    trade = {
        "Action": action,
        "Ticker": ticker,
        "Price": price,
        "Quantity": quantity,
        "Date": date
    }
    trades.append(trade)

    return trades

def export_trades_to_csv(trades, filename="trades.csv"):
    """
    This takes the output of the function log_trade and outputs each of the trades
    to a csv file.
    """
    if not trades:
        print("No trades to export.")
        return

    fieldnames = ["Action", "Ticker", "Price", "Quantity", "Date"]
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        for trade in trades:
            writer.writerow(trade)

    print(f"Trades exported to {filename}.")

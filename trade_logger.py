import csv
import os

def log_trade(action, ticker, price, quantity, date, trades):
    """Log the trade details."""
    trade = {
        "Action": action,
        "Ticker": ticker,
        "Price": price,
        "Quantity": quantity,
        "Date": date
    }
    trades.append(trade)

def export_trades_to_csv(trades, filename="trades.csv"):
    """Export trades to a CSV file."""
    if not trades:
        print("No trades to export.")
        return

    fieldnames = ["Action", "Ticker", "Price", "Quantity", "Date"]
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers only if the file doesn't already exist
        if not file_exists:
            writer.writeheader()

        for trade in trades:
            writer.writerow(trade)

    print(f"Trades exported to {filename}.")

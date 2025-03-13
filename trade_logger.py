import csv
import os

def log_trade(action, ticker, price, quantity, date):

    trade = {
        "Action": action,
        "Ticker": ticker,
        "Price": price,
        "Quantity": quantity,
        "Date": date
    }

    filename= "trades.csv"

    fieldnames = ["Action", "Ticker", "Price", "Quantity", "Date"]

 #   file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(trade)

    print(f"Trade exported to {filename}.")


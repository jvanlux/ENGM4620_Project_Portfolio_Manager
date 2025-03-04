import pandas as pd
import datetime

def read_transactions(csv_file):
    # Read CSV file
    trades = pd.read_csv(csv_file, header=None, names=["Type", "Symbol", "Price", "Shares", "Date"])
    trades["Date"] = pd.to_datetime(trades["Date"])
    trades = trades.sort_values(by="Date")

    # Initialize variables
    balance = 0
    dates = [trades["Date"].min()]
    balances = [balance]

    # Process transactions
    for _, row in trades.iterrows():
        if row["Type"] == "BUY":
            balance += row["Price"] * row["Shares"]  # Buying increases balance
        elif row["Type"] == "SELL":
            balance -= row["Price"] * row["Shares"]  # Selling decreases balance

        dates.append(row["Date"])
        balances.append(balance)

    # Extend to today's date
    today = datetime.datetime.today()
    dates.append(today)
    balances.append(balance)

    return pd.DataFrame({"Date": dates, "Cash Balance": balances})

# Call the function with the CSV file path
csv_file = "my_trades.csv"
read_transactions(csv_file)
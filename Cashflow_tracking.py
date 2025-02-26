import pandas as pd
import datetime

def read_transactions(csv_file):
    # Read CSV file
    df = pd.read_csv(csv_file, header=None, names=["Type", "Symbol", "Price", "Shares", "Date"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")

    # Initialize variables
    balance = 0
    dates = [df["Date"].min()]
    balances = [balance]

    # Process transactions
    for _, row in df.iterrows():
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
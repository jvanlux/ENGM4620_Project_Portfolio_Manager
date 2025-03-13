import csv

def log_trade(action, ticker, price, quantity, date, fname):
    """ This function logs a trade on a csv file."""

    # Dictionary containing BUY/SELL, ticker, action price, quantity, and date
    trade = {
        "Action": action,
        "Ticker": ticker,
        "Price": price,
        "Quantity": quantity,
        "Date": date
    }

    # Generates filename based on account name
    filename = fname + "_trades.csv"

    # Define print order in csv file
    fieldnames = ["Action", "Ticker", "Price", "Quantity", "Date"]

    try:
        # Append trade to csv file
        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(trade)
        print(f"Trade exported to {filename}.")

    except FileNotFoundError:
        print("Error: File not found.")

    except Exception as e:
        print(f"Error: {e}")
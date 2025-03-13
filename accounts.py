import yfinance as yf
from datetime import datetime
from trade_logger import log_trade
import pandas as pd

class Account:
    def __init__(self):
        self.account_name = input("Enter the account name: ")

    def buy_equity(self):
        """Get user input for buying an equity and log trade."""

        # Get purchase ticker
        ticker = input("Enter the stock ticker to buy: ").strip().upper()

        # Get purchase price
        while True:
            try:
                purchase_price = float(input(f"Enter the purchase price for {ticker}: "))
                if purchase_price <= 0:
                    raise ValueError("Price must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e} Please enter a valid purchase price.")

        # Get quantity of shares purchased
        while True:
            try:
                quantity = int(input(f"Enter the quantity of {ticker} to buy: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e} Please enter a valid quantity.")

        # Get purchase date
        purchase_date_input = input(f"Enter the purchase date for {ticker} (YYYY-MM-DD) or press Enter for today: ")
        if not purchase_date_input:
            purchase_date = datetime.today().strftime('%Y-%m-%d')
        else:
            try:
                purchase_date = datetime.strptime(purchase_date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using today's date.")
                # Fallback to today if the format is incorrect
                purchase_date = datetime.today().strftime('%Y-%m-%d')

        log_trade("BUY", ticker, purchase_price, quantity, purchase_date, self.account_name)
        print(f"Bought {quantity} shares of {ticker} at {purchase_price} each.")

    def sell_equity(self):
        """Get user input for selling an equity and execute the sell_equity method."""

        # Get sell ticker
        ticker = input("Enter the stock ticker to sell: ").strip().upper()

        # Get sell price
        while True:
            try:
                sell_price = float(input(f"Enter the sell price for {ticker}: "))
                if sell_price <= 0:
                    raise ValueError("Sell price must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e} Please enter a valid sell price.")

        # Get quantity to sell
        while True:
            try:
                quantity = int(input(f"Enter the quantity of {ticker} to sell: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e} Please enter a valid quantity.")

        # Get sell date
        sell_date_input = input(f"Enter the sell date for {ticker} (YYYY-MM-DD) or press Enter for today: ")
        if not sell_date_input:
            sell_date = datetime.today().strftime('%Y-%m-%d')
        else:
            try:
                sell_date = datetime.strptime(sell_date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using today's date.")
                # Fallback to today if the format is incorrect
                sell_date = datetime.today().strftime('%Y-%m-%d')

        log_trade("SELL", ticker, sell_price, quantity, sell_date, self.account_name)
        print(f"Sold {quantity} shares of {ticker} at {sell_price} each on {sell_date}")


    def get_current_price(self, symbol):
        """Fetch real-time stock prices from yfinance."""
        try:
            stock = yf.Ticker(symbol)
            return stock.history(period="1d")["Close"].iloc[-1]  # Get last closing price
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return 0  # Default to 0 if fetch fails

    def load_trades(self):
        """Load trades from CSV and return a DataFrame."""
        filename = self.account_name + "_trades.csv"
        try:
            df = pd.read_csv(filename, header=None, names=["Action", "Symbol", "Price", "Shares", "Date"])
            print("File loaded successfully.")
            return df
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

    def holdings(self):
        """Generate a summary of holdings with total value and unrealized profit/loss."""
        df = self.load_trades()
        if df.empty:
            return pd.DataFrame()  # Return empty DataFrame if no trades were loaded

        holdings = {}  # Temporary dictionary to track holdings during processing

        for _, row in df.iterrows():
            symbol = row["Symbol"]
            action = row["Action"]
            price = row["Price"]
            shares = row["Shares"]

            if symbol not in holdings:
                holdings[symbol] = {"total_shares": 0, "total_cost": 0}

            if action == "BUY":
                holdings[symbol]["total_shares"] += shares
                holdings[symbol]["total_cost"] += shares * price
            elif action == "SELL" and holdings[symbol]["total_shares"] > 0:
                avg_price = holdings[symbol]["total_cost"] / holdings[symbol]["total_shares"]
                holdings[symbol]["total_shares"] -= shares
                holdings[symbol]["total_cost"] -= avg_price * shares

        # Generate summary
        summary = []
        for symbol, data in holdings.items():
            total_shares = data["total_shares"]

            if total_shares > 0:
                avg_purchase_price = round(data["total_cost"] / total_shares, 2)
                current_price = round(self.get_current_price(symbol), 2)
                total_value = round(total_shares * current_price, 2)
                unrealized_pnl = round(total_value - data["total_cost"], 2)

                summary.append([symbol, total_shares, current_price, total_value, avg_purchase_price, unrealized_pnl])

        # Convert to DataFrame
        summary_df = pd.DataFrame(summary,
                                  columns=["Symbol", "Total Shares", "Current Price", "Total Value", "Avg Purchase Price",
                                           "Unrealized P/L"])

        # Add a row for the totals
        total_value_sum = round(summary_df["Total Value"].sum(), 2)
        unrealized_pnl_sum = round(summary_df["Unrealized P/L"].sum(), 2)

        summary_df.loc[len(summary_df)] = ["Summary", "-", "-", total_value_sum, "-", unrealized_pnl_sum]

        # Set pandas to display all columns
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        # Set the Symbol column as the index
        summary_df.set_index("Symbol", inplace=True)

        # Remove the name of the index ("Symbol")
        summary_df.rename_axis(None, inplace=True)

        return summary_df

    def print_all_holdings(self):
        print(self.holdings())

    def print_account_summary(self):
        df = self.holdings()
        print(pd.concat([df.head(0), df.tail(1)]))

    def print_specific_holding(self):
        df = self.holdings()
        symbol = input("Enter ticker to view data for: ").strip().upper()  # Ensure proper formatting
        try:
            print(df.loc[[symbol]].to_string())  # Double brackets keep it as a DataFrame (not Series)
        except KeyError:
            print(f"Error: {symbol} not found in holdings.")




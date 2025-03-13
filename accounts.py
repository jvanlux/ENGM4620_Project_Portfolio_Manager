import yfinance as yf
from datetime import datetime
from trade_logger import log_trade
import pandas as pd

# Base class for all account types
class Account:
    def __init__(self):
        pass

    def buy_equity(self):
        """Get user input for buying an equity and execute the buy_equity method."""
        ticker = input("Enter the stock ticker to buy: ")

        # Handle purchase price with error handling
        while True:
            try:
                purchase_price = float(input(f"Enter the purchase price for {ticker}: "))
                if purchase_price <= 0:
                    raise ValueError("Price must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid purchase price.")

        # Handle quantity with error handling
        while True:
            try:
                quantity = int(input(f"Enter the quantity of {ticker} to buy: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid quantity.")

        # Handle purchase date with default to today's date if empty
        purchase_date_input = input(f"Enter the purchase date for {ticker} (YYYY-MM-DD) or press Enter for today: ")

        if not purchase_date_input:
            purchase_date = datetime.today().strftime('%Y-%m-%d')  # Use today's date
        else:
            try:
                purchase_date = datetime.strptime(purchase_date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using today's date.")
                # Fallback to today if the format is incorrect
                purchase_date = datetime.today().strftime('%Y-%m-%d')

        log_trade("BUY", ticker, purchase_price, quantity, purchase_date)
        print(f"Bought {quantity} shares of {ticker} at {purchase_price} each.")

    def sell_equity(self):
        """Get user input for selling an equity and execute the sell_equity method."""
        ticker = input("Enter the stock ticker to sell: ")

        # Handle quantity with error handling
        while True:
            try:
                quantity = int(input(f"Enter the quantity of {ticker} to sell: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid quantity.")

        # Handle sell price with error handling
        while True:
            try:
                sell_price = float(input(f"Enter the sell price for {ticker}: "))
                if sell_price <= 0:
                    raise ValueError("Sell price must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid sell price.")

        # Handle sell date with default to today's date if empty
        sell_date_input = input(f"Enter the sell date for {ticker} (YYYY-MM-DD) or press Enter for today: ")
        if not sell_date_input:
            sell_date = datetime.today().strftime('%Y-%m-%d')  # Use today's date
        else:
            try:
                sell_date = datetime.strptime(sell_date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using today's date.")
                # Fallback to today if the format is incorrect
                sell_date = datetime.today().strftime('%Y-%m-%d')

        log_trade("SELL", ticker, sell_price, quantity, sell_date)
        print(f"Sold {quantity} shares of {ticker} at {sell_price} each on {sell_date}")

    def get_value(self, filename):
        # Load trades from CSV
        df = pd.read_csv(filename, header=None, names=["Action", "Symbol", "Price", "Shares", "Date"])

        # Calculate holdings
        holdings = {}
        for _, row in df.iterrows():
            symbol = row["Symbol"]
            shares = row["Shares"]
            action = row["Action"]

            if symbol not in holdings:
                holdings[symbol] = 0

            if action == "BUY":
                holdings[symbol] += shares
            elif action == "SELL":
                holdings[symbol] -= shares

        # Fetch current stock prices using yfinance
        current_prices = {}
        for symbol in holdings.keys():
            stock = yf.Ticker(symbol)
            current_prices[symbol] = stock.history(period="1d")["Close"].iloc[-1]

        # Calculate portfolio value
        portfolio_values = {symbol: shares * current_prices.get(symbol, 0) for symbol, shares in holdings.items()}
        total_portfolio_value = sum(portfolio_values.values())

        print("Portfolio value:", total_portfolio_value)

    def print_holdings(self, filename):
        # Load trades from CSV
        df = pd.read_csv(filename, header=None, names=["Action", "Symbol", "Price", "Shares", "Date"])

        # Calculate holdings
        holdings = {}
        for _, row in df.iterrows():
            symbol = row["Symbol"]
            shares = row["Shares"]
            action = row["Action"]

            if symbol not in holdings:
                holdings[symbol] = 0

            if action == "BUY":
                holdings[symbol] += shares
            elif action == "SELL":
                holdings[symbol] -= shares

        # Fetch current stock prices using yfinance
        current_prices = {}
        for symbol in holdings.keys():
            stock = yf.Ticker(symbol)
            current_prices[symbol] = stock.history(period="1d")["Close"].iloc[-1]

        # Calculate portfolio value
        portfolio_values = {symbol: shares * current_prices.get(symbol, 0) for symbol, shares in holdings.items()}

        # print a dataframe that shows ticker, shares, current price, and total value of stock



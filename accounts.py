from datetime import datetime
from trade_logger import log_trade
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import yfinance as yf

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


    def plot_holdings_pie_chart(self):
        """stuff here"""
        df = self.holdings().drop(index="Summary", errors="ignore")

        if df.empty:
            print("No holdings to display.")
            return

        labels = df.index
        sizes = df["Total Value"].astype(float)
        total_value = sizes.sum()

        # Prepare labels to include total value
        labels = [f"{label} (${value:,.2f})" for label, value in zip(labels, sizes)]

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.1f%%", startangle=140, pctdistance=0.85,
            colors=plt.cm.Paired.colors, wedgeprops={"edgecolor": "black"}
        )

        ax.set_title(f"Portfolio Distribution\nTotal Value: ${total_value:,.2f}")
        ax.axis("equal")
        plt.show()

    def net_investment(self):
        """
        This function reads in the csv file with all trades to date, and
        calculates the amount of money invested at every date a new transaction occurs.
        """

        # Use  account object to get CSV file name
        csv_file = f"{self.account_name}_trades.csv"
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

        print(pd.DataFrame({"Date": dates, "Net Investment": balances}))

        return pd.DataFrame({"Date": dates, "Net Investment": balances})

    def portfolio_value(self):

        # Use  account object to get CSV file name
        csv_file = f"{self.account_name}_trades.csv"

        # Read the transactions from the CSV file
        trades = pd.read_csv(csv_file, header=None, names=["Type", "Symbol", "Price", "Shares", "Date"])

        # make sure the dates are in proper datetime format
        trades['Date'] = pd.to_datetime(trades['Date'])

        # Find the unique symbols
        unique_symbols = trades['Symbol'].unique()

        all_stock_data = {}

        # Find the first BUY transaction date in the entire dataset
        first_buy_date = trades[trades["Type"] == "BUY"]["Date"].min()
        start_date = first_buy_date
        end_date = pd.to_datetime("today")

        # Download stock price data for each stock for each date since first purchase
        for symbol in unique_symbols:
            stock_df = trades[trades['Symbol'] == symbol]
            first_buy_date = stock_df[stock_df["Type"] == "BUY"]["Date"].min()

            stock_data = yf.download(symbol, start=first_buy_date, end=end_date)
            all_stock_data[symbol] = stock_data['Close']

        # Create a list of all dates in date range
        all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # Dictionary to store portfolio values per date
        portfolio_data = {}

        # Process each stock separately and track its portfolio value
        # Process each stock separately and track its portfolio value
        for symbol in unique_symbols:
            stock_df = trades[trades['Symbol'] == symbol]  # Filter trades for current stock
            close_data = all_stock_data[symbol]
            shares_owned = 0

            # Sort the transactions by date so we handle them in chronological order
            stock_df = stock_df.sort_values(by="Date")

            last_known_value = 0
            for date in all_dates:
                # If stock market data for the current date is available, use it
                if date in close_data.index:
                    close_price = close_data.loc[date].item()
                else:
                    # If no data for that date ie. weekend, holiday
                    close_price = last_known_value

                # If there was a trade on this date, update shares_owned
                stock_on_date = stock_df[stock_df['Date'] == date]
                for _, row in stock_on_date.iterrows():
                    if row["Type"] == "BUY":
                        shares_owned += row["Shares"]
                    elif row["Type"] == "SELL":
                        shares_owned -= row["Shares"]

                # Store the portfolio value per stock per date
                portfolio_value = shares_owned * close_price

                if date not in portfolio_data:
                    portfolio_data[date] = {}
                portfolio_data[date][symbol] = portfolio_value

                # Update last_known_value for future dates
                last_known_value = close_price if shares_owned > 0 else 0

        # Convert the portfolio dictionary into a DataFrame
        portfolio_df = pd.DataFrame.from_dict(portfolio_data, orient='index').fillna(0)

        # Add a column for total portfolio value
        portfolio_df["Total Portfolio Value"] = portfolio_df.sum(axis=1)

        # Reset index and rename columns
        portfolio_df.reset_index(inplace=True)
        portfolio_df.rename(columns={'index': 'Date'}, inplace=True)

        # Ensure Date column is in datetime format
        portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

        # Sort by Date in ascending order
        portfolio_df = portfolio_df.sort_values(by="Date", ascending=True)

        # Reset the index after sorting
        portfolio_df.reset_index(drop=True, inplace=True)

        print("This is portfolio_df")
        print(portfolio_df)

        return portfolio_df[["Date", "Total Portfolio Value"]]

    def plot_combined(self):
        """ Plots both net investement and total portfolio value on the same graph. """
        net_investment_df = self.net_investment()
        portfolio_value_df = self.portfolio_value()

        # Merge both DataFrames on Date, .ffill is forward fill of stuff with no data
        merged_df = pd.merge(net_investment_df, portfolio_value_df, on="Date", how="outer").ffill()
        print(merged_df)

        plt.figure(figsize=(12, 6))

        # Plot net investement
        plt.plot(merged_df["Date"], merged_df["Net Investment"], label="Net Investment", linestyle="--", color="black")

        # Plot total portfolio value
        plt.plot(merged_df["Date"], merged_df["Total Portfolio Value"], label="Total Portfolio Value", linestyle="-",
                 color="blue")

        # Formatting
        plt.xlabel("Date")
        plt.ylabel("Value ($)")
        plt.title("Net Investment vs. Total Portfolio Value Over Time")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()

        plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf


def read_and_plot_transactions(csv_file):
    # Read CSV file
    df = pd.read_csv(csv_file, header=None, names=["Type", "Symbol", "Price", "Shares", "Date"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")

    # Initialize variables
    portfolio = {}  # Store shares of each stock
    dates = [df["Date"].min()]
    portfolio_values = [0]  # Portfolio value at the beginning

    # Process transactions and create portfolio value tracking
    for _, row in df.iterrows():
        stock_value = 0
        if row["Type"] == "BUY":
            if row["Symbol"] in portfolio:
                portfolio[row["Symbol"]] += row["Shares"]  # Add shares to the existing stock
            else:
                portfolio[row["Symbol"]] = row["Shares"]  # Buy new stock
        elif row["Type"] == "SELL":
            if row["Symbol"] in portfolio and portfolio[row["Symbol"]] >= row["Shares"]:
                portfolio[row["Symbol"]] -= row["Shares"]  # Sell shares of the stock
            else:
                print(f"Error: Not enough shares to sell for {row['Symbol']}.")

        # Calculate portfolio value by summing the value of all stocks owned
        for symbol, shares in portfolio.items():
            stock_value += shares * row["Price"]  # Add stock value at the current price

        dates.append(row["Date"])
        portfolio_values.append(stock_value)

    # Extend to today's date with the last available price
    today = datetime.datetime.today()
    dates.append(today)
    portfolio_values.append(stock_value)

    # Get the list of symbols for historical data
    symbols = list(set(df["Symbol"]))  # Extract unique stock symbols
    stock_data = {}

    # Fetch stock data for each symbol
    for symbol in symbols:
        data = yf.download(symbol, start=df["Date"].min(), end=today, progress=False)
        print(f"Data for {symbol}: {data.columns}")  # Print the columns to debug

        # Check if 'Adj Close' is present, otherwise use 'Close'
        if 'Adj Close' in data.columns:
            stock_data[symbol] = data['Adj Close']
        elif 'Close' in data.columns:
            stock_data[symbol] = data['Close']
        else:
            print(f"Error: No suitable price column found for {symbol}")

    # Plot the portfolio value over time
    plt.figure(figsize=(12, 6))
    plt.plot(dates, portfolio_values, drawstyle='steps-post', linestyle='-', color='green', marker='o',
             label="Portfolio Value")

    # Track purchase dates for each stock to only plot after the first purchase
    for symbol in ["AAPL", "MSFT"]:
        if symbol in stock_data:
            stock_resampled = stock_data[symbol].resample('D').ffill()  # Forward fill to match daily data

            # Find the first purchase date for the stock
            purchase_date = df[df["Symbol"] == symbol].iloc[0]["Date"]
            # Filter the stock data to only plot after the first purchase date
            stock_resampled_after_purchase = stock_resampled[stock_resampled.index >= purchase_date]

            # Multiply the stock price by the number of shares you own at each date
            adjusted_value = stock_resampled_after_purchase * portfolio.get(symbol, 0)
            plt.plot(stock_resampled_after_purchase.index, adjusted_value, label=f"{symbol} Adjusted Value")

    plt.xlabel("Date")
    plt.ylabel("Value ($)")
    plt.title("Portfolio Value and Stock Prices Over Time (Adjusted for Shares)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()


# Call the function with the CSV file path
csv_file = "my_trades.csv"  # Update with the actual path
read_and_plot_transactions(csv_file)

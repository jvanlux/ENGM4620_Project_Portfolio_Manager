import pandas as pd
import yfinance as yf
import datetime


def calculate_portfolio_value(csv_file):
    # Read CSV file
    df = pd.read_csv(csv_file, header=None, names=["Type", "Symbol", "Price", "Shares", "Date"])
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort the transactions by date
    df = df.sort_values(by="Date")

    # Initialize variables
    portfolio_values = []
    current_holdings = {}

    # Get unique stock symbols from the transactions
    stock_symbols = df["Symbol"].unique()

    # Fetch stock data (historical close prices) for each symbol
    stock_data = {}
    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        historical_data = stock.history(period="1d", start=df["Date"].min(), end=pd.Timestamp.today())
        stock_data[symbol] = historical_data["Close"]

    # Track the amount of stock owned on each date
    for _, row in df.iterrows():
        symbol = row["Symbol"]
        shares = row["Shares"]

        # Update the number of shares owned for each stock
        if symbol not in current_holdings:
            current_holdings[symbol] = 0
        if row["Type"] == "BUY":
            current_holdings[symbol] += shares
        elif row["Type"] == "SELL":
            current_holdings[symbol] -= shares

    # Get all dates from the first transaction to today's date
    dates = pd.date_range(start=df["Date"].min(), end=pd.Timestamp.today())

    # Calculate portfolio value for each date
    for date in dates:
        portfolio_value = 0
        for symbol, shares in current_holdings.items():
            if shares > 0 and symbol in stock_data:
                # Check if the date exists in the stock data index
                closest_date = stock_data[symbol].index.get_loc(date,
                                                                method='ffill')  # 'ffill' gets the closest previous date
                close_price = stock_data[symbol].iloc[closest_date]
                portfolio_value += shares * close_price

        # Store the portfolio value and date
        portfolio_values.append({"Date": date, "Portfolio Value": portfolio_value})

    # Convert the portfolio values to a DataFrame for easy manipulation and visualization
    portfolio_df = pd.DataFrame(portfolio_values)

    return portfolio_df


# File path to your CSV file
csv_file = "my_trades.csv"

# Calculate the portfolio values over time
portfolio_df = calculate_portfolio_value(csv_file)

# Print the portfolio values DataFrame
print(portfolio_df)

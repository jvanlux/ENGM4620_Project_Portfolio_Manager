import yfinance as yf
import pandas as pd

def portfolio_value(csv_file):
    trades = pd.read_csv(csv_file, header=None, names=["Type", "Symbol", "Price", "Shares", "Date"])
    # Read the transactions from the CSV file

    trades['Date'] = pd.to_datetime(trades['Date'])

    unique_symbols = trades['Symbol'].unique()

    all_stock_data = {}

    # Find the first "BUY" transaction date in the entire dataset
    first_buy_date = trades[trades["Type"] == "BUY"]["Date"].min()
    start_date = first_buy_date
    end_date = pd.to_datetime("today")

    # Download stock price data for each stock
    for symbol in unique_symbols:
        stock_df = trades[trades['Symbol'] == symbol]  # Filter transactions for this stock
        first_buy_date = stock_df[stock_df["Type"] == "BUY"]["Date"].min()

        stock_data = yf.download(symbol, start=first_buy_date, end=end_date)
        all_stock_data[symbol] = stock_data['Close']  # Store only Close prices

    # Create a complete date range
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

    # Dictionary to store portfolio values per date
    portfolio_data = {}

    # Process each stock separately and track its portfolio value
    for symbol in unique_symbols:
        stock_df = trades[trades['Symbol'] == symbol]  # Filter transactions for this stock
        close_data = all_stock_data[symbol]  # Get stored close prices
        shares_owned = 0

        for date in all_dates:
            # If stock market data is available for the date, use it
            if date in close_data.index:
                close_price = close_data.loc[date].item()
            else:
                continue  # Skip this day if no market data available

            # Update the number of shares owned
            for _, row in stock_df[stock_df['Date'] == date].iterrows():
                if row["Type"] == "BUY":
                    shares_owned += row["Shares"]
                elif row["Type"] == "SELL":
                    shares_owned -= row["Shares"]

            # Calculate portfolio value for this stock
            portfolio_value = shares_owned * close_price

            # Store the portfolio value per stock per date
            if date not in portfolio_data:
                portfolio_data[date] = {}
            portfolio_data[date][symbol] = portfolio_value

    # Convert the portfolio dictionary into a DataFrame
    portfolio_df = pd.DataFrame.from_dict(portfolio_data, orient='index').fillna(0)

    # Add a column for total portfolio value
    portfolio_df["Total Portfolio Value"] = portfolio_df.sum(axis=1)

    # Reset index and rename columns
    portfolio_df.reset_index(inplace=True)
    portfolio_df.rename(columns={'index': 'Date'}, inplace=True)

    # Display the final DataFrame
    print(portfolio_df)

    # Ensure Date column is in datetime format
    portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

    # Sort by Date in ascending order
    portfolio_df = portfolio_df.sort_values(by="Date", ascending=True)

    # Reset the index after sorting
    portfolio_df.reset_index(drop=True, inplace=True)

    print(portfolio_df)

    return portfolio_df[["Date", "Total Portfolio Value"]]

csv_file = "my_trades.csv"
portfolio_value(csv_file)
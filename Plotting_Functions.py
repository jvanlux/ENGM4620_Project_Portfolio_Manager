import matplotlib.pyplot as plt
import pandas as pd
import datetime
import yfinance as yf

def plot_holdings_pie_chart(account):
    """"""
    df = account.holdings().drop(index="Summary", errors="ignore")

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

def net_investment(account):
    """
    This function reads in the csv file with all trades to date, and
    calculates the amount of money invested at every date a new transaction occurs.
    """

    # Use  account object to get CSV file name
    csv_file = f"{account.account_name}_trades.csv"
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

    print(pd.DataFrame({"Date": dates, "Cash Balance": balances}))

    return pd.DataFrame({"Date": dates, "Cash Balance": balances})


def portfolio_value(account):

    # Use  account object to get CSV file name
    csv_file = f"{account.account_name}_trades.csv"

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
    for symbol in unique_symbols:
        close_data = all_stock_data[symbol]
        shares_owned = 0

        for date in all_dates:
            if date in close_data.index:
                close_price = close_data.loc[date].item()
            else:
                # Skip day if no market data available ie. weekend/holiday
                continue

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

    # Ensure Date column is in datetime format
    portfolio_df["Date"] = pd.to_datetime(portfolio_df["Date"])

    # Sort by Date in ascending order
    portfolio_df = portfolio_df.sort_values(by="Date", ascending=True)

    # Reset the index after sorting
    portfolio_df.reset_index(drop=True, inplace=True)

    print("This is portfolio_df")
    print(portfolio_df)

    return portfolio_df[["Date", "Total Portfolio Value"]]


def plot_combined(account):
    """ Plots both net investement and total portfolio value on the same graph. """
    net_investment_df = net_investment(account)
    portfolio_value_df = portfolio_value(account)

    # Merge both DataFrames on Date, .ffill is forward fill of stuff with no data
    merged_df = pd.merge(net_investment_df, portfolio_value_df, on="Date", how="outer").ffill()
    print(merged_df)

    plt.figure(figsize=(12, 6))

    # Plot net investement
    plt.plot(merged_df["Date"], merged_df["Cash Balance"], label="Cash Balance", linestyle="-", color="blue")

    # Plot total portfolio value
    plt.plot(merged_df["Date"], merged_df["Total Portfolio Value"], label="Total Portfolio Value", linestyle="--", color="black")

    # Formatting
    plt.xlabel("Date")
    plt.ylabel("Value ($)")
    plt.title("Cash Input vs. Total Portfolio Value Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()

    plt.show()
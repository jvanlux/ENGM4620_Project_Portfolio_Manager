import yfinance as yf
import pandas as pd

# Read the transactions from the CSV file
df = pd.read_csv('my_trades.csv', header=None, names=["Type", "Symbol", "Price", "Shares", "Date"])

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Define the stock symbol (you can also read the symbol from the CSV if you prefer)
symbol = df['Symbol'].iloc[0]  # Assuming all transactions are for the same symbol

# Find the first "BUY" transaction date to set as the start date
first_buy_date = df[df["Type"] == "BUY"]["Date"].min()
start_date = first_buy_date
end_date = pd.to_datetime("today")  # You can change this to today's date or a custom end date

# Fetch historical stock data from the first "BUY" date to the end date
stock_data = yf.download(symbol, start=start_date, end=end_date)
print(stock_data)


# Select only the 'Close' price
close_data = stock_data['Close']

# Display the close prices (optional)
print(close_data)

# Save the close prices to a CSV file
close_data.to_csv(f"{symbol}_close_prices.csv")

# Create a list of all dates from the start date to the end date
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Initialize variables to track the number of shares owned
shares_owned = 0
shares_over_time = []

# Process each day and track the shares owned on each day
for date in all_dates:
    # Check if the close price exists for the current date
    if date in close_data.index:
        close_price = close_data.loc[date].item()
        print(close_price)
    else:
        # If no close price for the day, skip this date
        continue

    # Check if there's a transaction on this day and update shares
    for _, row in df[df['Date'] == date].iterrows():
        if row["Type"] == "BUY":
            shares_owned += row["Shares"]
        elif row["Type"] == "SELL":
            shares_owned -= row["Shares"]

    # Calculate the value of the shares owned at this date
    portfolio_value = shares_owned * close_price

    # Add the date, shares owned, and portfolio value to the list
    shares_over_time.append({"Date": date, "Shares Owned": shares_owned, "Portfolio Value": portfolio_value})

# Convert the list of shares owned and portfolio value over time to a DataFrame
shares_df = pd.DataFrame(shares_over_time)

# Display the shares owned and portfolio value over time (optional)
print(shares_df)


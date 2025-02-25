import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_and_plot_stock(ticker):
    # Define time ranges
    end_date = datetime.today()
    start_dates = {
        '3 Months': end_date.replace(month=end_date.month-3) if end_date.month > 3 else end_date.replace(year=end_date.year-1, month=end_date.month+9),
        '6 Months': end_date.replace(month=end_date.month-6) if end_date.month > 6 else end_date.replace(year=end_date.year-1, month=end_date.month+6),
        '1 Year': end_date.replace(year=end_date.year-1),
        '5 Years': end_date.replace(year=end_date.year-5),
    }

    # Create subplots (2 rows and 2 columns)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()  # Flatten the 2D array of axes for easy access

    for i, (label, start_date) in enumerate(start_dates.items()):
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        if stock_data.empty:
            print(f"No data found for {label}.")
            continue

        ax = axes[i]
        ax.plot(stock_data.index, stock_data['Close'], label=label)
        ax.set_xlabel("Date")
        ax.set_ylabel("Stock Price (Close)")
        ax.set_title(f"{ticker} - {label} Performance")
        ax.grid()
        ax.legend()

    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()

# Prompt user for stock ticker
ticker = input("Enter the stock ticker: ")
fetch_and_plot_stock(ticker)

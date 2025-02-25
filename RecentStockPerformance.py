import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime


def fetch_and_plot_stock(ticker, start_date=None, end_date=None):
    # If user did not provide custom dates, use predefined ranges
    if not start_date or not end_date:
        # Define time ranges
        end_date = datetime.today()
        start_dates = {
            '3 Months': end_date.replace(month=end_date.month - 3) if end_date.month > 3 else end_date.replace(
                year=end_date.year - 1, month=end_date.month + 9),
            '6 Months': end_date.replace(month=end_date.month - 6) if end_date.month > 6 else end_date.replace(
                year=end_date.year - 1, month=end_date.month + 6),
            '1 Year': end_date.replace(year=end_date.year - 1),
            '5 Years': end_date.replace(year=end_date.year - 5),
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

    # If user provided custom dates, use those for plotting
    else:
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        if stock_data.empty:
            print(f"No data found for the specified date range.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(stock_data.index, stock_data['Close'], label=f"{ticker} Price")
        plt.xlabel("Date")
        plt.ylabel("Stock Price (Close)")
        plt.title(f"{ticker} - Custom Date Range Performance")
        plt.grid()
        plt.legend()
        plt.show()


def get_date_input(prompt):
    while True:
        try:
            date_input = input(prompt)
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


# Prompt user for stock ticker
ticker = input("Enter the stock ticker: ")

# Ask user if they want to use a default range or custom range
date_option = input(
    "Choose date range:\n1. Default (3 months, 6 months, 1 year, 5 years)\n2. Custom range\nEnter option number: ").strip()

if date_option == '2':
    start_date = get_date_input("Enter the start date (YYYY-MM-DD): ")
    end_date = get_date_input("Enter the end date (YYYY-MM-DD): ")
    fetch_and_plot_stock(ticker, start_date, end_date)
else:
    fetch_and_plot_stock(ticker)
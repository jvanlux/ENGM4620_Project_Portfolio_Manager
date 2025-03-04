import pandas as pd
import matplotlib.pyplot as plt

from Cashflow_tracking import read_transactions
from Portfolio_value import portfolio_value


def plot_combined(csv_file):
    """ Plots both cash balance and total portfolio value on the same graph. """
    cash_df = read_transactions(csv_file)
    portfolio_df = portfolio_value(csv_file)

    # Merge both DataFrames on Date
    merged_df = pd.merge(cash_df, portfolio_df, on="Date", how="outer").fillna(method="ffill")

    plt.figure(figsize=(12, 6))

    # Plot Cash Balance
    plt.plot(merged_df["Date"], merged_df["Cash Balance"], label="Cash Balance", linestyle="-", color="blue")

    # Plot Total Portfolio Value
    plt.plot(merged_df["Date"], merged_df["Total Portfolio Value"], label="Total Portfolio Value", linestyle="--", color="black")

    # Formatting
    plt.xlabel("Date")
    plt.ylabel("Value ($)")
    plt.title("Cash Input vs. Total Portfolio Value Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()

    # Show the plot
    plt.show()

# Run the function
csv_file = "my_trades.csv"
plot_combined(csv_file)
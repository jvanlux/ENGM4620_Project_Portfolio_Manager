import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def portfolio_Distribution(filename):
    """Reads a CSV file of transactions, calculates holdings, fetches live prices,
    and plots a pie chart of the portfolio."""

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

    # Create labels with shares and value information
    labels = [f"{symbol}\n{holdings[symbol]} shares\n${value:.2f}" for symbol, value in portfolio_values.items()]

    # Plot pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(portfolio_values.values(), labels=labels, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'orange'])
    plt.title(f"Portfolio Distribution (Total: ${total_portfolio_value:.2f})")
    plt.show()

    # Print portfolio details
    print("Updated Holdings:")
    for symbol, value in portfolio_values.items():
        print(f"{symbol}: ${value:.2f} ({holdings[symbol]} shares)")
    print(f"Total Portfolio Value: ${total_portfolio_value:.2f}")



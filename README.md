# Portfolio Management Tool

### James McIntosh & John VanLuxemborg

## Overview

The Portfolio Management Tool is designed to help users track their stock trades, manage a portfolio, and visualize performance over time. It provides functionality for buying, selling, and tracking equities, generating portfolio summaries, displaying holdings, and visualizing account performance. It also includes a variety of analysis tools such as plotting portfolio value trends and creating pie charts for holdings distribution.

## Features

1. **Create or Load an Account**  
   Allows you to create a new account or load an existing account that has been saved locally by providing the account name.

2. **Buy or Sell Equities**  
   Lets you execute buy or sell transactions for stocks, by entering relevant details such as ticker, price, quantity, and date.

3. **Bulk Import Equities**  
   Facilitates importing a large number of stock transactions into the portfolio at an average purchase price if the user is not interested in past portfolio trends.

4. **Pie Chart Holdings**  
   Visualizes the distribution of your holdings in a pie chart.

5. **Account Balance Trend Plot**  
   Displays a line graph comparing net investment and total portfolio value over time.

6. **Display Account Holdings**  
   Allows you to view all your stock holdings in your portfolio, look at specific stocks, or look at a summary of all holdings.

7. **Track Performance Over Time**  
   The program calculates unrealized profits and losses (P/L) and allows you to track how your portfolio value evolves.

## Requirements
```
﻿matplotlib~=3.10.0
pandas~=2.2.3
yfinance~=0.2.54
colorama~=0.4.6
```

## How to Use

### 1. Running the Program
To run the program, simply execute the Python script:

```
python main.py
```

The program will guide you through the options available.

### 2. Creating or Loading an Account
- Upon running the program, you will be prompted to enter an account name. If the account exists, it will be loaded; if it doesn't, a new account will be created.

### 3. Buying or Selling Equities
- You can buy or sell stocks using the options available in the main menu. You'll be asked for the stock ticker, price, quantity, and date.
- The transaction will be logged in a CSV file, where all trades will be saved.

### 4. Bulk Import
- This option allows you to import stock purchases in bulk, specifying ticker, average purchase price, and quantity.

### 5. Plotting Portfolio Information
- **Holdings Pie Chart**: Displays a pie chart showing the distribution of your portfolio across different stocks.
- **Account Balance Trend**: Shows a plot comparing the trend of net investments and total portfolio value over time.

### 6. Display Holdings
You can display:
- **All Holdings**: Displays a table with all your stocks, quantities, current prices, total value, average purchase price, and unrealized P/L.
- **Summary**: Shows only a summarized row of your total portfolio.
- **Specific Holding**: Lets you search for a specific stock and see its performance.

## Example of User Interaction

```
python main.py

Please enter your selection: 1
Enter your account name: MyPortfolio

Please enter your selection: 2
Do you want to "Buy", "Sell", or "Exit"? BUY
Enter the stock ticker to buy: AAPL
Enter the purchase price for AAPL: 150.50
Enter the quantity of AAPL to buy: 10
Enter the purchase date for AAPL (YYYY-MM-DD) or press Enter for today: 2025-03-19
Bought 10 shares of AAPL at 150.50 each.

Please enter your selection: 4
Displaying portfolio holdings in a pie chart...
```

## Troubleshooting

- **Issue**: "The file 'account_name_trades.csv' was not found."  
  **Solution**: Ensure you have logged a transaction first (buy or sell) before attempting to load trades.


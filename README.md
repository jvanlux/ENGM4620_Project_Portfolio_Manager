# ENGM4620 Project: Portfolio Manager

## Authors
James McIntosh & John VanLuxemborg

## Python Version
This project uses **Python 3.13**.

## Required Packages
Ensure you have the following packages installed before running the project:
```python
import csv
import os
import yfinance as yf
import pandas as pd
import datetime
import matplotlib.pyplot as plt
```

## Functionality
This project is designed to help users manage their investment portfolios. Currently, `main.py` serves as a testing platform while a GUI is under development.

### Portfolio & Accounts
- A **Portfolio** object can be created using `Portfolio()`.
- Multiple accounts can be held within a portfolio, including:
  - FHSA
  - TFSA
  - RRSP
  - Other
- An account must be initialized before usage.

### Trading Functions
- **Buying & Selling Equities**:
  - `.buy_equity_for_account(account_name)` - Buys an equity for a specific account.
  - `.sell_equity_for_account(account_name)` - Sells an equity for a specific account.
  - Trades are recorded in a dictionary.
- **Exporting Trades**:
  - `export_trades_to_csv()` exports all trades into a CSV file.

### Visualization & Analysis
- **Portfolio Value & Cash Flow**:
  - `Plot_Portfolio_Cash_and_Value.py` reads transaction data and generates a line plot showing:
    - The value of holdings over time.
    - The total amount invested.
- **Portfolio Distribution**:
  - `PortfolioDistribution.py` creates a **pie chart** of the current holdings and their values.
- **Recent Stock Performance**:
  - `RecentStockPerformance.py` plots recent stock performance based on a user-defined date range and stock ticker.

## Usage
Run `main.py` to begin testing portfolio functionality. More detailed GUI-based interaction is in development.

---
This project is a work in progress, and additional features will be added over time.



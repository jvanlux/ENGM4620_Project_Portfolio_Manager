import yfinance as yf
from datetime import datetime

# Base class for all account types
class Account:
    def __init__(self):
        # Dictionary to store stocks: {ticker: [purchase_price, quantity_owned, purchase_date]}
        self.equities = {}
        # Track the total contributions
        self.total_contributions = 0

    def buy_equity(self, ticker, purchase_price, quantity, purchase_date):
        """Buy or add an equity to the account."""
        total_cost = purchase_price * quantity
        # Check if the contribution will exceed the contribution limit
        if hasattr(self, '_contribution_limit') and self._contribution_limit is not None:
            if self.total_contributions + total_cost > self._contribution_limit:
                print(f"Warning: Total contributions will exceed the contribution limit of {self._contribution_limit}.")
                proceed = input("Do you want to proceed with the purchase? (yes/no): ").strip().lower()
                if proceed != "yes":
                    print("Purchase cancelled.")
                    return

        # Update the total contributions
        self.total_contributions += total_cost
        if ticker in self.equities:
            # If the stock already exists, update the quantity and average price
            existing_price, existing_qty, _ = self.equities[ticker]
            new_qty = existing_qty + quantity
            # Calculate new average price
            new_price = ((existing_price * existing_qty) + (purchase_price * quantity)) / new_qty
            self.equities[ticker] = [new_price, new_qty, purchase_date]
        else:
            # If the stock does not exist, add it to the dictionary
            self.equities[ticker] = [purchase_price, quantity, purchase_date]
        print(f"Bought {quantity} shares of {ticker} at {purchase_price} each.")

    def sell_equity(self, ticker, quantity, sell_price, sell_date):
        """Sell an equity from the account."""
        if ticker in self.equities:
            purchase_price, existing_qty, purchase_date = self.equities[ticker]
            if existing_qty >= quantity:
                # Update the quantity after selling
                new_qty = existing_qty - quantity
                if new_qty == 0:
                    # Remove the equity if the quantity becomes zero
                    del self.equities[ticker]
                else:
                    self.equities[ticker] = [purchase_price, new_qty, purchase_date]
                print(f"Sold {quantity} shares of {ticker} at {sell_price} each on {sell_date}")
                # Successful sale
                return True
            else:
                print(f"Not enough quantity of {ticker} to sell.")
                # Not enough quantity to sell
                return False
        else:
            print(f"Equity {ticker} not found in account.")
            # Equity not found
            return False

    def get_value(self):
        """Calculate the total value of the account."""
        total_value = 0
        book_value = 0
        for ticker, (purchase_price, quantity, _) in self.equities.items():
            stock = yf.Ticker(ticker)
            current_price = stock.history(period="1d")["Close"].iloc[-1]
            total_value += current_price * quantity
            book_value += quantity * purchase_price
        return {"Total Value": total_value, "Book Value": book_value}

    def print_holdings(self):
        """Print the holdings of the account."""
        if not self.equities:
            print("No holdings in this account.")
        else:
            print("Holdings in the account:")
            for ticker, (purchase_price, quantity, purchase_date) in self.equities.items():
                stock = yf.Ticker(ticker)
                current_price = stock.history(period="1d")["Close"].iloc[-1]
                print(f"Ticker: {ticker}, Purchase Price: {purchase_price}, Current Price: {current_price}, Quantity: {quantity}, Purchase Date: {purchase_date}")

    def update_contribution_limit(self, new_limit):
        """Update the contribution limit for the account."""
        if hasattr(self, '_contribution_limit'):
            self._contribution_limit = new_limit
            print(f"Contribution limit updated to {new_limit}.")
        else:
            print("This account type does not have a contribution limit that can be updated.")

# FHSA Account class inheriting from Account
class FHSA(Account):
    def __init__(self, contribution_limit):
        super().__init__()
        self._contribution_limit = contribution_limit


# TFSA Account class inheriting from Account
class TFSA(Account):
    def __init__(self, contribution_limit):
        super().__init__()
        self._contribution_limit = contribution_limit


# RRSP Account class inheriting from Account
class RRSP(Account):
    def __init__(self, contribution_limit):
        super().__init__()
        self._contribution_limit = contribution_limit

# Other Account class inheriting from Account
class Other(Account):
    def __init__(self, contribution_limit=None):
        super().__init__()
        self._contribution_limit = contribution_limit

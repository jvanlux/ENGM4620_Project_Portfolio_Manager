import accounts
from datetime import datetime

# Portfolio class to manage the accounts
class Portfolio:
    account_list = []

    def __init__(self):
        pass

    def new_account(self, type):
        try:
            if type not in ["FHSA", "TFSA", "RRSP", "Other"]:
                raise ValueError()
        except ValueError:
            print("Account Type Not Supported: Valid Account Types are FHSA, TFSA, RRSP, Other")
        else:
            if type == "FHSA":
                contribution_limit = float(input("Enter Contribution Limit of FHSA: "))
                account_FHSA = accounts.FHSA(contribution_limit)
                self.account_list.append(account_FHSA)
                return account_FHSA
            elif type == "TFSA":
                contribution_limit = float(input("Enter Contribution Limit of TFSA: "))
                account_TFSA = accounts.TFSA(contribution_limit)
                self.account_list.append(account_TFSA)
                return account_TFSA
            elif type == "RRSP":
                contribution_limit = float(input("Enter Contribution Limit of RRSP: "))
                account_RRSP = accounts.RRSP(contribution_limit)
                self.account_list.append(account_RRSP)
                return account_RRSP
            elif type == "Other":
                contribution_limit = float(input("Enter Contribution Limit of Other Account (it won't be used): "))
                account_Other = accounts.Other(contribution_limit)
                self.account_list.append(account_Other)
                return account_Other

    def get_portfolio_value(self):
        """Calculate the total value of all accounts in the portfolio."""
        total_value = 0
        book_value = 0
        for account in self.account_list:
            account_data = account.get_value()
            total_value += account_data["Total Value"]
            book_value += account_data["Book Value"]
        return {"Total Value": total_value, "Book Value": book_value}

    def print_portfolio_holdings(self):
        """Print the holdings of all accounts in the portfolio."""
        if not self.account_list:
            print("No accounts in the portfolio.")
        else:
            print("Portfolio Holdings:")
            for account in self.account_list:
                print(f"\nAccount: {account.__class__.__name__}")
                # Print holdings of each account
                account.print_holdings()

    def buy_equity_for_account(self, account):
        """Get user input for buying an equity and execute the buy_equity method."""
        ticker = input("Enter the stock ticker to buy: ")

        # Handle purchase price with error handling
        while True:
            try:
                purchase_price = float(input(f"Enter the purchase price for {ticker}: "))
                if purchase_price <= 0:
                    raise ValueError("Price must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid purchase price.")

        # Handle quantity with error handling
        while True:
            try:
                quantity = int(input(f"Enter the quantity of {ticker} to buy: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid quantity.")

        # Handle purchase date with default to today's date if empty
        purchase_date_input = input(f"Enter the purchase date for {ticker} (YYYY-MM-DD) or press Enter for today: ")
        if not purchase_date_input:
            purchase_date = datetime.today().strftime('%Y-%m-%d')  # Use today's date
        else:
            try:
                purchase_date = datetime.strptime(purchase_date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using today's date.")
                # Fallback to today if the format is incorrect
                purchase_date = datetime.today().strftime('%Y-%m-%d')

                # Call buy_equity method on the account object
        account.buy_equity(ticker, purchase_price, quantity, purchase_date)
        print(f"Bought {quantity} shares of {ticker} at {purchase_price} each.")

    def sell_equity_for_account(self, account):
        """Get user input for selling an equity and execute the sell_equity method."""
        ticker = input("Enter the stock ticker to sell: ")

        # Handle quantity with error handling
        while True:
            try:
                quantity = int(input(f"Enter the quantity of {ticker} to sell: "))
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid quantity.")

        # Handle sell price with error handling
        while True:
            try:
                sell_price = float(input(f"Enter the sell price for {ticker}: "))
                if sell_price <= 0:
                    raise ValueError("Sell price must be greater than zero.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid sell price.")

        # Handle sell date with default to today's date if empty
        sell_date_input = input(f"Enter the sell date for {ticker} (YYYY-MM-DD) or press Enter for today: ")
        if not sell_date_input:
            sell_date = datetime.today().strftime('%Y-%m-%d')  # Use today's date
        else:
            try:
                sell_date = datetime.strptime(sell_date_input, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using today's date.")
                # Fallback to today if the format is incorrect
                sell_date = datetime.today().strftime('%Y-%m-%d')
                # Call sell_equity method on the account object
        success = account.sell_equity(ticker, quantity, sell_price, sell_date)
        if success:
            print(f"Successfully sold {quantity} shares of {ticker}.")
        else:
            print(f"Failed to sell {quantity} shares of {ticker}.")

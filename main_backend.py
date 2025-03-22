from accounts import Account
from colorama import Fore, Style, init

def main():

    # Initialize
    account_loaded = False
    init(autoreset=True)

    header = f"""
    {Fore.LIGHTGREEN_EX}███╗   ███╗███████╗ ██████╗██╗  ██╗    ██╗  ██╗ ██████╗ ██████╗  ██████╗ 
    ████╗ ████║██╔════╝██╔════╝██║  ██║    ██║  ██║██╔════╝ ╚════██╗██╔═████╗
    ██╔████╔██║█████╗  ██║     ███████║    ███████║███████╗  █████╔╝██║██╔██║
    ██║╚██╔╝██║██╔══╝  ██║     ██╔══██║    ╚════██║██╔═══██╗██╔═══╝ ████╔╝██║
    ██║ ╚═╝ ██║███████╗╚██████╗██║  ██║         ██║╚██████╔╝███████╗╚██████╔╝
    ╚═╝     ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝         ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝                                                                    
    {Fore.LIGHTGREEN_EX}========================================================================
    
    {Fore.LIGHTGREEN_EX}                      PORTFOLIO MANAGEMENT TOOL
    {Fore.LIGHTGREEN_EX}Developed by: James McIntosh (B00833105) & John VanLuxemborg (B00892614)
    
    {Fore.LIGHTGREEN_EX}       For on the code please see the Github repository here
         https://github.com/jvanlux/ENGM4620_Project_Portfolio_Manager 
    
    {Fore.LIGHTGREEN_EX}========================================================================
    {Style.RESET_ALL}"""
    print(header)

    print("Please select from the following list of options: \n1: Create/Load Account \n2: Buy or Sell Equities \n3: Bulk Equity Import \n4: Plot Pie Chart Holdings"
          "\n5: Plot Account Balance Trend \n6: Display Account Holdings \n7: Print Options \n8: Exit Program")

    while True:

        response = input("\nPlease enter your selection: ")

        if response == "1":
            print("\n")
            my_account = Account()
            account_loaded = True

        elif response == "2":
            if account_loaded:
                my_account.buy_sell()
            else:
                print("Please enter your account first.")

        elif response == "3":
            if account_loaded:
                my_account.bulk_import()
            else:
                print("Please enter your account first.")

        elif response == "4":
            if account_loaded:
                my_account.plot_holdings_pie_chart()
            else:
                print("Please enter your account first.")

        elif response == "5":
            if account_loaded:
                my_account.plot_combined()
            else:
                print("Please enter your account first.")

        elif response == "6":
            if account_loaded:
                my_account.display_account_holdings()
            else:
                print("Please enter your account first.")

        elif response == "7":
            print(
                " 1: Create/Load Account \n 2: Buy or Sell Equities \n 3: Bulk Equity Import \n 4: Plot Pie Chart Holdings"
                "\n 5: Plot Account Balance Trend \n 6: Display Account Holdings \n 7: Print Options \n 8: Exit Program")

        elif response == "8":
            print("Saving and closing program.")
            break

        else:
            print("Please enter a valid input.")
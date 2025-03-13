from accounts import Account
from Plotting_Functions import plot_holdings_pie_chart, net_investment, portfolio_value, plot_combined

#testing purposes
my_account= Account()
my_account.print_all_holdings()

plot_holdings_pie_chart(my_account)
net_investment(my_account)

portfolio_value(my_account)

plot_combined(my_account)
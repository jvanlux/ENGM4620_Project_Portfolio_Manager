import matplotlib.pyplot as plt

def plot_holdings_pie_chart(account):
    """"""
    df = account.holdings().drop(index="Summary", errors="ignore")

    if df.empty:
        print("No holdings to display.")
        return

    labels = df.index
    sizes = df["Total Value"].astype(float)
    total_value = sizes.sum()

    # Prepare labels to include total value
    labels = [f"{label} (${value:,.2f})" for label, value in zip(labels, sizes)]

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=140, pctdistance=0.85,
        colors=plt.cm.Paired.colors, wedgeprops={"edgecolor": "black"}
    )

    ax.set_title(f"Portfolio Distribution\nTotal Value: ${total_value:,.2f}")
    ax.axis("equal")
    plt.show()


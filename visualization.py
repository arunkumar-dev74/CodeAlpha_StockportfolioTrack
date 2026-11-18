import matplotlib.pyplot as plt

from portfolio import (
    calculate_investment,
    calculate_current_value
)


def create_portfolio_chart(stocks):

    if not stocks:
        return None

    names = [stock["symbol"] for stock in stocks]

    investments = [
        calculate_investment(stock)
        for stock in stocks
    ]

    current_values = [
        calculate_current_value(stock)
        for stock in stocks
    ]

    fig, ax = plt.subplots(figsize=(10, 5))

    x = range(len(names))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        investments,
        width,
        label="Investment"
    )

    ax.bar(
        [i + width / 2 for i in x],
        current_values,
        width,
        label="Current Value"
    )

    ax.set_title("Stock Portfolio Analysis")
    ax.set_xlabel("Stocks")
    ax.set_ylabel("Value (INR)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(names)
    ax.legend()

    fig.tight_layout()

    return fig


def create_allocation_chart(stocks):

    if not stocks:
        return None

    names = [stock["symbol"] for stock in stocks]

    values = [
        calculate_current_value(stock)
        for stock in stocks
    ]

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.pie(
        values,
        labels=names,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Portfolio Allocation")

    return fig
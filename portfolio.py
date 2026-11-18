def validate_stock(symbol, quantity, buy_price, current_price):
    if not symbol or not symbol.strip():
        raise ValueError("Stock symbol cannot be empty.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    if buy_price <= 0 or current_price <= 0:
        raise ValueError("Prices must be greater than zero.")


def calculate_investment(stock):
    return stock["quantity"] * stock["buy_price"]


def calculate_current_value(stock):
    return stock["quantity"] * stock["current_price"]


def calculate_profit_loss(stock):
    return (
        calculate_current_value(stock)
        - calculate_investment(stock)
    )


def calculate_profit_percentage(stock):
    investment = calculate_investment(stock)

    if investment == 0:
        return 0

    profit = calculate_profit_loss(stock)

    return (profit / investment) * 100


def get_portfolio_summary(stocks):
    total_investment = sum(
        calculate_investment(stock) for stock in stocks
    )

    total_value = sum(
        calculate_current_value(stock) for stock in stocks
    )

    profit_loss = total_value - total_investment

    profit_percentage = (
        (profit_loss / total_investment) * 100
        if total_investment else 0
    )

    return {
        "total_investment": total_investment,
        "total_value": total_value,
        "profit_loss": profit_loss,
        "profit_percentage": profit_percentage
    }


def search_stocks(stocks, keyword):
    keyword = keyword.strip().upper()

    if not keyword:
        return stocks

    return [
        stock for stock in stocks
        if keyword in stock["symbol"].upper()
    ]
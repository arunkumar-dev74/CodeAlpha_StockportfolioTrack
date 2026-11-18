import streamlit as st
import pandas as pd

from datetime import date

import database
import portfolio
import visualization

import streamlit as st

# GREEN THEME CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #052e16,
        #064e3b,
        #022c22
    );
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #022c22;
}

[data-testid="stHeader"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)


# Page Configuration
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈",
    layout="wide"
)


# Initialize Database
database.initialize_database()


# Dashboard Header
st.title("📈 Stock Portfolio Tracker")
st.caption("Manage and analyze your stock investments.")

stocks = database.get_all_stocks()


# Portfolio Summary
summary = portfolio.get_portfolio_summary(stocks)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Investment",
    f"₹{summary['total_investment']:,.2f}"
)

col2.metric(
    "Current Value",
    f"₹{summary['total_value']:,.2f}"
)

col3.metric(
    "Profit / Loss",
    f"₹{summary['profit_loss']:,.2f}",
    delta=f"{summary['profit_percentage']:.2f}%"
)

col4.metric(
    "Total Stocks",
    len(stocks)
)


st.divider()


# Sidebar Navigation
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Add Stock",
        "Update Stock",
        "Delete Stock",
        "Search Stocks"
    ]
)


# Dashboard
if menu == "Dashboard":

    st.header("Portfolio Overview")

    if stocks:

        df = pd.DataFrame(stocks)

        df["investment"] = df.apply(
            portfolio.calculate_investment,
            axis=1
        )

        df["current_value"] = df.apply(
            portfolio.calculate_current_value,
            axis=1
        )

        df["profit_loss"] = df.apply(
            portfolio.calculate_profit_loss,
            axis=1
        )

        df["profit_percentage"] = df.apply(
            portfolio.calculate_profit_percentage,
            axis=1
        )

        st.subheader("Your Stock Holdings")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Investment vs Current Value")

        fig = visualization.create_portfolio_chart(stocks)

        if fig:
            st.pyplot(fig)
            import matplotlib.pyplot as plt
            plt.close(fig)

        st.subheader("Portfolio Allocation")

        fig = visualization.create_allocation_chart(stocks)

        if fig:
            st.pyplot(fig)
            plt.close(fig)

    else:
        st.info("No stocks available. Add your first stock!")


# Add Stock
elif menu == "Add Stock":

    st.header("Add New Stock")

    with st.form("add_stock_form"):

        symbol = st.text_input(
            "Stock Symbol",
            placeholder="Example: TCS"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

        buy_price = st.number_input(
            "Buy Price (₹)",
            min_value=0.01,
            step=0.01
        )

        current_price = st.number_input(
            "Current Price (₹)",
            min_value=0.01,
            step=0.01
        )

        purchase_date = st.date_input(
            "Purchase Date",
            value=date.today(),
            max_value=date.today()
        )

        submitted = st.form_submit_button("Add Stock")

        if submitted:

            try:
                portfolio.validate_stock(
                    symbol,
                    quantity,
                    buy_price,
                    current_price
                )

                database.add_stock(
                    symbol,
                    quantity,
                    buy_price,
                    current_price,
                    purchase_date.isoformat()
                )

                st.success("Stock added successfully!")

            except ValueError as error:
                st.error(str(error))


# Update Stock
elif menu == "Update Stock":

    st.header("Update Stock Details")

    if stocks:

        stock_options = {
            f"{stock['symbol']} (ID: {stock['id']})": stock
            for stock in stocks
        }

        selected = st.selectbox(
            "Select Stock",
            list(stock_options.keys())
        )

        stock = stock_options[selected]

        with st.form("update_stock_form"):

            symbol = st.text_input(
                "Stock Symbol",
                value=stock["symbol"]
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=stock["quantity"]
            )

            buy_price = st.number_input(
                "Buy Price",
                min_value=0.01,
                value=float(stock["buy_price"])
            )

            current_price = st.number_input(
                "Current Price",
                min_value=0.01,
                value=float(stock["current_price"])
            )

            purchase_date = st.date_input(
                "Purchase Date",
                value=date.fromisoformat(stock["purchase_date"]),
                max_value=date.today()
            )

            submitted = st.form_submit_button("Update Stock")

            if submitted:

                try:
                    portfolio.validate_stock(
                        symbol,
                        quantity,
                        buy_price,
                        current_price
                    )

                    updated = database.update_stock(
                        stock["id"],
                        symbol,
                        quantity,
                        buy_price,
                        current_price,
                        purchase_date.isoformat()
                    )

                    if updated:
                        st.success("Stock updated successfully!")
                        st.rerun()

                except ValueError as error:
                    st.error(str(error))

    else:
        st.info("No stocks available to update.")


# Delete Stock
elif menu == "Delete Stock":

    st.header("Delete Stock")

    if stocks:

        stock_options = {
            f"{stock['symbol']} (ID: {stock['id']})": stock
            for stock in stocks
        }

        selected = st.selectbox(
            "Select Stock",
            list(stock_options.keys())
        )

        stock = stock_options[selected]

        st.warning(
            f"Are you sure you want to delete {stock['symbol']}?"
        )

        if st.button("Confirm Delete", type="primary"):

            deleted = database.delete_stock(stock["id"])

            if deleted:
                st.success("Stock deleted successfully!")
                st.rerun()

    else:
        st.info("No stocks available to delete.")


# Search Stocks
elif menu == "Search Stocks":

    st.header("Search Your Portfolio")

    keyword = st.text_input(
        "Enter Stock Symbol",
        placeholder="Example: TCS"
    )

    results = portfolio.search_stocks(stocks, keyword)

    if results:

        df = pd.DataFrame(results)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    elif keyword:
        st.warning("No matching stocks found.")

    else:
        st.info("Add stocks to start searching.")


# Footer
st.divider()

st.caption(
    "Stock Portfolio Tracker | Built with Python, SQLite and Streamlit"
)
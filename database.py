import sqlite3

DB_NAME = "portfolio.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            buy_price REAL NOT NULL,
            current_price REAL NOT NULL,
            purchase_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_stock(symbol, quantity, buy_price, current_price, purchase_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO stocks
        (symbol, quantity, buy_price, current_price, purchase_date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        symbol.upper(),
        quantity,
        buy_price,
        current_price,
        purchase_date
    ))

    conn.commit()
    conn.close()


def get_all_stocks():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks ORDER BY id DESC")

    stocks = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return stocks


def update_stock(stock_id, symbol, quantity, buy_price,
                 current_price, purchase_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE stocks
        SET symbol = ?,
            quantity = ?,
            buy_price = ?,
            current_price = ?,
            purchase_date = ?
        WHERE id = ?
    """, (
        symbol.upper(),
        quantity,
        buy_price,
        current_price,
        purchase_date,
        stock_id
    ))

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    return updated


def delete_stock(stock_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM stocks WHERE id = ?",
        (stock_id,)
    )

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    return deleted
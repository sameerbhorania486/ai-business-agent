from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_total_revenue() -> str:
    """
    Calculate the total revenue from all orders in the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM orders
    """)

    total_revenue = cursor.fetchone()[0]

    connection.close()

    return f"Total revenue is ₹{total_revenue:,.2f}"
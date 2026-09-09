from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_product_sales(product: str) -> str:
    """
    Get sales analytics for a specific product.
    Returns total units sold, number of orders, and total revenue.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            o.product,
            COALESCE(SUM(o.quantity), 0),
            COUNT(o.order_id),
            COALESCE(SUM(o.total_amount), 0)
        FROM orders o
        WHERE LOWER(o.product) LIKE ?
        GROUP BY o.product
    """, (f"%{product.strip().lower()}%",))

    result = cursor.fetchone()

    connection.close()

    if not result:
        return "Product sales data not found."

    return str({
        "product": result[0],
        "total_units_sold": result[1],
        "total_orders": result[2],
        "total_revenue": f"₹{result[3]:,.2f}",
    })
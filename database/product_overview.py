from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_product_sales_overview() -> str:
    """
    Get overall sales analytics for all products.
    Returns total units sold, total orders, and total revenue
    for each product, sorted by revenue.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product,
            COALESCE(SUM(quantity), 0) AS total_units_sold,
            COUNT(order_id) AS total_orders,
            COALESCE(SUM(total_amount), 0) AS total_revenue
        FROM orders
        GROUP BY product
        ORDER BY total_revenue DESC
    """)

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "No sales data found."

    products = []

    for product in results:
        products.append({
            "product": product[0],
            "total_units_sold": product[1],
            "total_orders": product[2],
            "total_revenue": f"₹{product[3]:,.2f}",
        })

    return str(products)
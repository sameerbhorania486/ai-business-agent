from langchain_core.tools import tool

from database.db import get_connection


@tool
def check_low_stock(threshold: int = 30) -> str:
    """
    Find products whose inventory quantity is at or below the given threshold.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, product, quantity, price
        FROM inventory
        WHERE quantity <= ?
        ORDER BY quantity ASC
    """, (threshold,))

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "No low-stock products found."

    low_stock_products = []

    for item in results:
        low_stock_products.append({
            "product_id": item[0],
            "product": item[1],
            "quantity": item[2],
            "price": item[3],
        })

    return str(low_stock_products)
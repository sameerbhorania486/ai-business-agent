from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_restock_recommendations(threshold: int = 30) -> str:
    """
    Identify products that need restocking.
    Returns current stock, price, and recommended restock quantity.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product,
            quantity,
            price
        FROM inventory
        WHERE quantity <= ?
        ORDER BY quantity ASC
    """, (threshold,))

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "No products currently need restocking."

    recommendations = []

    for item in results:
        product_id, product, quantity, price = item

        # Target stock level
        target_stock = 50

        restock_quantity = max(target_stock - quantity, 0)

        recommendations.append({
            "product_id": product_id,
            "product": product,
            "current_stock": quantity,
            "price": f"₹{price:,.2f}",
            "recommended_restock_quantity": restock_quantity,
        })

    return str(recommendations)
from langchain_core.tools import tool

from database.db import get_connection


@tool
def search_inventory(product: str) -> str:
    """
    Search inventory for a product from the SQLite database.
    Handles singular and plural product names.
    Returns available quantity and price.
    """

    product = product.strip().lower()

    # Handle common plural forms
    if product.endswith("s"):
        product = product[:-1]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, product, quantity, price
        FROM inventory
        WHERE LOWER(product) LIKE ?
    """, (f"%{product}%",))

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "Product not found in inventory."

    inventory = []

    for item in results:
        inventory.append({
            "product_id": item[0],
            "product": item[1],
            "quantity": item[2],
            "price": item[3],
        })

    return str(inventory)
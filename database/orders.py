from langchain_core.tools import tool

from database.db import get_connection


@tool
def search_orders(customer_id: str) -> str:
    """
    Search orders for a customer from the SQLite database.
    """

    try:
        customer_id = int(customer_id)
    except ValueError:
        return "Invalid customer ID."

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, customer_id, product, quantity, total_amount, status
        FROM orders
        WHERE customer_id = ?
    """, (customer_id,))

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "No orders found for this customer."

    orders = []

    for order in results:
        orders.append({
            "order_id": order[0],
            "customer_id": order[1],
            "product": order[2],
            "quantity": order[3],
            "total_amount": order[4],
            "status": order[5],
        })

    return str(orders)
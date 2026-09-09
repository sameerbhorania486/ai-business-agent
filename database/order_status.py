from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_order_status(order_id: str) -> str:
    """
    Get the status and details of a specific order.
    """

    try:
        order_id = int(order_id)
    except ValueError:
        return "Invalid order ID."

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            o.order_id,
            c.name,
            o.product,
            o.quantity,
            o.total_amount,
            o.status
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.id
        WHERE o.order_id = ?
    """, (order_id,))

    order = cursor.fetchone()

    connection.close()

    if not order:
        return "Order not found."

    return str({
        "order_id": order[0],
        "customer": order[1],
        "product": order[2],
        "quantity": order[3],
        "amount": f"₹{order[4]:,.2f}",
        "status": order[5],
    })
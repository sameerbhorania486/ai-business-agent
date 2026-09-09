from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_customer_order_summary(customer_name: str) -> str:
    """
    Get a complete order summary for a specific customer.
    Includes customer details, order count, total quantity, products,
    order statuses, and total revenue.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.name,
            c.company,
            COUNT(o.order_id),
            COALESCE(SUM(o.quantity), 0),
            COALESCE(SUM(o.total_amount), 0)
        FROM customers c
        LEFT JOIN orders o
            ON c.id = o.customer_id
        WHERE c.name LIKE ?
        GROUP BY c.id, c.name, c.company
    """, (f"%{customer_name.strip()}%",))

    customer = cursor.fetchone()

    if not customer:
        connection.close()
        return "Customer not found."

    cursor.execute("""
        SELECT
            o.order_id,
            o.product,
            o.quantity,
            o.total_amount,
            o.status
        FROM customers c
        JOIN orders o
            ON c.id = o.customer_id
        WHERE c.name LIKE ?
        ORDER BY o.order_id
    """, (f"%{customer_name.strip()}%",))

    orders = cursor.fetchall()

    connection.close()

    summary = {
        "customer": customer[0],
        "company": customer[1],
        "total_orders": customer[2],
        "total_quantity": customer[3],
        "total_revenue": f"₹{customer[4]:,.2f}",
        "orders": []
    }

    for order in orders:
        summary["orders"].append({
            "order_id": order[0],
            "product": order[1],
            "quantity": order[2],
            "amount": f"₹{order[3]:,.2f}",
            "status": order[4]
        })

    return str(summary)
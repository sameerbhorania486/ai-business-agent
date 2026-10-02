from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_order_status(
    order_id: str,
    business_id: int
) -> str:
    """
    Get the status and details of a specific order
    within the authenticated business.
    """

    try:
        order_id = int(order_id)
    except ValueError:
        return "Invalid order ID."

    supabase = get_connection()

    # =========================
    # GET ORDER
    # =========================

    order_response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status"
        )
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .execute()
    )

    orders = order_response.data

    if not orders:
        return "Order not found."

    order = orders[0]

    # =========================
    # GET CUSTOMER
    # =========================

    customer_response = (
        supabase
        .table("customers")
        .select("name")
        .eq("id", order["customer_id"])
        .eq("business_id", business_id)
        .execute()
    )

    customers = customer_response.data

    customer_name = (
        customers[0]["name"]
        if customers
        else "Unknown customer"
    )

    # =========================
    # RETURN ORDER DETAILS
    # =========================

    return str({
        "order_id": order["order_id"],
        "customer": customer_name,
        "product": order["product"],
        "quantity": order["quantity"],
        "amount": f"₹{float(order['total_amount']):,.2f}",
        "status": order["status"],
    })


if __name__ == "__main__":
    print(
        get_order_status.invoke({
            "order_id": "1",
            "business_id": 1
        })
    )

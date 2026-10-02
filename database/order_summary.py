from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_customer_order_summary(
    customer_name: str,
    business_id: int
) -> str:
    """
    Get a complete order summary for a specific customer
    within the authenticated business.

    Includes customer details, order count,
    total quantity, products, order statuses,
    and total revenue.
    """

    supabase = get_connection()

    # =========================
    # FIND CUSTOMER
    # =========================

    customer_response = (
        supabase
        .table("customers")
        .select("id, name, company")
        .eq("business_id", business_id)
        .ilike(
            "name",
            f"%{customer_name.strip()}%"
        )
        .execute()
    )

    customers = customer_response.data

    if not customers:
        return "Customer not found."

    customer = customers[0]

    # =========================
    # FIND CUSTOMER ORDERS
    # =========================

    order_response = (
        supabase
        .table("orders")
        .select(
            "order_id, product, quantity, "
            "total_amount, status"
        )
        .eq("customer_id", customer["id"])
        .eq("business_id", business_id)
        .order("order_id")
        .execute()
    )

    orders = order_response.data

    # =========================
    # CALCULATE SUMMARY
    # =========================

    total_orders = len(orders)

    total_quantity = sum(
        order["quantity"]
        for order in orders
    )

    total_revenue = sum(
        float(order["total_amount"])
        for order in orders
    )

    summary = {
        "customer": customer["name"],
        "company": customer["company"],
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "total_revenue": f"₹{total_revenue:,.2f}",
        "orders": []
    }

    # =========================
    # ORDER DETAILS
    # =========================

    for order in orders:

        summary["orders"].append({
            "order_id": order["order_id"],
            "product": order["product"],
            "quantity": order["quantity"],
            "amount": f"₹{float(order['total_amount']):,.2f}",
            "status": order["status"]
        })

    return str(summary)


if __name__ == "__main__":
    print(
        get_customer_order_summary.invoke({
            "customer_name": "Rahul",
            "business_id": 1
        })
    )
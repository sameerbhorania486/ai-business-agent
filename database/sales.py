from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_total_revenue(business_id: int) -> str:
    """
    Calculate the total revenue from all orders
    within the authenticated business.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("orders")
        .select("total_amount")
        .eq("business_id", business_id)
        .execute()
    )

    results = response.data

    if not results:
        return "Total revenue is ₹0.00"

    total_revenue = sum(
        float(order["total_amount"])
        for order in results
    )

    return f"Total revenue is ₹{total_revenue:,.2f}"


if __name__ == "__main__":
    print(
        get_total_revenue.invoke({
            "business_id": 1
        })
    )
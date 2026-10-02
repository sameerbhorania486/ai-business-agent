from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_product_sales(
    product: str,
    business_id: int
) -> str:
    """
    Get sales analytics for a specific product
    within the authenticated business.

    Returns total units sold, number of orders,
    and total revenue.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("orders")
        .select(
            "product, quantity, total_amount, order_id"
        )
        .eq("business_id", business_id)
        .ilike(
            "product",
            f"%{product.strip()}%"
        )
        .execute()
    )

    results = response.data

    if not results:
        return "Product sales data not found."

    total_units_sold = sum(
        order["quantity"]
        for order in results
    )

    total_orders = len(results)

    total_revenue = sum(
        float(order["total_amount"])
        for order in results
    )

    return str({
        "product": results[0]["product"],
        "total_units_sold": total_units_sold,
        "total_orders": total_orders,
        "total_revenue": f"₹{total_revenue:,.2f}",
    })


if __name__ == "__main__":
    print(
        get_product_sales.invoke({
            "product": "Laptop",
            "business_id": 1
        })
    )

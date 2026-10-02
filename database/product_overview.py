from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_product_sales_overview(
    business_id: int
) -> str:
    """
    Get overall sales analytics for all products
    within the authenticated business.

    Returns total units sold, total orders,
    and total revenue for each product,
    sorted by revenue.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("orders")
        .select(
            "product, quantity, total_amount, order_id"
        )
        .eq("business_id", business_id)
        .execute()
    )

    results = response.data

    if not results:
        return "No sales data found."

    product_data = {}

    for order in results:

        product = order["product"]

        if product not in product_data:
            product_data[product] = {
                "product": product,
                "total_units_sold": 0,
                "total_orders": 0,
                "total_revenue": 0.0,
            }

        product_data[product]["total_units_sold"] += (
            order["quantity"]
        )

        product_data[product]["total_orders"] += 1

        product_data[product]["total_revenue"] += (
            float(order["total_amount"])
        )

    products = list(product_data.values())

    products.sort(
        key=lambda x: x["total_revenue"],
        reverse=True
    )

    for product in products:
        product["total_revenue"] = (
            f"₹{product['total_revenue']:,.2f}"
        )

    return str(products)


if __name__ == "__main__":
    print(
        get_product_sales_overview.invoke({
            "business_id": 1
        })
    )
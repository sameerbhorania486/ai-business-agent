from langchain_core.tools import tool

from database.db import get_connection


@tool
def get_restock_recommendations(
    threshold: int = 30,
    business_id: int = 0
) -> str:
    """
    Identify products that need restocking
    within the authenticated business.

    Returns current stock, price, and
    recommended restock quantity.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq("business_id", business_id)
        .lte("quantity", threshold)
        .order("quantity")
        .execute()
    )

    results = response.data

    if not results:
        return "No products currently need restocking."

    recommendations = []

    for item in results:

        quantity = item["quantity"]

        target_stock = 50

        restock_quantity = max(
            target_stock - quantity,
            0
        )

        recommendations.append({
            "product_id": item["product_id"],
            "product": item["product"],
            "current_stock": quantity,
            "price": f"₹{float(item['price']):,.2f}",
            "recommended_restock_quantity": restock_quantity,
        })

    return str(recommendations)


if __name__ == "__main__":
    print(
        get_restock_recommendations.invoke({
            "threshold": 30,
            "business_id": 1
        })
    )
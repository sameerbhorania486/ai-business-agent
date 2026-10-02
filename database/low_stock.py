from langchain_core.tools import tool

from database.db import get_connection


@tool
def check_low_stock(
    threshold: int = 30,
    business_id: int = 0
) -> str:
    """
    Find products whose inventory quantity
    is at or below the given threshold
    within the authenticated business.
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
        return "No low-stock products found."

    low_stock_products = []

    for item in results:
        low_stock_products.append({
            "product_id": item["product_id"],
            "product": item["product"],
            "quantity": item["quantity"],
            "price": item["price"],
        })

    return str(low_stock_products)


if __name__ == "__main__":
    print(
        check_low_stock.invoke({
            "threshold": 30,
            "business_id": 1
        })
    )
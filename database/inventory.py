from langchain_core.tools import tool

from database.db import get_connection


# =========================================================
# SEARCH INVENTORY
# =========================================================

@tool
def search_inventory(
    product: str,
    business_id: int
) -> str:
    """
    Search inventory for a product
    within the authenticated business.
    """

    product = product.strip().lower()

    # Handle common plural forms
    if product.endswith("s"):
        product = product[:-1]

    supabase = get_connection()

    response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq("business_id", business_id)
        .ilike(
            "product",
            f"%{product}%"
        )
        .execute()
    )

    results = response.data

    if not results:
        return "Product not found in inventory."

    inventory = []

    for item in results:
        inventory.append({
            "product_id": item["product_id"],
            "product": item["product"],
            "quantity": item["quantity"],
            "price": item["price"],
        })

    return str(inventory)


# =========================================================
# GET ALL INVENTORY
# =========================================================

@tool
def get_all_inventory(
    business_id: int
) -> str:
    """
    Get all inventory products
    belonging to the authenticated business.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq("business_id", business_id)
        .order("product_id")
        .execute()
    )

    products = response.data

    if not products:
        return "No products found in inventory."

    inventory = []

    for item in products:
        inventory.append({
            "product_id": item["product_id"],
            "product": item["product"],
            "quantity": item["quantity"],
            "price": item["price"],
        })

    return str({
        "status": "success",
        "inventory": inventory
    })


# =========================================================
# ADD PRODUCT
# =========================================================

@tool
def add_inventory_product(
    product: str,
    quantity: int,
    price: float,
    business_id: int = 0
) -> str:
    """
    Add a new product to inventory
    within the authenticated business.
    """

    product = product.strip()

    if not product:
        return "Product name is required."

    if quantity < 0:
        return "Quantity cannot be negative."

    if price < 0:
        return "Price cannot be negative."

    supabase = get_connection()

    # Check if product already exists
    existing_response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product"
        )
        .eq("business_id", business_id)
        .ilike("product", product)
        .limit(1)
        .execute()
    )

    if existing_response.data:
        return "Product already exists in inventory."

    # Get latest product ID
    latest_response = (
        supabase
        .table("inventory")
        .select("product_id")
        .order("product_id", desc=True)
        .limit(1)
        .execute()
    )

    latest_products = latest_response.data

    if latest_products:
        new_product_id = (
            latest_products[0]["product_id"] + 1
        )
    else:
        new_product_id = 1

    # Insert product
    response = (
        supabase
        .table("inventory")
        .insert({
            "product_id": new_product_id,
            "product": product,
            "quantity": quantity,
            "price": price,
            "business_id": business_id
        })
        .execute()
    )

    if not response.data:
        return "Failed to add product to inventory."

    item = response.data[0]

    return str({
        "status": "success",
        "message": "Product added successfully.",
        "product": {
            "product_id": item["product_id"],
            "product": item["product"],
            "quantity": item["quantity"],
            "price": item["price"]
        }
    })


# =========================================================
# UPDATE PRODUCT
# =========================================================

@tool
def update_inventory_product(
    product_id: int,
    quantity: int | None = None,
    price: float | None = None,
    business_id: int = 0
) -> str:
    """
    Update the quantity or price of an inventory product
    within the authenticated business.
    """

    if quantity is not None and quantity < 0:
        return "Quantity cannot be negative."

    if price is not None and price < 0:
        return "Price cannot be negative."

    if quantity is None and price is None:
        return "No inventory information was provided to update."

    supabase = get_connection()

    # Check product belongs to this business
    existing_response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq("product_id", product_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    products = existing_response.data

    if not products:
        return "Product not found in inventory."

    updates = {}

    if quantity is not None:
        updates["quantity"] = quantity

    if price is not None:
        updates["price"] = price

    response = (
        supabase
        .table("inventory")
        .update(updates)
        .eq("product_id", product_id)
        .eq("business_id", business_id)
        .execute()
    )

    if not response.data:
        return "Failed to update inventory product."

    item = response.data[0]

    return str({
        "status": "success",
        "message": "Inventory product updated successfully.",
        "product": {
            "product_id": item["product_id"],
            "product": item["product"],
            "quantity": item["quantity"],
            "price": item["price"]
        }
    })


# =========================================================
# DELETE PRODUCT
# =========================================================

@tool
def delete_inventory_product(
    product_id: int,
    business_id: int = 0
) -> str:
    """
    Delete an inventory product
    within the authenticated business.
    """

    supabase = get_connection()

    # Check product belongs to this business
    existing_response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq("product_id", product_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    products = existing_response.data

    if not products:
        return "Product not found in inventory."

    item = products[0]

    # Delete product
    response = (
        supabase
        .table("inventory")
        .delete()
        .eq("product_id", product_id)
        .eq("business_id", business_id)
        .execute()
    )

    if not response.data:
        return "Failed to delete inventory product."

    return str({
        "status": "success",
        "message": "Product deleted successfully.",
        "product": {
            "product_id": item["product_id"],
            "product": item["product"],
            "quantity": item["quantity"],
            "price": item["price"]
        }
    })


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        search_inventory.invoke({
            "product": "Laptop",
            "business_id": 4
        })
    )

    print(
        get_all_inventory.invoke({
            "business_id": 4
        })
    )
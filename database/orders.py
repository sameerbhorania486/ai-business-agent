from langchain_core.tools import tool

from database.db import get_connection


# =========================================================
# COMMON
# =========================================================

ALLOWED_STATUSES = [
    "pending",
    "confirmed",
    "shipped",
    "delivered",
    "cancelled"
]


# =========================================================
# SEARCH ORDERS BY CUSTOMER
# =========================================================

@tool
def search_orders(
    customer_id: str,
    business_id: int
) -> str:
    """
    Search all orders for a customer
    within the authenticated business.
    """

    try:
        customer_id = int(customer_id)
    except ValueError:
        return "Invalid customer ID."

    supabase = get_connection()

    response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status, business_id"
        )
        .eq("customer_id", customer_id)
        .eq("business_id", business_id)
        .order("order_id", desc=True)
        .execute()
    )

    results = response.data

    if not results:
        return "No orders found for this customer."

    return str({
        "status": "success",
        "orders": results
    })


# =========================================================
# GET ALL ORDERS
# =========================================================

@tool
def get_all_orders(
    business_id: int
) -> str:
    """
    Get all orders belonging to the authenticated business.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status, business_id"
        )
        .eq("business_id", business_id)
        .order("order_id", desc=True)
        .execute()
    )

    orders = response.data

    if not orders:
        return "No orders found."

    return str({
        "status": "success",
        "orders": orders
    })


# =========================================================
# GET ORDER BY ID
# =========================================================

@tool
def get_order_by_id(
    order_id: int,
    business_id: int
) -> str:
    """
    Get a specific order by order ID
    within the authenticated business.
    """

    supabase = get_connection()

    response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status, business_id"
        )
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    orders = response.data

    if not orders:
        return "Order not found."

    return str({
        "status": "success",
        "order": orders[0]
    })


# =========================================================
# CREATE ORDER
# =========================================================

@tool
def create_order(
    customer_id: int,
    product: str,
    quantity: int,
    total_amount: float,
    status: str = "pending",
    business_id: int = 0
) -> str:
    """
    Create a new order for a customer
    within the authenticated business.
    """

    if quantity <= 0:
        return "Quantity must be greater than 0."

    if total_amount < 0:
        return "Total amount cannot be negative."

    product = product.strip()

    if not product:
        return "Product name is required."

    status = status.strip().lower()

    if status not in ALLOWED_STATUSES:
        return (
            "Invalid order status. "
            "Use: pending, confirmed, shipped, "
            "delivered, or cancelled."
        )

    supabase = get_connection()

    # -----------------------------------------------------
    # CHECK CUSTOMER
    # -----------------------------------------------------

    customer_response = (
        supabase
        .table("customers")
        .select("id, name")
        .eq("id", customer_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    customers = customer_response.data

    if not customers:
        return "Customer not found in this business."

    # -----------------------------------------------------
    # GET NEXT ORDER ID
    # -----------------------------------------------------

    latest_order_response = (
        supabase
        .table("orders")
        .select("order_id")
        .order("order_id", desc=True)
        .limit(1)
        .execute()
    )

    latest_orders = latest_order_response.data

    if latest_orders:
        new_order_id = latest_orders[0]["order_id"] + 1
    else:
        new_order_id = 1

    # -----------------------------------------------------
    # CREATE ORDER
    # -----------------------------------------------------

    response = (
        supabase
        .table("orders")
        .insert({
            "order_id": new_order_id,
            "customer_id": customer_id,
            "product": product,
            "quantity": quantity,
            "total_amount": total_amount,
            "status": status,
            "business_id": business_id
        })
        .execute()
    )

    if not response.data:
        return "Failed to create order."

    order = response.data[0]

    return str({
        "status": "success",
        "message": "Order created successfully.",
        "order": {
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "product": order["product"],
            "quantity": order["quantity"],
            "total_amount": order["total_amount"],
            "status": order["status"],
            "business_id": order["business_id"]
        }
    })


# =========================================================
# UPDATE ORDER STATUS
# =========================================================

@tool
def update_order_status(
    order_id: int,
    status: str,
    business_id: int = 0
) -> str:
    """
    Update the status of an existing order
    within the authenticated business.
    """

    status = status.strip().lower()

    if status not in ALLOWED_STATUSES:
        return (
            "Invalid order status. "
            "Use: pending, confirmed, shipped, "
            "delivered, or cancelled."
        )

    supabase = get_connection()

    # -----------------------------------------------------
    # CHECK ORDER
    # -----------------------------------------------------

    existing_response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status, business_id"
        )
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    orders = existing_response.data

    if not orders:
        return "Order not found."

    # -----------------------------------------------------
    # UPDATE STATUS
    # -----------------------------------------------------

    response = (
        supabase
        .table("orders")
        .update({
            "status": status
        })
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .execute()
    )

    if not response.data:
        return "Failed to update order status."

    order = response.data[0]

    return str({
        "status": "success",
        "message": "Order status updated successfully.",
        "order": {
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "product": order["product"],
            "quantity": order["quantity"],
            "total_amount": order["total_amount"],
            "status": order["status"],
            "business_id": order["business_id"]
        }
    })
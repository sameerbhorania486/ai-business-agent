from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database.db import get_connection
from auth import verify_token


router = APIRouter()

security = HTTPBearer()


# =========================================================
# AUTHENTICATION
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token."
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    supabase = get_connection()

    response = (
        supabase
        .table("users")
        .select("id, name, email, business_id")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )

    users = response.data or []

    if not users:
        raise HTTPException(
            status_code=401,
            detail="User account not found."
        )

    user = users[0]

    if user.get("business_id") is None:
        raise HTTPException(
            status_code=403,
            detail="User is not linked to a business."
        )

    return user


# =========================================================
# MAIN DASHBOARD
# =========================================================

@router.get("/dashboard")
def get_dashboard(
    current_user: dict = Depends(get_current_user)
):

    supabase = get_connection()

    business_id = current_user["business_id"]


    # =====================================================
    # TOTAL CUSTOMERS
    # =====================================================

    customers_response = (
        supabase
        .table("customers")
        .select("id", count="exact")
        .eq("business_id", business_id)
        .execute()
    )

    total_customers = customers_response.count or 0


    # =====================================================
    # TOTAL ORDERS
    # =====================================================

    orders_response = (
        supabase
        .table("orders")
        .select("order_id", count="exact")
        .eq("business_id", business_id)
        .execute()
    )

    total_orders = orders_response.count or 0


    # =====================================================
    # TOTAL REVENUE
    # =====================================================

    revenue_response = (
        supabase
        .table("orders")
        .select("total_amount")
        .eq("business_id", business_id)
        .execute()
    )

    total_revenue = 0.0

    for order in revenue_response.data or []:
        total_revenue += float(
            order.get("total_amount") or 0
        )


    # =====================================================
    # LOW STOCK PRODUCTS
    # =====================================================

    low_stock_response = (
        supabase
        .table("inventory")
        .select("product_id", count="exact")
        .eq("business_id", business_id)
        .lte("quantity", 30)
        .execute()
    )

    low_stock_products = low_stock_response.count or 0


    # =====================================================
    # TOTAL INVENTORY UNITS
    # =====================================================

    inventory_response = (
        supabase
        .table("inventory")
        .select("quantity")
        .eq("business_id", business_id)
        .execute()
    )

    total_inventory = 0

    for item in inventory_response.data or []:
        total_inventory += int(
            item.get("quantity") or 0
        )


    # =====================================================
    # RESPONSE
    # =====================================================

    return {
        "user": current_user.get("name"),
        "business_id": business_id,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "low_stock_products": low_stock_products,
        "total_inventory": total_inventory
    }


# =========================================================
# DASHBOARD ORDERS
# =========================================================

@router.get("/dashboard/orders")
def get_dashboard_orders(
    current_user: dict = Depends(get_current_user)
):

    supabase = get_connection()

    business_id = current_user["business_id"]

    response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status"
        )
        .eq("business_id", business_id)
        .order("order_id", desc=True)
        .execute()
    )

    orders = response.data or []

    return {
        "business_id": business_id,
        "total_orders": len(orders),
        "orders": orders
    }


# =========================================================
# DASHBOARD INVENTORY
# =========================================================

@router.get("/dashboard/inventory")
def get_dashboard_inventory(
    current_user: dict = Depends(get_current_user)
):

    supabase = get_connection()

    business_id = current_user["business_id"]

    response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq("business_id", business_id)
        .order("product")
        .execute()
    )

    inventory = []

    for item in response.data or []:

        quantity = int(
            item.get("quantity") or 0
        )

        inventory.append({
            "product_id": item["product_id"],
            "product": item["product"],
            "quantity": quantity,
            "price": item["price"],
            "low_stock": quantity <= 30
        })

    return {
        "business_id": business_id,
        "total_products": len(inventory),
        "inventory": inventory
    }


# =========================================================
# DASHBOARD CUSTOMERS
# =========================================================

@router.get("/dashboard/customers")
def get_dashboard_customers(
    current_user: dict = Depends(get_current_user)
):

    supabase = get_connection()

    business_id = current_user["business_id"]

    response = (
        supabase
        .table("customers")
        .select(
            "id, name, email, company, phone"
        )
        .eq("business_id", business_id)
        .order("name")
        .execute()
    )

    customers = response.data or []

    return {
        "business_id": business_id,
        "total_customers": len(customers),
        "customers": customers
    }
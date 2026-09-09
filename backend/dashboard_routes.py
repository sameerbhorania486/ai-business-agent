from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database.db import get_connection
from auth import verify_token


router = APIRouter()

security = HTTPBearer()


# =========================
# AUTHENTICATION
# =========================

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

    return payload


# =========================
# DASHBOARD
# =========================

@router.get("/dashboard")
def get_dashboard(
    current_user: dict = Depends(get_current_user)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM customers
    """)

    total_customers = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
    """)

    total_orders = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM orders
    """)

    total_revenue = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM inventory
        WHERE quantity <= 30
    """)

    low_stock_products = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM inventory
    """)

    total_inventory = cursor.fetchone()[0]

    connection.close()

    return {
        "user": current_user.get("name"),
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "low_stock_products": low_stock_products,
        "total_inventory": total_inventory
    }
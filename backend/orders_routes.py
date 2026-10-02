from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from auth import verify_token
from database.db import get_connection


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

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

    users = response.data

    if not users:
        raise HTTPException(
            status_code=401,
            detail="User account not found."
        )

    user = users[0]

    if not user.get("business_id"):
        raise HTTPException(
            status_code=403,
            detail="User is not linked to a business."
        )

    return user


# =========================================================
# REQUEST MODELS
# =========================================================

class OrderCreate(BaseModel):
    customer_id: int
    product: str
    quantity: int
    total_amount: float
    status: str = "pending"


class OrderUpdate(BaseModel):
    customer_id: int | None = None
    product: str | None = None
    quantity: int | None = None
    total_amount: float | None = None
    status: str | None = None


# =========================================================
# GET ALL ORDERS
# =========================================================

@router.get("/")
def get_orders(
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

    return {
        "business_id": business_id,
        "total_orders": len(response.data),
        "orders": response.data
    }


# =========================================================
# ADD ORDER
# =========================================================

@router.post("/")
def create_order(
    order: OrderCreate,
    current_user: dict = Depends(get_current_user)
):

    supabase = get_connection()

    business_id = current_user["business_id"]


    # -----------------------------------------------------
    # VALIDATE QUANTITY
    # -----------------------------------------------------

    if order.quantity <= 0:

        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0."
        )


    # -----------------------------------------------------
    # CHECK CUSTOMER
    # -----------------------------------------------------

    customer_response = (
        supabase
        .table("customers")
        .select("id, name")
        .eq("id", order.customer_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    if not customer_response.data:

        raise HTTPException(
            status_code=400,
            detail="Customer not found in your business."
        )


    # -----------------------------------------------------
    # GENERATE ORDER ID
    # -----------------------------------------------------
    #
    # order_id is a PRIMARY KEY, so it must be unique
    # across ALL businesses.
    #
    # Therefore, we find the highest order_id globally
    # and create the next ID.
    # -----------------------------------------------------

    existing_response = (
        supabase
        .table("orders")
        .select("order_id")
        .order("order_id", desc=True)
        .limit(1)
        .execute()
    )

    existing_orders = existing_response.data

    if existing_orders:

        new_order_id = (
            existing_orders[0]["order_id"] + 1
        )

    else:

        new_order_id = 1


    # -----------------------------------------------------
    # INSERT ORDER
    # -----------------------------------------------------

    response = (
        supabase
        .table("orders")
        .insert({
            "order_id": new_order_id,
            "customer_id": order.customer_id,
            "product": order.product.strip(),
            "quantity": order.quantity,
            "total_amount": order.total_amount,
            "status": order.status.strip().lower(),
            "business_id": business_id
        })
        .execute()
    )


    if not response.data:

        raise HTTPException(
            status_code=400,
            detail="Failed to create order."
        )


    return {
        "status": "success",
        "message": "Order created successfully.",
        "order": response.data[0]
    }


# =========================================================
# UPDATE ORDER
# =========================================================

@router.put("/{order_id}")
def update_order(
    order_id: int,
    order: OrderUpdate,
    current_user: dict = Depends(get_current_user)
):

    supabase = get_connection()

    business_id = current_user["business_id"]


    # -----------------------------------------------------
    # CHECK ORDER
    # -----------------------------------------------------

    existing_response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status"
        )
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    if not existing_response.data:

        raise HTTPException(
            status_code=404,
            detail="Order not found."
        )


    # -----------------------------------------------------
    # PREPARE UPDATE
    # -----------------------------------------------------

    updates = {}


    if order.customer_id is not None:

        customer_response = (
            supabase
            .table("customers")
            .select("id")
            .eq("id", order.customer_id)
            .eq("business_id", business_id)
            .limit(1)
            .execute()
        )

        if not customer_response.data:

            raise HTTPException(
                status_code=400,
                detail="Customer not found in your business."
            )

        updates["customer_id"] = order.customer_id


    if order.product is not None:

        if not order.product.strip():

            raise HTTPException(
                status_code=400,
                detail="Product name cannot be empty."
            )

        updates["product"] = order.product.strip()


    if order.quantity is not None:

        if order.quantity <= 0:

            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than 0."
            )

        updates["quantity"] = order.quantity


    if order.total_amount is not None:

        if order.total_amount < 0:

            raise HTTPException(
                status_code=400,
                detail="Total amount cannot be negative."
            )

        updates["total_amount"] = order.total_amount


    if order.status is not None:

        if not order.status.strip():

            raise HTTPException(
                status_code=400,
                detail="Status cannot be empty."
            )

        updates["status"] = order.status.strip().lower()


    if not updates:

        raise HTTPException(
            status_code=400,
            detail="No order information was provided to update."
        )


    # -----------------------------------------------------
    # UPDATE ORDER
    # -----------------------------------------------------

    response = (
        supabase
        .table("orders")
        .update(updates)
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .execute()
    )


    if not response.data:

        raise HTTPException(
            status_code=400,
            detail="Failed to update order."
        )


    return {
        "status": "success",
        "message": "Order updated successfully.",
        "order": response.data[0]
    }


# =========================================================
# DELETE ORDER
# =========================================================

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    current_user: dict = Depends(get_current_user)
):

    supabase = get_connection()

    business_id = current_user["business_id"]


    # -----------------------------------------------------
    # CHECK ORDER
    # -----------------------------------------------------

    existing_response = (
        supabase
        .table("orders")
        .select(
            "order_id, customer_id, product, "
            "quantity, total_amount, status"
        )
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .limit(1)
        .execute()
    )

    if not existing_response.data:

        raise HTTPException(
            status_code=404,
            detail="Order not found."
        )


    existing_order = existing_response.data[0]


    # -----------------------------------------------------
    # DELETE ORDER
    # -----------------------------------------------------

    response = (
        supabase
        .table("orders")
        .delete()
        .eq("order_id", order_id)
        .eq("business_id", business_id)
        .execute()
    )


    if not response.data:

        raise HTTPException(
            status_code=400,
            detail="Failed to delete order."
        )


    return {
        "status": "success",
        "message": "Order deleted successfully.",
        "order": existing_order
    }
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from auth import verify_token
from database.db import get_connection

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


# =========================================================
# SECURITY
# =========================================================

security = HTTPBearer()


# =========================================================
# GET CURRENT USER
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
# REQUEST MODELS
# =========================================================

class InventoryCreate(BaseModel):

    product: str = Field(
        ...,
        min_length=1
    )

    quantity: int = Field(
        ...,
        ge=0
    )

    price: float = Field(
        ...,
        ge=0
    )


class InventoryUpdate(BaseModel):

    quantity: Optional[int] = Field(
        default=None,
        ge=0
    )

    price: Optional[float] = Field(
        default=None,
        ge=0
    )


# =========================================================
# GET ALL INVENTORY
# =========================================================

@router.get("/")
def get_inventory(
    current_user: dict = Depends(get_current_user)
):

    business_id = current_user["business_id"]

    supabase = get_connection()

    response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq(
            "business_id",
            business_id
        )
        .order(
            "product_id"
        )
        .execute()
    )

    inventory = response.data or []

    return {
        "business_id": business_id,
        "total_products": len(inventory),
        "inventory": inventory
    }


# =========================================================
# SEARCH INVENTORY
# =========================================================

@router.get("/search")
def search_inventory(
    product: str,
    current_user: dict = Depends(get_current_user)
):

    business_id = current_user["business_id"]

    supabase = get_connection()

    response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq(
            "business_id",
            business_id
        )
        .ilike(
            "product",
            f"%{product}%"
        )
        .execute()
    )

    inventory = response.data or []

    return {
        "business_id": business_id,
        "total_products": len(inventory),
        "inventory": inventory
    }


# =========================================================
# ADD INVENTORY PRODUCT
# =========================================================

@router.post("/")
def create_inventory(
    request: InventoryCreate,
    current_user: dict = Depends(get_current_user)
):

    business_id = current_user["business_id"]

    product = request.product.strip()

    if not product:

        raise HTTPException(
            status_code=400,
            detail="Product name is required."
        )

    supabase = get_connection()

    # -----------------------------------------------------
    # CHECK DUPLICATE PRODUCT
    # Only inside the current business
    # -----------------------------------------------------

    existing = (
        supabase
        .table("inventory")
        .select("product_id")
        .eq(
            "business_id",
            business_id
        )
        .ilike(
            "product",
            product
        )
        .execute()
    )

    if existing.data:

        raise HTTPException(
            status_code=400,
            detail="This product already exists in your inventory."
        )

    # -----------------------------------------------------
    # GET NEXT GLOBAL PRODUCT ID
    #
    # IMPORTANT:
    # product_id is PRIMARY KEY.
    # Therefore it must be unique across ALL businesses.
    #
    # We DO NOT filter by business_id here.
    # -----------------------------------------------------

    latest = (
        supabase
        .table("inventory")
        .select("product_id")
        .order(
            "product_id",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if latest.data:

        next_product_id = (
            int(latest.data[0]["product_id"]) + 1
        )

    else:

        next_product_id = 1

    # -----------------------------------------------------
    # CREATE PRODUCT DATA
    # -----------------------------------------------------

    data = {
        "product_id": next_product_id,
        "product": product,
        "quantity": request.quantity,
        "price": request.price,
        "business_id": business_id
    }

    # -----------------------------------------------------
    # INSERT PRODUCT
    # -----------------------------------------------------

    response = (
        supabase
        .table("inventory")
        .insert(data)
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=500,
            detail="Failed to add inventory product."
        )

    # -----------------------------------------------------
    # SUCCESS RESPONSE
    # -----------------------------------------------------

    return {
        "message": "Inventory product added successfully.",
        "business_id": business_id,
        "product": response.data[0]
    }


# =========================================================
# UPDATE INVENTORY
# =========================================================

@router.put("/{product_id}")
def update_inventory(
    product_id: int,
    request: InventoryUpdate,
    current_user: dict = Depends(get_current_user)
):

    business_id = current_user["business_id"]

    supabase = get_connection()

    # -----------------------------------------------------
    # CHECK PRODUCT
    # -----------------------------------------------------

    existing = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq(
            "product_id",
            product_id
        )
        .eq(
            "business_id",
            business_id
        )
        .execute()
    )

    if not existing.data:

        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    # -----------------------------------------------------
    # BUILD UPDATE DATA
    # -----------------------------------------------------

    update_data = {}

    if request.quantity is not None:

        update_data["quantity"] = request.quantity

    if request.price is not None:

        update_data["price"] = request.price

    if not update_data:

        raise HTTPException(
            status_code=400,
            detail="Provide quantity or price to update."
        )

    # -----------------------------------------------------
    # UPDATE PRODUCT
    # -----------------------------------------------------

    response = (
        supabase
        .table("inventory")
        .update(update_data)
        .eq(
            "product_id",
            product_id
        )
        .eq(
            "business_id",
            business_id
        )
        .execute()
    )

    if not response.data:

        raise HTTPException(
            status_code=500,
            detail="Failed to update inventory."
        )

    return {
        "message": "Inventory updated successfully.",
        "business_id": business_id,
        "product": response.data[0]
    }


# =========================================================
# DELETE INVENTORY
# =========================================================

@router.delete("/{product_id}")
def delete_inventory(
    product_id: int,
    current_user: dict = Depends(get_current_user)
):

    business_id = current_user["business_id"]

    supabase = get_connection()

    # -----------------------------------------------------
    # CHECK PRODUCT
    # -----------------------------------------------------

    existing = (
        supabase
        .table("inventory")
        .select(
            "product_id"
        )
        .eq(
            "product_id",
            product_id
        )
        .eq(
            "business_id",
            business_id
        )
        .execute()
    )

    if not existing.data:

        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    # -----------------------------------------------------
    # DELETE PRODUCT
    # -----------------------------------------------------

    response = (
        supabase
        .table("inventory")
        .delete()
        .eq(
            "product_id",
            product_id
        )
        .eq(
            "business_id",
            business_id
        )
        .execute()
    )

    return {
        "message": "Inventory product deleted successfully.",
        "business_id": business_id,
        "product_id": product_id
    }


# =========================================================
# LOW STOCK
# =========================================================

@router.get("/low-stock")
def get_low_stock(
    current_user: dict = Depends(get_current_user)
):

    business_id = current_user["business_id"]

    supabase = get_connection()

    response = (
        supabase
        .table("inventory")
        .select(
            "product_id, product, quantity, price"
        )
        .eq(
            "business_id",
            business_id
        )
        .lte(
            "quantity",
            30
        )
        .order(
            "quantity"
        )
        .execute()
    )

    inventory = response.data or []

    return {
        "business_id": business_id,
        "low_stock_threshold": 30,
        "total_low_stock": len(inventory),
        "inventory": inventory
    }
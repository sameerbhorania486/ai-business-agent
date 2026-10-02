from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from auth import verify_token
from database.db import get_connection
from database.customers import (
    add_customer,
    update_customer,
    delete_customer
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
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

class CustomerCreate(BaseModel):
    name: str
    email: str = ""
    company: str = ""
    phone: str = ""


class CustomerUpdate(BaseModel):
    email: str | None = None
    company: str | None = None
    phone: str | None = None


# =========================================================
# GET CUSTOMERS
# =========================================================

@router.get("/")
def get_customers(
    current_user: dict = Depends(get_current_user)
):
    business_id = current_user["business_id"]

    supabase = get_connection()

    response = (
        supabase
        .table("customers")
        .select(
            "id, name, email, company, phone"
        )
        .eq("business_id", business_id)
        .order("id")
        .execute()
    )

    return response.data


# =========================================================
# SEARCH CUSTOMER
# =========================================================

@router.get("/search")
def search_customers(
    name: str,
    current_user: dict = Depends(get_current_user)
):
    business_id = current_user["business_id"]

    supabase = get_connection()

    response = (
        supabase
        .table("customers")
        .select(
            "id, name, email, company, phone"
        )
        .eq("business_id", business_id)
        .ilike(
            "name",
            f"%{name.strip()}%"
        )
        .order("id")
        .execute()
    )

    return response.data


# =========================================================
# ADD CUSTOMER
# =========================================================

@router.post("/")
def create_customer(
    customer: CustomerCreate,
    current_user: dict = Depends(get_current_user)
):
    business_id = current_user["business_id"]

    result = add_customer.invoke({
        "name": customer.name,
        "email": customer.email,
        "company": customer.company,
        "phone": customer.phone,
        "business_id": business_id
    })

    if "success" not in result:
        raise HTTPException(
            status_code=400,
            detail=result
        )

    return {
        "status": "success",
        "message": "Customer added successfully."
    }


# =========================================================
# UPDATE CUSTOMER
# =========================================================

@router.put("/{customer_id}")
def edit_customer(
    customer_id: int,
    customer: CustomerUpdate,
    current_user: dict = Depends(get_current_user)
):
    business_id = current_user["business_id"]

    result = update_customer.invoke({
        "customer_id": customer_id,
        "email": customer.email,
        "company": customer.company,
        "phone": customer.phone,
        "business_id": business_id
    })

    if "success" not in result:
        raise HTTPException(
            status_code=400,
            detail=result
        )

    return {
        "status": "success",
        "message": "Customer updated successfully."
    }


# =========================================================
# DELETE CUSTOMER
# =========================================================

@router.delete("/{customer_id}")
def remove_customer(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
):
    business_id = current_user["business_id"]

    result = delete_customer.invoke({
        "customer_id": customer_id,
        "business_id": business_id
    })

    if "success" not in result:
        raise HTTPException(
            status_code=400,
            detail=result
        )

    return {
        "status": "success",
        "message": "Customer deleted successfully."
    }
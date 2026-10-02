from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from database.db import get_connection
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


# =========================
# REGISTER
# =========================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    business_name: str
    phone: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name is required.")

        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip().lower()

        if not value:
            raise ValueError("Email is required.")

        if "@" not in value or "." not in value:
            raise ValueError("Please enter a valid email address.")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password is required.")

        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters long."
            )

        return value

    @field_validator("business_name")
    @classmethod
    def validate_business_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Business name is required.")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        value = value.strip()

        return value


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    email: str
    password: str


# =========================
# REGISTER USER + BUSINESS
# =========================

@router.post("/register")
def register_user(request: RegisterRequest):

    supabase = get_connection()

    email = request.email.strip().lower()

    # -------------------------
    # Check existing user
    # -------------------------

    response = (
        supabase
        .table("users")
        .select("id")
        .eq("email", email)
        .execute()
    )

    if response.data:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    # -------------------------
    # Create business
    # -------------------------

    business_response = (
        supabase
        .table("businesses")
        .insert({
            "business_name": request.business_name,
            "owner_name": request.name,
            "email": email,
            "phone": request.phone
        })
        .execute()
    )

    if not business_response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create business."
        )

    business = business_response.data[0]

    business_id = business["id"]

    # -------------------------
    # Create user
    # -------------------------

    password_hash = hash_password(request.password)

    user_response = (
        supabase
        .table("users")
        .insert({
            "name": request.name,
            "email": email,
            "password_hash": password_hash,
            "business_id": business_id
        })
        .execute()
    )

    if not user_response.data:
        raise HTTPException(
            status_code=500,
            detail="Failed to create user."
        )

    user = user_response.data[0]

    return {
        "status": "success",
        "message": "Business and user registered successfully.",
        "user_id": user["id"],
        "business_id": business_id
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
def login_user(request: LoginRequest):

    supabase = get_connection()

    email = request.email.strip().lower()

    response = (
        supabase
        .table("users")
        .select(
            "id, name, email, password_hash, business_id"
        )
        .eq("email", email)
        .execute()
    )

    users = response.data

    if not users:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    user = users[0]

    if not verify_password(
        request.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not user.get("business_id"):
        raise HTTPException(
            status_code=403,
            detail="User is not linked to a business."
        )

    token_data = {
        "user_id": user["id"],
        "email": user["email"],
        "name": user["name"]
    }

    access_token = create_access_token(
        token_data
    )

    return {
        "status": "success",
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer"
    }
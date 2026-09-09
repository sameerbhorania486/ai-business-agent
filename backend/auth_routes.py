from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator

from database.db import get_connection
from auth import hash_password, verify_password, create_access_token


router = APIRouter()


# =========================
# REQUEST MODELS
# =========================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

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


class LoginRequest(BaseModel):
    email: str
    password: str


# =========================
# REGISTER
# =========================

@router.post("/register")
def register_user(request: RegisterRequest):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (request.email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    password_hash = hash_password(
        request.password
    )

    cursor.execute(
        """
        INSERT INTO users
        (name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (
            request.name,
            request.email,
            password_hash
        )
    )

    connection.commit()
    connection.close()

    return {
        "status": "success",
        "message": "User registered successfully."
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
def login_user(request: LoginRequest):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            password_hash
        FROM users
        WHERE email = ?
        """,
        (request.email.strip().lower(),)
    )

    user = cursor.fetchone()

    connection.close()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    user_id, name, email, password_hash = user

    if not verify_password(
        request.password,
        password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token_data = {
        "user_id": user_id,
        "email": email,
        "name": name
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
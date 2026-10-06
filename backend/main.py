from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.agent import run_agent
from auth import verify_token
from database.db import get_connection

from backend.auth_routes import router as auth_router
from backend.dashboard_routes import router as dashboard_router
from backend.customers_routes import router as customer_router
from backend.orders_routes import router as order_router
from backend.inventory_routes import router as inventory_router


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AI Business Agent",
    description="AI-powered business automation backend",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-business-agent-html-frontend-9qsxutube-sameerbhorania486.vercel.app"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# =========================================================
# SECURITY
# =========================================================

security = HTTPBearer()


# =========================================================
# CHAT REQUEST
# =========================================================

class ChatRequest(BaseModel):

    message: str


# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth_router)

app.include_router(dashboard_router)

app.include_router(customer_router)

app.include_router(order_router)

app.include_router(inventory_router)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "status": "success",
        "message": "AI Business Agent API is running",
        "version": "1.0.0"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Business Agent API"
    }


# =========================================================
# GET CURRENT AUTHENTICATED USER
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
        .select(
            "id, name, email, business_id"
        )
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
# CHAT
# =========================================================

@app.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):

    business_id = current_user["business_id"]

    response = run_agent(
        request.message,
        business_id
    )

    return {
        "user": current_user.get("name"),
        "business_id": business_id,
        "message": request.message,
        "response": response
    }
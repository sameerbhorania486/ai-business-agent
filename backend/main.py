from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from agents.agent import run_agent
from auth import verify_token
from backend.auth_routes import router as auth_router
from backend.dashboard_routes import router as dashboard_router


app = FastAPI(
    title="AI Business Agent",
    description="AI-powered business automation backend",
    version="1.0.0"
)


# JWT Bearer authentication
security = HTTPBearer()


class ChatRequest(BaseModel):
    message: str


app.include_router(auth_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "AI Business Agent API is running"
    }


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


@app.post("/chat")
def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    response = run_agent(request.message)

    return {
        "user": current_user.get("name"),
        "message": request.message,
        "response": response
    }
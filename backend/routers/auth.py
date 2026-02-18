from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import database

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    tenant_name: str
    role: str = "user"


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[dict] = None


@router.post("/login", response_model=TokenResponse)
def login_for_access_token(body: LoginRequest):
    user = next((u for u in database.USERS if u["username"] == body.username), None)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    tenant = database.TENANTS.get(user["tenant_id"], {})
    tenant_name = tenant.get("name", user["tenant_id"])

    return TokenResponse(
        access_token=body.username,
        user={
            "username": user["username"],
            "tenant_id": user["tenant_id"],
            "tenant_name": tenant_name,
            "role": user["role"],
        },
    )


@router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest):
    if any(u["username"] == body.username for u in database.USERS):
        raise HTTPException(status_code=400, detail="Username already exists")
    if len(body.password.strip()) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters")
    
    tenant_id = f"tenant_{body.username}"
    database.TENANTS[tenant_id] = {"name": body.tenant_name}
    
    new_user = {
        "username": body.username,
        "password": body.password,
        "role": body.role,
        "tenant_id": tenant_id,
    }
    database.USERS.append(new_user)
    database.CHANNEL_CONNECTIONS[tenant_id] = []
    
    return TokenResponse(
        access_token=body.username,
        user={
            "username": body.username,
            "tenant_id": tenant_id,
            "tenant_name": body.tenant_name,
            "role": body.role,
        },
    )


@router.post("/change-password")
def change_password(body: ChangePasswordRequest, current_user=Depends(get_current_user)):
    if current_user["password"] != body.current_password:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if not body.new_password or len(body.new_password.strip()) < 4:
        raise HTTPException(status_code=400, detail="New password must be at least 4 characters")
    current_user["password"] = body.new_password.strip()
    return {"message": "Password updated successfully"}

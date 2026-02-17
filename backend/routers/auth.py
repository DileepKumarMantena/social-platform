from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import database

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


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

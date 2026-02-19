from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import database
import random
import string
from datetime import datetime, timezone, timedelta
from constants import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, TWO_FA_ENABLED, TWO_FA_CODE_LENGTH, TWO_FA_CODE_EXPIRE_MINUTES, MSG_LOGIN_SUCCESS, MSG_LOGIN_FAILED, MSG_2FA_REQUIRED, MSG_2FA_INVALID, MSG_UNAUTHORIZED

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


class TwoFactorVerifyRequest(BaseModel):
    username: str
    password: str
    two_factor_code: str


class TwoFactorEnableRequest(BaseModel):
    enable: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[dict] = None
    requires_two_factor: Optional[bool] = False


class TwoFactorResponse(BaseModel):
    success: bool
    message: str
    temp_token: Optional[str] = None


def generate_2fa_code():
    """Generate a 2FA code"""
    return ''.join(random.choices(string.digits, k=TWO_FA_CODE_LENGTH))


def is_2fa_enabled(username: str):
    """Check if 2FA is enabled for user (demo: enabled for admin users)"""
    user = next((u for u in database.USERS if u["username"] == username), None)
    return user and user.get("role") == "admin"


@router.post("/login/step1", response_model=TokenResponse)
def login_step1(body: LoginRequest):
    """Direct login - no 2FA required"""
    user = next((u for u in database.USERS if u["username"] == body.username), None)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
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
        requires_two_factor=False
    )


@router.post("/create-tenant", response_model=dict)
def create_tenant(body: dict):
    """Super admin creates a new tenant/customer"""
    # Check if user is super admin
    # In real app, verify token and role
    tenant_counter = len(database.TENANTS) + 1
    tenant_id = f"tenant_{tenant_counter:04d}"
    new_tenant = {
        "id": tenant_id,
        "name": body.get("name"),
        "status": "active",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    # Add to tenants (in real app, save to database)
    database.TENANTS[tenant_id] = new_tenant
    
    return {"success": True, "tenant_id": tenant_id, "message": "Tenant created successfully"}


@router.post("/create-user", response_model=dict)
def create_user(body: dict):
    """Lead creates admin/user within their tenant"""
    # Check if user is lead role
    # In real app, verify token and role
    
    user_counter = len(database.USERS) + 1
    user_id = f"user_{user_counter:04d}"
    expires_at = None
    
    # Set expiration for admin users if specified
    if body.get("role") == "admin" and body.get("access_days"):
        from datetime import timedelta
        expires_at = (datetime.now(timezone.utc) + timedelta(days=body.get("access_days"))).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    new_user = {
        "username": body.get("username"),
        "password": body.get("password"),
        "role": body.get("role"),
        "tenant_id": body.get("tenant_id"),
        "expires_at": expires_at
    }
    
    # Add to users (in real app, save to database)
    database.USERS.append(new_user)
    
    return {"success": True, "user_id": user_id, "expires_at": expires_at, "message": "User created successfully"}


@router.post("/login", response_model=TokenResponse)
def login_for_access_token(body: LoginRequest):
    """Direct login endpoint - no 2FA required"""
    user = next((u for u in database.USERS if u["username"] == body.username), None)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check if admin user has expired
    if user.get("role") == "admin" and user.get("expires_at"):
        from datetime import datetime, timezone
        expires_at = datetime.fromisoformat(user["expires_at"].replace('Z', '+00:00'))
        if datetime.now(timezone.utc) > expires_at:
            raise HTTPException(status_code=401, detail="Admin access has expired")
    
    tenant = database.TENANTS.get(user["tenant_id"], {})
    tenant_name = tenant.get("name", user["tenant_id"])
    
    return TokenResponse(
        access_token=body.username,
        user={
            "username": user["username"],
            "tenant_id": user["tenant_id"],
            "tenant_name": tenant_name,
            "role": user["role"],
            "expires_at": user.get("expires_at")
        },
        requires_two_factor=False
    )



    

@router.post("/change-password")
def change_password(body: ChangePasswordRequest, current_user=Depends(get_current_user)):
    if current_user["password"] != body.current_password:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if not body.new_password or len(body.new_password.strip()) < 4:
        raise HTTPException(status_code=400, detail="New password must be at least 4 characters")
    current_user["password"] = body.new_password.strip()
    return {"message": "Password updated successfully"}

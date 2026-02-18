from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import database
import random
import string
from datetime import datetime, timezone, timedelta

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
    """Generate a 6-digit 2FA code"""
    return ''.join(random.choices(string.digits, k=6))


def is_2fa_enabled(username: str):
    """Check if 2FA is enabled for user (demo: enabled for admin users)"""
    user = next((u for u in database.USERS if u["username"] == username), None)
    return user and user.get("role") == "admin"


@router.post("/login/step1", response_model=TwoFactorResponse)
def login_step1(body: LoginRequest):
    """First step of login - validate credentials and issue 2FA if needed"""
    user = next((u for u in database.USERS if u["username"] == body.username), None)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Check if 2FA is enabled for this user
    if is_2fa_enabled(body.username):
        # Generate 2FA code
        code = generate_2fa_code()
        temp_token = f"temp_{body.username}_{random.randint(1000, 9999)}"
        
        # Store the 2FA code (in real app, this would be sent via SMS/email)
        database.TWO_FA_TOKENS[temp_token] = {
            "username": body.username,
            "code": code,
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        return TwoFactorResponse(
            success=True,
            message=f"2FA code sent: {code} (Demo: code shown in response)",
            temp_token=temp_token
        )
    else:
        # No 2FA required, return regular token
        tenant = database.TENANTS.get(user["tenant_id"], {})
        tenant_name = tenant.get("name", user["tenant_id"])
        
        return TwoFactorResponse(
            success=True,
            message="Login successful",
            temp_token=body.username  # Use username as token for non-2FA users
        )


@router.post("/login/step2", response_model=TokenResponse)
def login_step2(body: TwoFactorVerifyRequest):
    """Second step of login - verify 2FA code"""
    user = next((u for u in database.USERS if u["username"] == body.username), None)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # For non-2FA users, just return token
    if not is_2fa_enabled(body.username):
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
    
    # For 2FA users, verify the code (demo: accept any 6-digit code)
    if len(body.two_factor_code) != 6 or not body.two_factor_code.isdigit():
        raise HTTPException(status_code=400, detail="Invalid 2FA code format")
    
    # In demo, we'll accept any valid 6-digit code
    # In real app, you'd verify against stored code
    
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
        requires_two_factor=True
    )


@router.post("/login", response_model=TokenResponse)
def login_for_access_token(body: LoginRequest):
    """Legacy login endpoint for backward compatibility"""
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
        requires_two_factor=is_2fa_enabled(body.username)
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

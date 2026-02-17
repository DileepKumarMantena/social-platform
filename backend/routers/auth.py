from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import database

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login_for_access_token(body: LoginRequest):
    user = next((u for u in database.USERS if u["username"] == body.username), None)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # token is username
    return TokenResponse(access_token=body.username)
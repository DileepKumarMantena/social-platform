from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import database
from typing import List
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user

class Lead(BaseModel):
    id: int
    name: str
    email: str

@router.get("/leads", response_model=List[Lead])
def get_leads(current_user=Depends(get_current_user)):
    return database.LEADS
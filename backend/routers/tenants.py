from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import database

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user


@router.get("/tenants")
def get_tenants(current_user=Depends(get_current_user)):
    return [{"id": tid, "name": t.get("name", tid)} for tid, t in database.TENANTS.items()]

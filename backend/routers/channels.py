from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import database

router = APIRouter()
security = HTTPBearer()  # Swagger lock

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user

@router.get("/channels")
def get_channels(current_user=Depends(get_current_user)):
    return database.CHANNELS

@router.post("/channels/toggle")
def toggle_channel(channel_id: int, current_user=Depends(get_current_user)):
    for ch in database.CHANNELS:
        if ch["id"] == channel_id:
            ch["enabled"] = not ch.get("enabled", False)
            return {"message": "Channel updated", "channel": ch}
    raise HTTPException(status_code=404, detail="Channel not found")
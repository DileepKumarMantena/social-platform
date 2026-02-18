from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import database

router = APIRouter()
security = HTTPBearer()


class ToggleChannelBody(BaseModel):
    channel_id: int


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user


def require_role(allowed_roles: list):
    def check_role(current_user=Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return check_role


@router.get("/channels")
def get_channels(current_user=Depends(get_current_user)):
    tenant_id = current_user.get("tenant_id", "")
    connected_ids = set(database.CHANNEL_CONNECTIONS.get(tenant_id, []))

    return [
        {
            **ch,
            "connected": ch["id"] in connected_ids,
            "active": ch["id"] in connected_ids,
        }
        for ch in database.CHANNELS
    ]


@router.post("/channels/toggle")
def toggle_channel(body: ToggleChannelBody, current_user=Depends(require_role(["admin", "lead"]))):
    channel_id = body.channel_id
    channel = next((c for c in database.CHANNELS if c["id"] == channel_id), None)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    tenant_id = current_user.get("tenant_id", "")
    if tenant_id not in database.CHANNEL_CONNECTIONS:
        database.CHANNEL_CONNECTIONS[tenant_id] = []

    conn = database.CHANNEL_CONNECTIONS[tenant_id]
    if channel_id in conn:
        conn.remove(channel_id)
    else:
        conn.append(channel_id)

    connected = channel_id in database.CHANNEL_CONNECTIONS.get(tenant_id, [])
    return {
        "message": "Connected" if connected else "Disconnected",
        "channel": {**channel, "connected": connected, "active": connected},
    }

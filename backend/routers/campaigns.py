from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import database
from typing import Optional

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user

class CampaignCreate(BaseModel):
    name: str
    channel_id: int
    budget: Optional[float] = 0.0

@router.get("/campaigns")
def get_campaigns(current_user=Depends(get_current_user)):
    return database.CAMPAIGNS

@router.post("/campaigns")
def create_campaign(body: CampaignCreate, current_user=Depends(get_current_user)):
    channel = next((c for c in database.CHANNELS if c["id"] == body.channel_id), None)
    if not channel:
        raise HTTPException(status_code=400, detail="Invalid channel_id")
    new_id = max([c.get("id", 0) for c in database.CAMPAIGNS], default=0) + 1
    campaign = {
        "id": new_id,
        "name": body.name,
        "channel_id": body.channel_id,
        "channel_name": channel["name"],
        "budget": float(body.budget or 0.0),
    }
    database.CAMPAIGNS.append(campaign)
    return {"message": "Campaign created", "campaign": campaign}
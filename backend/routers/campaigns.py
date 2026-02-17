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
    tenant_id = current_user.get("tenant_id", "")
    return [c for c in database.CAMPAIGNS if c.get("tenant_id") == tenant_id]


@router.post("/campaigns")
def create_campaign(body: CampaignCreate, current_user=Depends(get_current_user)):
    channel = next((c for c in database.CHANNELS if c["id"] == body.channel_id), None)
    if not channel:
        raise HTTPException(status_code=400, detail="Invalid channel_id")

    tenant_id = current_user.get("tenant_id", "")
    tenant = database.TENANTS.get(tenant_id, {})
    tenant_name = tenant.get("name", tenant_id)

    new_id = max([c.get("id", 0) for c in database.CAMPAIGNS], default=0) + 1
    campaign = {
        "id": new_id,
        "name": body.name,
        "channel_id": body.channel_id,
        "channel_name": channel["name"],
        "channel_slug": channel.get("slug", ""),
        "budget": float(body.budget or 0.0),
        "status": "active",
        "tenant_id": tenant_id,
        "tenant_name": tenant_name,
    }
    database.CAMPAIGNS.append(campaign)
    return {"message": "Campaign created", "campaign": campaign}


@router.get("/campaigns/stats")
def get_campaign_stats(current_user=Depends(get_current_user)):
    tenant_id = current_user.get("tenant_id", "")
    campaigns = [c for c in database.CAMPAIGNS if c.get("tenant_id") == tenant_id]
    return {
        "total": len(campaigns),
        "active": len([c for c in campaigns if c.get("status") == "active"]),
        "draft": len([c for c in campaigns if c.get("status") == "draft"]),
    }

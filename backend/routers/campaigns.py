from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import database
from typing import Optional
from datetime import datetime, timezone

router = APIRouter()
security = HTTPBearer()


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


class CampaignCreate(BaseModel):
    name: str
    channel_id: int
    budget: Optional[float] = 0.0


class CampaignComment(BaseModel):
    comment: str


class CampaignApproval(BaseModel):
    approved: bool
    notes: Optional[str] = ""


@router.get("/campaigns")
def get_campaigns(current_user=Depends(get_current_user)):
    tenant_id = current_user.get("tenant_id", "")
    return [c for c in database.CAMPAIGNS if c.get("tenant_id") == tenant_id]


@router.post("/campaigns")
def create_campaign(body: CampaignCreate, current_user=Depends(require_role(["admin", "lead"]))):
    channel = next((c for c in database.CHANNELS if c["id"] == body.channel_id), None)
    if not channel:
        raise HTTPException(status_code=400, detail="Invalid channel_id")

    tenant_id = current_user.get("tenant_id", "")
    tenant = database.TENANTS.get(tenant_id, {})
    tenant_name = tenant.get("name", tenant_id)

    new_id = max([c.get("id", 0) for c in database.CAMPAIGNS], default=0) + 1
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    campaign = {
        "id": new_id,
        "name": body.name,
        "channel_id": body.channel_id,
        "channel_name": channel["name"],
        "channel_slug": channel.get("slug", ""),
        "budget": float(body.budget or 0.0),
        "status": "pending_approval",  # New campaigns start as pending
        "tenant_id": tenant_id,
        "tenant_name": tenant_name,
        "created_at": created_at,
        "created_by": current_user.get("username"),
        "approved_by": None,
        "approved_at": None,
    }
    database.CAMPAIGNS.append(campaign)
    
    # Log activity
    activity_log = {
        "id": len(database.ACTIVITY_LOGS) + 1,
        "tenant_id": tenant_id,
        "user_id": current_user.get("username"),
        "action": "created",
        "entity_type": "campaign",
        "entity_id": new_id,
        "timestamp": created_at
    }
    database.ACTIVITY_LOGS.append(activity_log)
    
    return {"message": "Campaign created and pending approval", "campaign": campaign}


@router.get("/campaigns/stats")
def get_campaign_stats(current_user=Depends(get_current_user)):
    tenant_id = current_user.get("tenant_id", "")
    campaigns = [c for c in database.CAMPAIGNS if c.get("tenant_id") == tenant_id]
    return {
        "total": len(campaigns),
        "active": len([c for c in campaigns if c.get("status") == "active"]),
        "draft": len([c for c in campaigns if c.get("status") == "draft"]),
        "pending_approval": len([c for c in campaigns if c.get("status") == "pending_approval"]),
    }


@router.get("/campaigns/{campaign_id}/comments")
def get_campaign_comments(campaign_id: int, current_user=Depends(get_current_user)):
    """Get all comments for a specific campaign"""
    tenant_id = current_user.get("tenant_id", "")
    
    # Verify campaign belongs to tenant
    campaign = next((c for c in database.CAMPAIGNS if c.get("id") == campaign_id and c.get("tenant_id") == tenant_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get comments for this campaign
    comments = [c for c in database.CAMPAIGN_COMMENTS if c.get("campaign_id") == campaign_id and c.get("tenant_id") == tenant_id]
    
    # Enrich with user information
    enriched_comments = []
    for comment in comments:
        user_info = next((u for u in database.USERS if u["username"] == comment.get("user_id")), None)
        enriched_comments.append({
            "id": comment.get("id"),
            "user_id": comment.get("user_id"),
            "user_role": user_info.get("role", "unknown") if user_info else "unknown",
            "comment": comment.get("comment"),
            "timestamp": comment.get("timestamp")
        })
    
    # Sort by timestamp
    enriched_comments.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return {"comments": enriched_comments}


@router.post("/campaigns/{campaign_id}/comments")
def add_campaign_comment(campaign_id: int, body: CampaignComment, current_user=Depends(get_current_user)):
    """Add a comment to a campaign"""
    tenant_id = current_user.get("tenant_id", "")
    
    # Verify campaign belongs to tenant
    campaign = next((c for c in database.CAMPAIGNS if c.get("id") == campaign_id and c.get("tenant_id") == tenant_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    new_comment = {
        "id": len(database.CAMPAIGN_COMMENTS) + 1,
        "campaign_id": campaign_id,
        "tenant_id": tenant_id,
        "user_id": current_user.get("username"),
        "comment": body.comment,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    database.CAMPAIGN_COMMENTS.append(new_comment)
    
    # Log activity
    activity_log = {
        "id": len(database.ACTIVITY_LOGS) + 1,
        "tenant_id": tenant_id,
        "user_id": current_user.get("username"),
        "action": "commented",
        "entity_type": "campaign",
        "entity_id": campaign_id,
        "timestamp": new_comment["timestamp"]
    }
    database.ACTIVITY_LOGS.append(activity_log)
    
    return {"message": "Comment added", "comment": new_comment}


@router.post("/campaigns/{campaign_id}/approve")
def approve_campaign(campaign_id: int, body: CampaignApproval, current_user=Depends(require_role(["admin"]))):
    """Approve or reject a campaign (admin only)"""
    tenant_id = current_user.get("tenant_id", "")
    
    # Verify campaign belongs to tenant
    campaign = next((c for c in database.CAMPAIGNS if c.get("id") == campaign_id and c.get("tenant_id") == tenant_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if campaign.get("status") != "pending_approval":
        raise HTTPException(status_code=400, detail="Campaign is not pending approval")
    
    approval_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Update campaign status
    campaign["status"] = "active" if body.approved else "rejected"
    campaign["approved_by"] = current_user.get("username")
    campaign["approved_at"] = approval_time
    
    # Log activity
    action = "approved" if body.approved else "rejected"
    activity_log = {
        "id": len(database.ACTIVITY_LOGS) + 1,
        "tenant_id": tenant_id,
        "user_id": current_user.get("username"),
        "action": action,
        "entity_type": "campaign",
        "entity_id": campaign_id,
        "timestamp": approval_time
    }
    database.ACTIVITY_LOGS.append(activity_log)
    
    # Add approval comment if notes provided
    if body.notes:
        approval_comment = {
            "id": len(database.CAMPAIGN_COMMENTS) + 1,
            "campaign_id": campaign_id,
            "tenant_id": tenant_id,
            "user_id": current_user.get("username"),
            "comment": f"Campaign {action}: {body.notes}",
            "timestamp": approval_time
        }
        database.CAMPAIGN_COMMENTS.append(approval_comment)
    
    return {"message": f"Campaign {action}", "campaign": campaign}


@router.get("/campaigns/pending-approval")
def get_pending_approval_campaigns(current_user=Depends(require_role(["admin"]))):
    """Get all campaigns pending approval (admin only)"""
    tenant_id = current_user.get("tenant_id", "")
    
    pending_campaigns = [c for c in database.CAMPAIGNS 
                         if c.get("tenant_id") == tenant_id and c.get("status") == "pending_approval"]
    
    return {"pending_campaigns": pending_campaigns}

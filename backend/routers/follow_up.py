from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import database
from typing import Optional, List
from datetime import datetime, timezone, timedelta
import random

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user


class FollowUpCreate(BaseModel):
    lead_id: int
    type: str  # "email" or "sms"
    message: str
    scheduled_at: Optional[str] = None  # ISO datetime string


class FollowUpTemplate(BaseModel):
    name: str
    type: str  # "email" or "sms"
    subject: Optional[str] = None  # for email
    message: str


# Demo follow-up templates
FOLLOW_UP_TEMPLATES = [
    {
        "id": 1,
        "name": "Welcome Email",
        "type": "email",
        "subject": "Welcome to our platform!",
        "message": "Hi {lead_name}, thank you for your interest! We're excited to help you get started."
    },
    {
        "id": 2,
        "name": "Quick Follow-up SMS",
        "type": "sms",
        "message": "Hi {lead_name}, just checking in about your inquiry. Let us know if you have questions!"
    },
    {
        "id": 3,
        "name": "Product Information",
        "type": "email",
        "subject": "More Information About Our Services",
        "message": "Hi {lead_name}, here's more detailed information about how our platform can help your business."
    }
]


@router.get("/follow-up/templates")
def get_follow_up_templates(current_user=Depends(get_current_user)):
    """Get available follow-up templates"""
    return {"templates": FOLLOW_UP_TEMPLATES}


@router.post("/follow-up/create")
def create_follow_up(body: FollowUpCreate, current_user=Depends(get_current_user)):
    """Create a new follow-up sequence"""
    tenant_id = current_user.get("tenant_id", "")
    
    # Verify lead belongs to tenant
    lead = next((l for l in database.LEADS if l.get("id") == body.lead_id and l.get("tenant_id") == tenant_id), None)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Set default schedule time if not provided
    if body.scheduled_at:
        scheduled_at = body.scheduled_at
    else:
        # Default to 2 hours from now
        scheduled_at = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    new_follow_up = {
        "id": len(database.FOLLOW_UP_SEQUENCES) + 1,
        "tenant_id": tenant_id,
        "lead_id": body.lead_id,
        "type": body.type,
        "status": "pending",
        "scheduled_at": scheduled_at,
        "message": body.message,
        "created_by": current_user.get("username"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    database.FOLLOW_UP_SEQUENCES.append(new_follow_up)
    
    return {"message": "Follow-up created", "follow_up": new_follow_up}


@router.get("/follow-up/list")
def get_follow_ups(current_user=Depends(get_current_user)):
    """Get all follow-ups for the current tenant"""
    tenant_id = current_user.get("tenant_id", "")
    
    follow_ups = [f for f in database.FOLLOW_UP_SEQUENCES if f.get("tenant_id") == tenant_id]
    
    # Enrich with lead information
    enriched_follow_ups = []
    for follow_up in follow_ups:
        lead = next((l for l in database.LEADS if l.get("id") == follow_up.get("lead_id")), None)
        enriched_follow_ups.append({
            "id": follow_up.get("id"),
            "lead_id": follow_up.get("lead_id"),
            "lead_name": lead.get("name") if lead else "Unknown",
            "lead_email": lead.get("email") if lead else "Unknown",
            "type": follow_up.get("type"),
            "status": follow_up.get("status"),
            "scheduled_at": follow_up.get("scheduled_at"),
            "message": follow_up.get("message"),
            "created_at": follow_up.get("created_at")
        })
    
    # Sort by scheduled time
    enriched_follow_ups.sort(key=lambda x: x.get("scheduled_at", ""))
    
    return {"follow_ups": enriched_follow_ups}


@router.post("/follow-up/{follow_up_id}/send")
def send_follow_up_now(follow_up_id: int, current_user=Depends(get_current_user)):
    """Send a follow-up immediately (demo)"""
    tenant_id = current_user.get("tenant_id", "")
    
    # Find the follow-up
    follow_up = next((f for f in database.FOLLOW_UP_SEQUENCES 
                     if f.get("id") == follow_up_id and f.get("tenant_id") == tenant_id), None)
    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    
    # Update status to sent
    follow_up["status"] = "sent"
    follow_up["sent_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    follow_up["sent_by"] = current_user.get("username")
    
    # Get lead info for demo
    lead = next((l for l in database.LEADS if l.get("id") == follow_up.get("lead_id")), None)
    
    # Simulate sending (in real app, this would integrate with email/SMS service)
    success_rate = 0.95  # 95% success rate for demo
    success = random.random() < success_rate
    
    if success:
        return {
            "message": f"{follow_up['type'].title()} sent successfully",
            "follow_up": follow_up,
            "sent_to": {
                "name": lead.get("name") if lead else "Unknown",
                "email": lead.get("email") if lead else "Unknown"
            }
        }
    else:
        follow_up["status"] = "failed"
        return {
            "message": f"Failed to send {follow_up['type']}",
            "follow_up": follow_up,
            "error": "Simulated delivery failure"
        }


@router.post("/follow-up/{follow_up_id}/cancel")
def cancel_follow_up(follow_up_id: int, current_user=Depends(get_current_user)):
    """Cancel a pending follow-up"""
    tenant_id = current_user.get("tenant_id", "")
    
    follow_up = next((f for f in database.FOLLOW_UP_SEQUENCES 
                     if f.get("id") == follow_up_id and f.get("tenant_id") == tenant_id), None)
    if not follow_up:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    
    if follow_up.get("status") != "pending":
        raise HTTPException(status_code=400, detail="Cannot cancel follow-up that is not pending")
    
    follow_up["status"] = "cancelled"
    follow_up["cancelled_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    follow_up["cancelled_by"] = current_user.get("username")
    
    return {"message": "Follow-up cancelled", "follow_up": follow_up}


@router.get("/follow-up/stats")
def get_follow_up_stats(current_user=Depends(get_current_user)):
    """Get follow-up statistics"""
    tenant_id = current_user.get("tenant_id", "")
    
    follow_ups = [f for f in database.FOLLOW_UP_SEQUENCES if f.get("tenant_id") == tenant_id]
    
    stats = {
        "total": len(follow_ups),
        "pending": len([f for f in follow_ups if f.get("status") == "pending"]),
        "sent": len([f for f in follow_ups if f.get("status") == "sent"]),
        "failed": len([f for f in follow_ups if f.get("status") == "failed"]),
        "cancelled": len([f for f in follow_ups if f.get("status") == "cancelled"]),
        "by_type": {
            "email": len([f for f in follow_ups if f.get("type") == "email"]),
            "sms": len([f for f in follow_ups if f.get("type") == "sms"])
        }
    }
    
    return {"stats": stats}


@router.post("/follow-up/bulk-create")
def create_bulk_follow_ups(body: dict, current_user=Depends(get_current_user)):
    """Create follow-ups for multiple leads at once"""
    tenant_id = current_user.get("tenant_id", "")
    lead_ids = body.get("lead_ids", [])
    template_id = body.get("template_id", 1)
    custom_message = body.get("message", "")
    follow_up_type = body.get("type", "email")
    
    # Get template
    template = next((t for t in FOLLOW_UP_TEMPLATES if t.get("id") == template_id), None)
    if not template and not custom_message:
        raise HTTPException(status_code=400, detail="Template not found and no custom message provided")
    
    created_follow_ups = []
    for lead_id in lead_ids:
        # Verify lead belongs to tenant
        lead = next((l for l in database.LEADS if l.get("id") == lead_id and l.get("tenant_id") == tenant_id), None)
        if not lead:
            continue
        
        # Use template or custom message
        message = custom_message
        if template:
            message = template.get("message", "").replace("{lead_name}", lead.get("name", "Valued Customer"))
        
        # Create follow-up
        new_follow_up = {
            "id": len(database.FOLLOW_UP_SEQUENCES) + 1,
            "tenant_id": tenant_id,
            "lead_id": lead_id,
            "type": follow_up_type,
            "status": "pending",
            "scheduled_at": (datetime.now(timezone.utc) + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "message": message,
            "created_by": current_user.get("username"),
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        database.FOLLOW_UP_SEQUENCES.append(new_follow_up)
        created_follow_ups.append(new_follow_up)
    
    return {
        "message": f"Created {len(created_follow_ups)} follow-ups",
        "follow_ups": created_follow_ups
    }

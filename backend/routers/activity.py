from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import database
from typing import Optional, List
from datetime import datetime, timezone

router = APIRouter()
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user


@router.get("/activity/logs")
def get_activity_logs(current_user=Depends(get_current_user)):
    """Get team activity logs for the current tenant"""
    tenant_id = current_user.get("tenant_id", "")
    
    # Filter activity logs for current tenant
    tenant_logs = [log for log in database.ACTIVITY_LOGS if log.get("tenant_id") == tenant_id]
    
    # Sort by timestamp (most recent first)
    tenant_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Enrich with user and entity information
    enriched_logs = []
    for log in tenant_logs:
        user_info = next((u for u in database.USERS if u["username"] == log.get("user_id")), None)
        
        # Get entity details
        entity_details = {}
        entity_type = log.get("entity_type")
        entity_id = log.get("entity_id")
        
        if entity_type == "campaign":
            campaign = next((c for c in database.CAMPAIGNS if c.get("id") == entity_id), None)
            if campaign:
                entity_details = {
                    "name": campaign.get("name", "Unknown"),
                    "status": campaign.get("status", "unknown")
                }
        
        enriched_logs.append({
            "id": log.get("id"),
            "user": {
                "username": log.get("user_id"),
                "role": user_info.get("role", "unknown") if user_info else "unknown"
            },
            "action": log.get("action"),
            "entity_type": entity_type,
            "entity_id": entity_id,
            "entity_details": entity_details,
            "timestamp": log.get("timestamp")
        })
    
    return {"activity_logs": enriched_logs}


@router.post("/activity/log")
def log_activity(body: dict, current_user=Depends(get_current_user)):
    """Log a new activity (internal use)"""
    tenant_id = current_user.get("tenant_id", "")
    
    new_log = {
        "id": len(database.ACTIVITY_LOGS) + 1,
        "tenant_id": tenant_id,
        "user_id": current_user.get("username"),
        "action": body.get("action"),
        "entity_type": body.get("entity_type"),
        "entity_id": body.get("entity_id"),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    database.ACTIVITY_LOGS.append(new_log)
    return {"message": "Activity logged", "log": new_log}


@router.get("/activity/stats")
def get_activity_stats(current_user=Depends(get_current_user)):
    """Get activity statistics for the current tenant"""
    tenant_id = current_user.get("tenant_id", "")
    
    tenant_logs = [log for log in database.ACTIVITY_LOGS if log.get("tenant_id") == tenant_id]
    
    # Count by action type
    action_counts = {}
    for log in tenant_logs:
        action = log.get("action", "unknown")
        action_counts[action] = action_counts.get(action, 0) + 1
    
    # Count by user
    user_counts = {}
    for log in tenant_logs:
        user = log.get("user_id", "unknown")
        user_counts[user] = user_counts.get(user, 0) + 1
    
    # Count by entity type
    entity_counts = {}
    for log in tenant_logs:
        entity = log.get("entity_type", "unknown")
        entity_counts[entity] = entity_counts.get(entity, 0) + 1
    
    # Recent activity (last 7 days)
    recent_logs = [log for log in tenant_logs if log.get("timestamp", "")][:10]
    
    return {
        "stats": {
            "total_activities": len(tenant_logs),
            "by_action": action_counts,
            "by_user": user_counts,
            "by_entity_type": entity_counts,
            "recent_activities": recent_logs
        }
    }

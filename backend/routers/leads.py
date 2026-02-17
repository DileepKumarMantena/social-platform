from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import database

router = APIRouter()
security = HTTPBearer()

VALID_STATUSES = ["new", "contacted", "qualified", "won", "lost"]


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = next((u for u in database.USERS if u["username"] == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token/user")
    return user


class LeadStatusUpdate(BaseModel):
    status: str


@router.get("/leads")
def get_leads(current_user=Depends(get_current_user), tenant_id: str = None):
    user_tenant = current_user.get("tenant_id", "")
    role = current_user.get("role", "")

    leads = database.LEADS
    if tenant_id and role in ("admin", "sales"):
        filtered = [l for l in leads if l.get("tenant_id") == tenant_id]
    else:
        filtered = [l for l in leads if l.get("tenant_id") == user_tenant]

    # Add tenant_name for display
    result = []
    for l in filtered:
        tid = l.get("tenant_id", "")
        tn = database.TENANTS.get(tid, {}).get("name", tid)
        result.append({**l, "tenant_name": tn})
    return result


@router.post("/leads/{lead_id}/status")
def update_lead_status(lead_id: int, body: LeadStatusUpdate, current_user=Depends(get_current_user)):
    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Use: {VALID_STATUSES}")

    lead = next((l for l in database.LEADS if l["id"] == lead_id), None)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    user_tenant = current_user.get("tenant_id", "")
    if lead.get("tenant_id") != user_tenant:
        raise HTTPException(status_code=403, detail="Not authorized for this lead")

    lead["status"] = body.status
    return {"message": "Lead updated", "lead": lead}

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
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


def require_role(allowed_roles: list):
    def check_role(current_user=Depends(get_current_user)):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return current_user
    return check_role


class LeadStatusUpdate(BaseModel):
    status: str


class LeadCreate(BaseModel):
    name: str
    email: str
    tenant_id: Optional[str] = None
    status: str = "new"


@router.get("/leads")
def get_leads(current_user=Depends(get_current_user), tenant_id: Optional[str] = None):
    """
    Return leads for one company only, restricted by login.
    - Non-admin/sales: always get leads for the user's tenant only (tenant_id param ignored).
    - Admin/sales: can pass tenant_id to view that company's leads; otherwise get user's tenant.
    """
    user_tenant = current_user.get("tenant_id", "")
    role = current_user.get("role", "")

    leads = database.LEADS
    # Restrict by login: only show one company's leads
    if role in ("admin", "sales") and tenant_id:
        effective_tenant = tenant_id
    else:
        effective_tenant = user_tenant

    filtered = [l for l in leads if l.get("tenant_id") == effective_tenant]

    result = []
    for l in filtered:
        tid = l.get("tenant_id", "")
        tn = database.TENANTS.get(tid, {}).get("name", tid)
        result.append({**l, "tenant_name": tn})
    return result


@router.post("/leads")
def create_lead(body: LeadCreate, current_user=Depends(require_role(["lead"]))):
    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Use: {VALID_STATUSES}")

    user_tenant = current_user.get("tenant_id", "")
    role = current_user.get("role", "")
    
    # Determine tenant_id: use provided one if admin/sales, otherwise use user's tenant
    tenant_id = body.tenant_id if (body.tenant_id and role in ("admin", "sales")) else user_tenant
    
    # Get tenant name
    tenant = database.TENANTS.get(tenant_id, {})
    tenant_name = tenant.get("name", tenant_id)

    new_id = max([l.get("id", 0) for l in database.LEADS], default=0) + 1
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lead = {
        "id": new_id,
        "name": body.name.strip(),
        "email": body.email.strip(),
        "tenant_id": tenant_id,
        "status": body.status,
        "created_at": created_at,
    }
    database.LEADS.append(lead)
    
    # Add tenant_name for response
    result = {**lead, "tenant_name": tenant_name}
    return {"message": "Lead created", "lead": result}


@router.post("/leads/{lead_id}/status")
def update_lead_status(lead_id: int, body: LeadStatusUpdate, current_user=Depends(require_role(["lead"]))):
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

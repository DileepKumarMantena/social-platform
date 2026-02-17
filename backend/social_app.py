from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

try:
    import database
except Exception as e:
    raise RuntimeError("database.py not found or has errors: %s" % e)

print(">>>>>>>>>>> THIS IS THE CORRECT social_app.py LOADED <<<<<<<<<<<")

app = FastAPI(title="Social Platform API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- SECURITY ----------------------
security = HTTPBearer()   # THIS FIXES SWAGGER AUTH

# ---------------------- Schemas ----------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChannelToggleRequest(BaseModel):
    channel_id: int

class CampaignCreate(BaseModel):
    name: str
    channel_id: int
    budget: Optional[float] = 0.0

class Lead(BaseModel):
    id: int
    name: str
    email: str

# ---------------------- Auth Helpers ----------------------

def _find_user(username: str):
    for u in getattr(database, "USERS", []):
        if u.get("username") == username:
            return u
    return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Authorization: Bearer <username>
    token IS the username
    """
    token = credentials.credentials
    user = _find_user(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid user/token")

    return user


# ---------------------- Routes ----------------------

@app.get("/")
def root():
    return {"status": "ok", "message": "Social Platform API running"}


# LOGIN
@app.post("/api/login", response_model=TokenResponse)
def login_for_access_token(body: LoginRequest):
    user = _find_user(body.username)

    if not user or user.get("password") != body.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # token = username (no JWT)
    return TokenResponse(access_token=body.username)


# CHANNELS
@app.get("/api/channels")
def get_channels(current_user=Depends(get_current_user)):
    return database.CHANNELS


@app.post("/api/channels/toggle")
def toggle_channel(body: ChannelToggleRequest, current_user=Depends(get_current_user)):
    for ch in database.CHANNELS:
        if ch["id"] == body.channel_id:
            ch["enabled"] = not ch.get("enabled", False)
            return {"message": "Channel updated", "channel": ch}

    raise HTTPException(status_code=404, detail="Channel not found")


# CAMPAIGNS
@app.get("/api/campaigns")
def get_campaigns(current_user=Depends(get_current_user)):
    return database.CAMPAIGNS


@app.post("/api/campaigns")
def create_campaign(body: CampaignCreate, current_user=Depends(get_current_user)):
    channel = next((c for c in database.CHANNELS if c["id"] == body.channel_id), None)

    if not channel:
        raise HTTPException(status_code=400, detail="Invalid channel_id")

    new_id = max([c["id"] for c in database.CAMPAIGNS], default=0) + 1

    campaign = {
        "id": new_id,
        "name": body.name,
        "channel_id": body.channel_id,
        "channel_name": channel["name"],
        "budget": float(body.budget or 0.0),
    }

    database.CAMPAIGNS.append(campaign)
    return {"message": "Campaign created", "campaign": campaign}


# LEADS
@app.get("/api/leads", response_model=List[Lead])
def get_leads(current_user=Depends(get_current_user)):
    return database.LEADS
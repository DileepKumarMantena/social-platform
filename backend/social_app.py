from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers import channels, campaigns, leads, auth, tenants, analytics, activity, follow_up
from constants import DEV, API_PREFIX

print(">>>>>>>>>>> THIS IS THE CORRECT social_app.py LOADED <<<<<<<<<<<")
print(f">>>>>>>>>>> DEV MODE: {DEV} <<<<<<<<<<<")

app = FastAPI(title="Social Platform API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers with dynamic prefix
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(channels.router, prefix=API_PREFIX)
app.include_router(campaigns.router, prefix=API_PREFIX)
app.include_router(leads.router, prefix=API_PREFIX)
app.include_router(tenants.router, prefix=API_PREFIX)
app.include_router(analytics.router, prefix=API_PREFIX)
app.include_router(activity.router, prefix=API_PREFIX)
app.include_router(follow_up.router, prefix=API_PREFIX)

@app.get("/")
def root():
    return {"status": "ok", "message": "Social Platform API running", "dev_mode": DEV}
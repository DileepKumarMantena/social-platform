from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers import channels, campaigns, leads, auth, tenants

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

# Include all routers
app.include_router(auth.router, prefix="/api")
app.include_router(channels.router, prefix="/api")
app.include_router(campaigns.router, prefix="/api")
app.include_router(leads.router, prefix="/api")
app.include_router(tenants.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "message": "Social Platform API running"}
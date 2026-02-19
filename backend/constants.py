# constants.py

# Development Mode Configuration
DEV = True  # When True: Use dummy data, When False: Use database

# API Configuration
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Authentication Configuration
JWT_SECRET_KEY = "your-secret-key-here"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 2FA Configuration
TWO_FA_ENABLED = True
TWO_FA_CODE_LENGTH = 6
TWO_FA_CODE_EXPIRE_MINUTES = 5

# User Roles
ROLE_ADMIN = "admin"
ROLE_LEAD = "lead"
ROLE_USER = "user"

# Campaign Status
STATUS_DRAFT = "draft"
STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_ACTIVE = "active"
STATUS_COMPLETED = "completed"

# Lead Status
LEAD_STATUS_NEW = "new"
LEAD_STATUS_CONTACTED = "contacted"
LEAD_STATUS_QUALIFIED = "qualified"
LEAD_STATUS_CLOSED = "closed"

# Channel Configuration
CHANNEL_FACEBOOK = "facebook"
CHANNEL_INSTAGRAM = "instagram"
CHANNEL_LINKEDIN = "linkedin"
CHANNEL_TWITTER = "twitter"
CHANNEL_YOUTUBE = "youtube"
CHANNEL_GOOGLE_ADS = "google-ads"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Response Messages
MSG_LOGIN_SUCCESS = "Login successful"
MSG_LOGIN_FAILED = "Invalid credentials"
MSG_2FA_REQUIRED = "2FA code required"
MSG_2FA_INVALID = "Invalid 2FA code"
MSG_UNAUTHORIZED = "Unauthorized access"
MSG_FORBIDDEN = "Access forbidden"
MSG_NOT_FOUND = "Resource not found"
MSG_SERVER_ERROR = "Internal server error"

# Demo Data Configuration
DEMO_USERS = [
    {"username": "super_admin", "password": "Super@123456", "role": "super_admin", "tenant_id": "system"},
    {"username": "demo_lead", "password": "Lead@123456", "role": "lead", "tenant_id": "tenant_123", "tenant_name": "Demo Company"},
    {"username": "demo_admin", "password": "Admin@123456", "role": "admin", "tenant_id": "tenant_123", "expires_at": None},
    {"username": "demo_user", "password": "User@123456", "role": "user", "tenant_id": "tenant_123"},
]

# Super admin credentials
SUPER_ADMIN = {
    "username": "super_admin",
    "password": "Super@123456"
}

DEMO_TENANTS = [
    {"id": "tenant_123", "name": "Demo Company", "status": "active"},
    {"id": "tenant_456", "name": "Test Company", "status": "active"},
]

# Channel Colors for UI
CHANNEL_COLORS = {
    "facebook": "#1877f2",
    "instagram": "#e4405f", 
    "linkedin": "#0a66c2",
    "twitter": "#1da1f2",
    "youtube": "#ff0000",
    "google-ads": "#4285f4"
}

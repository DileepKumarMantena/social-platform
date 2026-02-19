# database.py - Multi-tenant demo data with DEV mode support

from constants import DEV, DEMO_USERS, DEMO_TENANTS, CHANNEL_COLORS, STATUS_DRAFT, STATUS_ACTIVE, STATUS_PENDING, STATUS_APPROVED, STATUS_COMPLETED, LEAD_STATUS_NEW, LEAD_STATUS_CONTACTED, LEAD_STATUS_QUALIFIED, LEAD_STATUS_CLOSED, ROLE_ADMIN, ROLE_LEAD, ROLE_USER, CHANNEL_FACEBOOK, CHANNEL_INSTAGRAM, CHANNEL_LINKEDIN, CHANNEL_TWITTER, CHANNEL_YOUTUBE, CHANNEL_GOOGLE_ADS

# Data source selector
def get_tenant_data():
    """Get tenant data based on DEV mode"""
    if DEV:
        return DEMO_TENANTS
    else:
        # TODO: Implement database query for tenants
        return []

def get_user_data():
    """Get user data based on DEV mode"""
    if DEV:
        return DEMO_USERS
    else:
        # TODO: Implement database query for users
        return []

def get_channel_data():
    """Get channel data based on DEV mode"""
    if DEV:
        return [
            {"id": 1, "name": "Facebook", "slug": CHANNEL_FACEBOOK},
            {"id": 2, "name": "Instagram", "slug": CHANNEL_INSTAGRAM},
            {"id": 3, "name": "LinkedIn", "slug": CHANNEL_LINKEDIN},
            {"id": 4, "name": "Twitter", "slug": CHANNEL_TWITTER},
            {"id": 5, "name": "YouTube", "slug": CHANNEL_YOUTUBE},
            {"id": 6, "name": "Google Ads", "slug": CHANNEL_GOOGLE_ADS},
        ]
    else:
        # TODO: Implement database query for channels
        return []

def get_campaign_data():
    """Get campaign data based on DEV mode"""
    if DEV:
        return [
            {"id": 1, "name": "Summer Sale", "channel_id": 1, "channel_name": "Facebook", "channel_slug": CHANNEL_FACEBOOK, "budget": 5000, "status": STATUS_ACTIVE, "tenant_id": "tenant_123", "created_at": "2024-01-15T10:00:00Z"},
            {"id": 2, "name": "Product Launch", "channel_id": 2, "channel_name": "Instagram", "channel_slug": CHANNEL_INSTAGRAM, "budget": 3000, "status": STATUS_PENDING, "tenant_id": "tenant_123", "created_at": "2024-01-20T14:00:00Z"},
            {"id": 3, "name": "Brand Awareness", "channel_id": 3, "channel_name": "LinkedIn", "channel_slug": CHANNEL_LINKEDIN, "budget": 2000, "status": STATUS_DRAFT, "tenant_id": "tenant_123", "created_at": "2024-01-25T11:00:00Z"},
        ]
    else:
        # TODO: Implement database query for campaigns
        return []

def get_lead_data():
    """Get lead data based on DEV mode"""
    if DEV:
        return [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "phone": "+1234567890", "company": "Acme Corp", "status": LEAD_STATUS_NEW, "source": "Facebook", "tenant_id": "tenant_123", "created_at": "2024-01-15T09:00:00Z"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "phone": "+0987654321", "company": "Beta Inc", "status": LEAD_STATUS_CONTACTED, "source": "LinkedIn", "tenant_id": "tenant_123", "created_at": "2024-01-16T10:30:00Z"},
            {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "phone": "+1122334455", "company": "Gamma Ltd", "status": LEAD_STATUS_QUALIFIED, "source": "Twitter", "tenant_id": "tenant_123", "created_at": "2024-01-17T11:15:00Z"},
        ]
    else:
        # TODO: Implement database query for leads
        return []

def get_analytics_data():
    """Get analytics data based on DEV mode"""
    if DEV:
        return {
            "trends": {
                "best_performing_post": {"title": "Summer Sale Announcement", "engagement": 85, "channel": "Facebook"},
                "best_channel": {"name": "Facebook", "performance": 45},
                "optimal_time": {"day": "Tuesday", "time": "14:00"},
            },
            "recommendations": [
                {"type": "posting_time", "message": "Post more on Tuesdays at 2 PM for higher engagement"},
                {"type": "content", "message": "Video content performs 30% better than images"},
                {"type": "channel", "message": "Focus more on LinkedIn for B2B leads"},
            ],
            "dashboard": {
                "total_impressions": 2400000,
                "engagement_rate": 8.5,
                "click_through_rate": 3.2,
                "top_channels": [
                    {"name": "Facebook", "percentage": 45, "color": "#1877f2"},
                    {"name": "Instagram", "percentage": 30, "color": "#e4405f"},
                    {"name": "LinkedIn", "percentage": 25, "color": "#0a66c2"},
                ],
                "optimal_times": [
                    {"day": "Monday", "time": "09:00", "engagement": 75},
                    {"day": "Tuesday", "time": "14:00", "engagement": 85},
                    {"day": "Wednesday", "time": "16:00", "engagement": 70},
                ],
                "demographics": {
                    "18-24": 25,
                    "25-34": 35,
                    "35-44": 25,
                    "45+": 15,
                },
                "trending_content": [
                    {"type": "video", "title": "Product Demo", "views": 50000, "engagement": 12},
                    {"type": "image", "title": "Behind the Scenes", "views": 30000, "engagement": 8},
                    {"type": "text", "title": "Industry Tips", "views": 20000, "engagement": 6},
                ],
            }
        }
    else:
        # TODO: Implement database query for analytics
        return {}

# Legacy compatibility - keep old variable names for existing code
TENANTS = {tenant["id"]: tenant for tenant in get_tenant_data()}
USERS = get_user_data()
CHANNELS = get_channel_data()
CAMPAIGNS = get_campaign_data()
LEADS = get_lead_data()
ANALYTICS_DATA = get_analytics_data()

# Per-tenant channel connections: {tenant_id: [channel_id, ...]}
CHANNEL_CONNECTIONS = {
    "tenant_123": [1, 2],
    "tenant_456": [1],
    "tenant_789": [],
    "tenant_101": [1, 2, 3],
    "tenant_hippo": [1, 2, 3],
    "tenant_nlite": [1, 2],
}

# 2FA tokens (demo purposes)
TWO_FA_TOKENS = {}

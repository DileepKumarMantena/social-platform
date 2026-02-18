# database.py - Multi-tenant demo data

TENANTS = {
    "tenant_123": {"name": "Acme Corp"},
    "tenant_456": {"name": "Beta Inc"},
    "tenant_789": {"name": "Gamma Ltd"},
    "tenant_101": {"name": "Delta Co"},
    "tenant_hippo": {"name": "Hippo Cloud"},
    "tenant_nlite": {"name": "Nlite"},
}

USERS = [
    # Acme Corp
    {"username": "admin", "password": "admin", "role": "admin", "tenant_id": "tenant_123"},
    {"username": "sales", "password": "sales", "role": "lead", "tenant_id": "tenant_123"},
    {"username": "support_mike", "password": "Support@123", "role": "user", "tenant_id": "tenant_123"},
    {"username": "john_viewer", "password": "viewer123", "role": "user", "tenant_id": "tenant_123"},
    
    # Beta Inc
    {"username": "manager_emily", "password": "Manager@123", "role": "admin", "tenant_id": "tenant_456"},
    {"username": "sales_peter", "password": "Sales@321", "role": "lead", "tenant_id": "tenant_456"},
    {"username": "analyst_bob", "password": "analyst123", "role": "user", "tenant_id": "tenant_456"},
    
    # Gamma Ltd
    {"username": "hr_linda", "password": "HR@123", "role": "user", "tenant_id": "tenant_789"},
    {"username": "finance_raj", "password": "Finance@123", "role": "user", "tenant_id": "tenant_789"},
    {"username": "marketing_sarah", "password": "marketing123", "role": "admin", "tenant_id": "tenant_789"},
    {"username": "sales_tom", "password": "sales123", "role": "lead", "tenant_id": "tenant_789"},
    
    # Delta Co
    {"username": "admin_susan", "password": "Admin@321", "role": "admin", "tenant_id": "tenant_101"},
    {"username": "developer_steve", "password": "Dev@123", "role": "user", "tenant_id": "tenant_101"},
    {"username": "sales_rachel", "password": "Sales@456", "role": "lead", "tenant_id": "tenant_101"},
    
    # Hippo Cloud
    {"username": "hippo_admin", "password": "hippo123", "role": "admin", "tenant_id": "tenant_hippo"},
    {"username": "hippo_lead", "password": "hippo456", "role": "lead", "tenant_id": "tenant_hippo"},
    {"username": "hippo_viewer", "password": "hippo789", "role": "user", "tenant_id": "tenant_hippo"},
    
    # Nlite
    {"username": "nlite_admin", "password": "nlite123", "role": "admin", "tenant_id": "tenant_nlite"},
    {"username": "nlite_lead", "password": "nlite456", "role": "lead", "tenant_id": "tenant_nlite"},
    {"username": "nlite_viewer", "password": "nlite789", "role": "user", "tenant_id": "tenant_nlite"},
]

# All available channel types (Facebook, Instagram, LinkedIn, Twitter, YouTube, Google Ads)
CHANNELS = [
    {"id": 1, "name": "Facebook", "slug": "facebook"},
    {"id": 2, "name": "Instagram", "slug": "instagram"},
    {"id": 3, "name": "LinkedIn", "slug": "linkedin"},
    {"id": 4, "name": "Twitter", "slug": "twitter"},
    {"id": 5, "name": "YouTube", "slug": "youtube"},
    {"id": 6, "name": "Google Ads", "slug": "google-ads"},
]

# Per-tenant channel connections: {tenant_id: [channel_id, ...]}
CHANNEL_CONNECTIONS = {
    "tenant_123": [1, 2],
    "tenant_456": [1],
    "tenant_789": [],
    "tenant_101": [1, 2, 3],
    "tenant_hippo": [1, 2, 3],
    "tenant_nlite": [1, 2],
}

CAMPAIGNS = [
    {
        "id": 1,
        "name": "Summer Sale Campaign",
        "channel_id": 1,
        "channel_name": "Facebook",
        "channel_slug": "facebook",
        "budget": 1000.0,
        "status": "active",
        "tenant_id": "tenant_123",
        "tenant_name": "Acme Corp",
        "created_at": "2025-01-15T08:30:00",
        "created_by": "admin",
        "approved_by": "admin",
        "approved_at": "2025-01-15T09:45:00"
    },
    {
        "id": 2,
        "name": "Product Launch",
        "channel_id": 2,
        "channel_name": "Instagram",
        "channel_slug": "instagram",
        "budget": 1500.0,
        "status": "active",
        "tenant_id": "tenant_123",
        "tenant_name": "Acme Corp",
        "created_at": "2025-01-16T09:00:00",
        "created_by": "sales",
        "approved_by": "admin",
        "approved_at": "2025-01-16T09:50:00"
    },
    {
        "id": 3,
        "name": "Brand Awareness",
        "channel_id": 1,
        "channel_name": "Facebook",
        "channel_slug": "facebook",
        "budget": 800.0,
        "status": "active",
        "tenant_id": "tenant_456",
        "tenant_name": "Beta Inc",
        "created_at": "2025-01-17T10:30:00",
        "created_by": "manager_emily",
        "approved_by": "manager_emily",
        "approved_at": "2025-01-17T10:35:00"
    }
]

LEADS = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "tenant_id": "tenant_123", "status": "new", "created_at": "2025-01-15T10:00:00"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "tenant_id": "tenant_123", "status": "contacted", "created_at": "2025-01-16T11:30:00"},
    {"id": 3, "name": "Bob Wilson", "email": "bob@example.com", "tenant_id": "tenant_456", "status": "qualified", "created_at": "2025-01-17T09:00:00"},
    {"id": 4, "name": "Alice Brown", "email": "alice@example.com", "tenant_id": "tenant_456", "status": "new", "created_at": "2025-01-18T14:00:00"},
]

# Analytics data for trend analysis
ANALYTICS = [
    {"id": 1, "campaign_id": 1, "tenant_id": "tenant_123", "channel_id": 1, "impressions": 1500, "clicks": 75, "engagement_rate": 5.0, "posted_at": "2025-01-15T09:00:00"},
    {"id": 2, "campaign_id": 1, "tenant_id": "tenant_123", "channel_id": 2, "impressions": 800, "clicks": 40, "engagement_rate": 5.0, "posted_at": "2025-01-15T14:00:00"},
    {"id": 3, "campaign_id": 2, "tenant_id": "tenant_123", "channel_id": 1, "impressions": 2000, "clicks": 120, "engagement_rate": 6.0, "posted_at": "2025-01-16T10:00:00"},
    {"id": 4, "campaign_id": 2, "tenant_id": "tenant_123", "channel_id": 3, "impressions": 1200, "clicks": 48, "engagement_rate": 4.0, "posted_at": "2025-01-16T16:00:00"},
    {"id": 5, "campaign_id": 3, "tenant_id": "tenant_456", "channel_id": 1, "impressions": 900, "clicks": 45, "engagement_rate": 5.0, "posted_at": "2025-01-17T11:00:00"},
    {"id": 6, "campaign_id": 3, "tenant_id": "tenant_456", "channel_id": 2, "impressions": 600, "clicks": 18, "engagement_rate": 3.0, "posted_at": "2025-01-17T15:00:00"},
]

# Team activity logs
ACTIVITY_LOGS = [
    {"id": 1, "tenant_id": "tenant_123", "user_id": "admin", "action": "created", "entity_type": "campaign", "entity_id": 1, "timestamp": "2025-01-15T08:30:00"},
    {"id": 2, "tenant_id": "tenant_123", "user_id": "sales", "action": "modified", "entity_type": "campaign", "entity_id": 1, "timestamp": "2025-01-15T09:15:00"},
    {"id": 3, "tenant_id": "tenant_123", "user_id": "admin", "action": "approved", "entity_type": "campaign", "entity_id": 2, "timestamp": "2025-01-16T09:45:00"},
    {"id": 4, "tenant_id": "tenant_456", "user_id": "manager_emily", "action": "created", "entity_type": "campaign", "entity_id": 3, "timestamp": "2025-01-17T10:30:00"},
]

# Campaign comments and approval workflow
CAMPAIGN_COMMENTS = [
    {"id": 1, "campaign_id": 1, "tenant_id": "tenant_123", "user_id": "admin", "comment": "Great campaign idea! Let's increase the budget.", "timestamp": "2025-01-15T08:45:00"},
    {"id": 2, "campaign_id": 1, "tenant_id": "tenant_123", "user_id": "sales", "comment": "I think we should target a younger demographic.", "timestamp": "2025-01-15T09:00:00"},
    {"id": 3, "campaign_id": 2, "tenant_id": "tenant_123", "user_id": "admin", "comment": "Approved for launch.", "timestamp": "2025-01-16T09:50:00"},
]

# 2FA tokens (demo purposes)
TWO_FA_TOKENS = {}

# Follow-up sequences
FOLLOW_UP_SEQUENCES = [
    {"id": 1, "tenant_id": "tenant_123", "lead_id": 1, "type": "email", "status": "pending", "scheduled_at": "2025-01-15T12:00:00", "message": "Thank you for your interest! Here's more information..."},
    {"id": 2, "tenant_id": "tenant_123", "lead_id": 2, "type": "sms", "status": "sent", "scheduled_at": "2025-01-16T15:00:00", "message": "Quick follow-up regarding your inquiry."},
]

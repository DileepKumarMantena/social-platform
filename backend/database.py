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
    {"username": "admin", "password": "admin", "role": "admin", "tenant_id": "tenant_123"},
    {"username": "sales", "password": "sales", "role": "sales", "tenant_id": "tenant_123"},
    {"username": "support_mike", "password": "Support@123", "role": "support", "tenant_id": "tenant_123"},
    {"username": "manager_emily", "password": "Manager@123", "role": "manager", "tenant_id": "tenant_456"},
    {"username": "sales_peter", "password": "Sales@321", "role": "sales", "tenant_id": "tenant_456"},
    {"username": "hr_linda", "password": "HR@123", "role": "hr", "tenant_id": "tenant_789"},
    {"username": "finance_raj", "password": "Finance@123", "role": "finance", "tenant_id": "tenant_789"},
    {"username": "admin_susan", "password": "Admin@321", "role": "admin", "tenant_id": "tenant_101"},
    {"username": "developer_steve", "password": "Dev@123", "role": "developer", "tenant_id": "tenant_101"},
    {"username": "sales_rachel", "password": "Sales@456", "role": "sales", "tenant_id": "tenant_101"},
    {"username": "hippo_user", "password": "hippo123", "role": "manager", "tenant_id": "tenant_hippo"},
    {"username": "nlite_user", "password": "nlite123", "role": "manager", "tenant_id": "tenant_nlite"},
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

CAMPAIGNS = []

LEADS = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "tenant_id": "tenant_123", "status": "new", "created_at": "2025-01-15T10:00:00"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "tenant_id": "tenant_123", "status": "contacted", "created_at": "2025-01-16T11:30:00"},
    {"id": 3, "name": "Bob Wilson", "email": "bob@example.com", "tenant_id": "tenant_456", "status": "qualified", "created_at": "2025-01-17T09:00:00"},
    {"id": 4, "name": "Alice Brown", "email": "alice@example.com", "tenant_id": "tenant_456", "status": "new", "created_at": "2025-01-18T14:00:00"},
]

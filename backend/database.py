# ---------------- USERS ----------------
# username + password must EXACTLY match login request

USERS = [
    {
        "id": 1,
        "username": "admin",
        "password": "admin",
        "role": "admin",
        "tenant_id": "tenant_123",
    },
    {
        "id": 2,
        "username": "sales",
        "password": "sales",
        "role": "sales",
        "tenant_id": "tenant_123",
    }
]

# ---------------- CHANNELS ----------------
CHANNELS = [
    {"id": 1, "name": "Facebook", "enabled": True},
    {"id": 2, "name": "Instagram", "enabled": True},
    {"id": 3, "name": "WhatsApp", "enabled": False},
    {"id": 4, "name": "LinkedIn", "enabled": False},
]

# ---------------- CAMPAIGNS ----------------
CAMPAIGNS = [
    {
        "id": 1,
        "name": "Diwali Offer",
        "channel_id": 1,
        "channel_name": "Facebook",
        "budget": 5000,
    },
    {
        "id": 2,
        "name": "New Year Sale",
        "channel_id": 2,
        "channel_name": "Instagram",
        "budget": 8000,
    },
]

# ---------------- LEADS ----------------
LEADS = [
    {"id": 1, "name": "Ravi Kumar", "email": "ravi@gmail.com"},
    {"id": 2, "name": "Priya Sharma", "email": "priya@gmail.com"},
    {"id": 3, "name": "Arjun Reddy", "email": "arjun@gmail.com"},
]
# database.py
USERS = [
    {"username": "admin", "password": "admin", "role": "admin", "tenant_id": "tenant_123"},
    {"username": "sales", "password": "sales", "role": "sales", "tenant_id": "tenant_123"},
]

CHANNELS = [
    {"id": 1, "name": "Facebook", "enabled": True},
    {"id": 2, "name": "Instagram", "enabled": True},
]

CAMPAIGNS = []

LEADS = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
]
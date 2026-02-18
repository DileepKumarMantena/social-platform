# Role-Based Access Control (RBAC)

## Three Role Types

### 1. User (Read-Only)
- **Permissions:**
  - View channels (cannot connect/disconnect)
  - View campaigns (cannot create)
  - View leads (cannot create or update status)
- **Use Case:** Viewers, analysts, stakeholders who need visibility only

### 2. Admin (Manage Channels & Campaigns)
- **Permissions:**
  - View and connect/disconnect channels
  - View and create campaigns
  - View leads only (cannot create or update status)
- **Use Case:** Marketing managers who manage campaigns but don't handle leads

### 3. Lead (Full Access)
- **Permissions:**
  - View and connect/disconnect channels
  - View and create campaigns
  - View, create, and update leads
- **Use Case:** Sales team, lead managers with full operational access

---

## Demo Accounts

| Username      | Password   | Role  | Company    |
| ------------- | ---------- | ----- | ---------- |
| admin         | admin      | admin | Acme Corp  |
| sales         | sales      | lead  | Acme Corp  |
| support_mike  | Support@123| user  | Acme Corp  |
| manager_emily | Manager@123| admin | Beta Inc   |
| sales_peter   | Sales@321  | lead  | Beta Inc   |
| hr_linda      | HR@123     | user  | Gamma Ltd  |

---

## Backend Implementation

### Role Checks
- `require_role([allowed_roles])` dependency in routers
- Returns 403 if user role not in allowed list

### Protected Endpoints
- `POST /api/channels/toggle` - admin, lead only
- `POST /api/campaigns` - admin, lead only
- `POST /api/leads` - lead only
- `POST /api/leads/{id}/status` - lead only

---

## Frontend Implementation

### UI Controls
- Buttons hidden/disabled based on `user.role`
- `canEdit` checks in components:
  - Channels: admin, lead can toggle
  - Campaigns: admin, lead can create
  - Leads: lead only can create/update

---

## Registration
- New users select role during registration
- Default role: "user" (read-only)
- Options: user, admin, lead

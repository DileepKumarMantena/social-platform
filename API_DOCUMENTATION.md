# Social Platform API - Complete Documentation

## Authentication Endpoints

### POST /api/v1/login
Authenticate user and receive access token.
**Request**: `{ "username": "string", "password": "string" }`
**Response**: `{ "access_token": "string", "user": { "username": "string", "role": "string", "tenant_id": "string" } }`

### POST /api/v1/create-tenant (Super Admin only)
Create new tenant/customer with sequential ID.
**Request**: `{ "name": "string" }`
**Response**: `{ "success": true, "tenant_id": "tenant_0001", "message": "Tenant created successfully" }`

### POST /api/v1/create-user (Lead only)
Create new user within tenant with optional time-limited access.
**Request**: `{ "username": "string", "password": "string", "role": "string", "tenant_id": "string", "access_days": "number" }`
**Response**: `{ "success": true, "user_id": "user_0001", "expires_at": "2024-02-20T11:58:00Z", "message": "User created successfully" }`

## Data Endpoints

### GET /api/v1/tenants
Get list of all tenants (Super Admin only).
**Response**: Array of tenant objects with id, name, status, created_at.

### GET /api/v1/campaigns
Get list of campaigns for current user's tenant.
**Response**: Array of campaign objects with id, name, channel, budget, status, metrics.

### GET /api/v1/leads
Get list of leads for current user's tenant.
**Response**: Array of lead objects with id, name, status, contact information.

### GET /api/v1/channels
Get list of available marketing channels.
**Response**: Array of channel objects with id, name, type, configuration.

## Analytics & Trend Analysis

### GET /api/analytics/trends
Get trend analysis including best-performing posts, time slots, and channels.
**Response**: Best performing posts, channels, and optimal time slots based on engagement data.

### GET /api/analytics/recommendations  
Get smart recommendations based on historical engagement data.
**Response**: Channel recommendations, optimal posting times, content performance suggestions.

### GET /api/analytics/dashboard
Get comprehensive analytics dashboard data.
**Response**: Overall metrics, channel breakdown, recent performance data.

## Team Activity Logs

### GET /api/v1/activity-logs
Get system activity logs for auditing (Super Admin only).
**Response**: Array of log entries with timestamp, user, action, details.

## Multi-Tenant Features

### Role-Based Access
- **Super Admin**: Full system access, tenant/user management
- **Lead**: Tenant management, user creation, campaign control
- **Admin**: Time-limited access, campaign management
- **User**: Basic access, campaign viewing, scheduler usage

### Time-Limited Access
Admin users can be created with expiration dates for temporary access.
**Access Days**: Number of days until access expires
**Expiration**: Automatic calculation of end date
**Status**: Admins cannot login after expiration

### Sequential ID Generation
- **Tenants**: tenant_0001, tenant_0002, etc.
- **Users**: user_0001, user_0002, etc.
**Format**: Zero-padded 4-digit numbers
**Purpose**: Scalable identifier system

## Error Responses

### 401 Unauthorized
Invalid credentials or expired admin access.
**Response**: `{ "detail": "Invalid credentials" }`

### 403 Forbidden
Insufficient permissions for requested action.
**Response**: `{ "detail": "Access denied" }`

### 404 Not Found
Requested resource does not exist.
**Response**: `{ "detail": "Resource not found" }`

### 422 Validation Error
Invalid request data format.
**Response**: `{ "detail": "Validation error details" }`

## Rate Limiting

### Request Limits
- **Authentication**: 5 requests per minute
- **Data Endpoints**: 100 requests per minute
- **Analytics**: 50 requests per minute

### Headers
- **X-RateLimit-Limit**: Total requests allowed
- **X-RateLimit-Remaining**: Requests remaining
- **X-RateLimit-Reset**: Time when limit resets

## Data Models

### User Model
```json
{
  "username": "string",
  "role": "super_admin|lead|admin|user",
  "tenant_id": "string",
  "expires_at": "string|null",
  "tenant_name": "string"
}
```

### Tenant Model
```json
{
  "id": "string",
  "name": "string",
  "status": "active|inactive",
  "created_at": "string"
}
```

### Campaign Model
```json
{
  "id": "number",
  "name": "string",
  "channel_name": "string",
  "channel_slug": "string",
  "budget": "number",
  "status": "draft|active|pending|completed",
  "impressions": "number",
  "clicks": "number",
  "engagement": "number",
  "created_at": "string"
}
```

## Version Information

### Current Version: v1.0
### Base URL: http://localhost:8000/api/v1
### Authentication: Bearer Token required for all endpoints except login

## Security Features

### Password Management
- Passwords stored securely in backend
- Frontend password visibility toggle for admin users
- Encrypted transmission for all sensitive data

### Tenant Isolation
- Data completely separated by tenant
- Users can only access their tenant's data
- Super Admin can access all tenant data

### Access Control
- Role-based permissions enforced at API level
- Time-limited access automatically enforced
- Activity logging for audit trails

### GET /api/activity/logs
Get team activity logs for the current tenant.
**Response**: List of all activities (created, modified, approved, commented) with user info.

### GET /api/activity/stats
Get activity statistics for the current tenant.
**Response**: Activity counts by action type, user, and entity type.

## Campaign Comments & Approval Workflow

### GET /api/campaigns/{campaign_id}/comments
Get all comments for a specific campaign.
**Response**: Comments with user information and timestamps.

### POST /api/campaigns/{campaign_id}/comments
Add a comment to a campaign.
**Body**: `{ "comment": "string" }`

### POST /api/campaigns/{campaign_id}/approve
Approve or reject a campaign (admin only).
**Body**: `{ "approved": boolean, "notes": "string" }`

### GET /api/campaigns/pending-approval
Get all campaigns pending approval (admin only).
**Response**: List of campaigns awaiting approval.

## Email & SMS Follow-Up Automation

### GET /api/follow-up/templates
Get available follow-up templates.
**Response**: List of email and SMS templates.

### POST /api/follow-up/create
Create a new follow-up sequence.
**Body**: `{ "lead_id": number, "type": "email|sms", "message": "string", "scheduled_at": "string" }`

### GET /api/follow-up/list
Get all follow-ups for the current tenant.
**Response**: Follow-ups with lead information and status.

### POST /api/follow-up/{follow_up_id}/send
Send a follow-up immediately (demo).
**Response**: Send status and delivery confirmation.

### POST /api/follow-up/{follow_up_id}/cancel
Cancel a pending follow-up.
**Response**: Cancellation confirmation.

### GET /api/follow-up/stats
Get follow-up statistics.
**Response**: Counts by status and type.

### POST /api/follow-up/bulk-create
Create follow-ups for multiple leads at once.
**Body**: `{ "lead_ids": [numbers], "template_id": number, "message": "string", "type": "email|sms" }`

## Two-Factor Authentication (2FA)

### POST /api/login/step1
First step of login - validate credentials and issue 2FA if needed.
**Body**: `{ "username": "string", "password": "string" }`
**Response**: 2FA code (for admin users) or direct token (for regular users).

### POST /api/login/step2
Second step of login - verify 2FA code.
**Body**: `{ "username": "string", "password": "string", "two_factor_code": "string" }`
**Response**: Access token upon successful verification.

### POST /api/login
Legacy login endpoint for backward compatibility.
**Response**: Access token with `requires_two_factor` flag.

## Demo Notes

- **2FA**: Enabled for admin users only. Demo shows 2FA code in response.
- **Follow-ups**: Simulated 95% delivery success rate.
- **Analytics**: Uses sample data for demonstration.
- **Comments**: All users can comment, only admins can approve.
- **Activity Logs**: Automatically track all campaign-related actions.

## Sample Data

The system includes sample campaigns, analytics, leads, and activity logs for testing. Admin users (e.g., "admin", "manager_emily") will trigger 2FA, while regular users can login directly.

## Testing

1. Start server: `cd backend && source venv/bin/activate && python -m uvicorn social_app:app --reload --host 0.0.0.0 --port 8000`
2. Use existing users or register new ones
3. Admin users will receive 2FA codes in the response
4. Explore all new endpoints using the API documentation

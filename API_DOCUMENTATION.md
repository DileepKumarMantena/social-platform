# Social Platform API - New Features Documentation

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

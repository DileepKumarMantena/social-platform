# Registration & Routing Implementation

## Changes Made

### Backend
1. **auth.py** - Added `/api/register` endpoint
   - Creates new user with username, password, company name
   - Auto-generates tenant_id
   - Returns access token immediately after registration

### Frontend
1. **Installed react-router-dom** for URL-based routing

2. **App.jsx** - Converted to single-page app with routes:
   - `/login` - Login page
   - `/register` - Registration page
   - `/dashboard` - Dashboard (default)
   - `/channels` - Channels page
   - `/campaigns` - Campaigns page
   - `/leads` - Leads page
   - `/settings` - Settings page

3. **Register.jsx** - New registration component
   - Username, password, company name fields
   - Link to login page

4. **Login.jsx** - Added link to register page

5. **AppUtils.js** - Added `register()` function

## Usage

### Start Backend
```bash
cd backend
python -m uvicorn social_app:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd frontend/social-frontend
npm run dev
```

### Access URLs
- Login: http://localhost:5173/login
- Register: http://localhost:5173/register
- Dashboard: http://localhost:5173/dashboard
- Channels: http://localhost:5173/channels
- Campaigns: http://localhost:5173/campaigns
- Leads: http://localhost:5173/leads
- Settings: http://localhost:5173/settings

### Features
✅ URL-based routing - refresh works on any page
✅ Registration creates new tenant automatically
✅ Auto-login after registration
✅ Navigation preserves URL state
✅ Protected routes redirect to login if not authenticated

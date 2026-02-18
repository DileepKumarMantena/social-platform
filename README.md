# Social Platform (SocialMark)

A full-stack social media marketing platform with a **FastAPI** backend and **React + Vite** frontend. Multi-tenant demo supporting Facebook, Instagram, LinkedIn, Twitter, YouTube, and Google Ads. Users can register, connect channels, create campaigns, view leads, and sales users can follow up on leads per company.

**Development Mode** — In-memory storage. Designed for demos, frontend integration, and learning.

---

## Tech Stack

### Backend
- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic

### Frontend
- React 19
- Vite 7
- React Router DOM
- Axios

---

## Project Structure

```
social-platform/
├── backend/
│   ├── social_app.py       # Main FastAPI app
│   ├── database.py         # In-memory dummy data
│   ├── routers/
│   │   ├── auth.py         # Login & Register
│   │   ├── channels.py     # Channels CRUD
│   │   ├── campaigns.py    # Campaigns CRUD
│   │   ├── leads.py        # Leads
│   │   └── tenants.py      # Tenants list
│   └── ...
├── frontend/
│   └── social-frontend/
│       ├── src/
│       │   ├── App.jsx
│       │   ├── AppUtils.js # API client
│       │   └── components/
│       │       ├── Login.jsx
│       │       ├── Register.jsx
│       │       ├── Dashboard.jsx
│       │       ├── Channels.jsx
│       │       ├── Campaigns.jsx
│       │       ├── Leads.jsx
│       │       └── Settings.jsx
│       ├── package.json
│       └── vite.config.js
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm

---

## Installation & Running

### 1. Backend (API)

**Create and activate virtual environment**

```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run the server**

```bash
cd backend
python -m uvicorn social_app:app --reload --host 0.0.0.0 --port 8000
```

API base URL: **http://127.0.0.1:8000**

---

### 2. Frontend (React)

**Install dependencies**

```bash
cd frontend/social-frontend
npm install
```

**Run the dev server**

```bash
npm run dev
```

Frontend: **http://localhost:5173** (or the port Vite assigns)

---

## Getting Started

### Option 1: Register New Account
1. Go to **http://localhost:5173/register**
2. Enter username, password, company name, and select role
3. Click Register - you'll be logged in automatically

### Option 2: Use Demo Accounts

#### Acme Corp
| Username      | Password   | Role  | Access Level |
| ------------- | ---------- | ----- | ------------ |
| admin         | admin      | admin | Channels & Campaigns |
| sales         | sales      | lead  | Full Access |
| support_mike  | Support@123| user  | Read-only |
| john_viewer   | viewer123  | user  | Read-only |

#### Beta Inc
| Username      | Password   | Role  | Access Level |
| ------------- | ---------- | ----- | ------------ |
| manager_emily | Manager@123| admin | Channels & Campaigns |
| sales_peter   | Sales@321  | lead  | Full Access |
| analyst_bob   | analyst123 | user  | Read-only |

#### Gamma Ltd
| Username        | Password     | Role  | Access Level |
| --------------- | ------------ | ----- | ------------ |
| marketing_sarah | marketing123 | admin | Channels & Campaigns |
| sales_tom       | sales123     | lead  | Full Access |
| hr_linda        | HR@123       | user  | Read-only |
| finance_raj     | Finance@123  | user  | Read-only |

#### Delta Co
| Username        | Password   | Role  | Access Level |
| --------------- | ---------- | ----- | ------------ |
| admin_susan     | Admin@321  | admin | Channels & Campaigns |
| sales_rachel    | Sales@456  | lead  | Full Access |
| developer_steve | Dev@123    | user  | Read-only |

#### Hippo Cloud
| Username      | Password | Role  | Access Level |
| ------------- | -------- | ----- | ------------ |
| hippo_admin   | hippo123 | admin | Channels & Campaigns |
| hippo_lead    | hippo456 | lead  | Full Access |
| hippo_viewer  | hippo789 | user  | Read-only |

#### Nlite
| Username     | Password | Role  | Access Level |
| ------------ | -------- | ----- | ------------ |
| nlite_admin  | nlite123 | admin | Channels & Campaigns |
| nlite_lead   | nlite456 | lead  | Full Access |
| nlite_viewer | nlite789 | user  | Read-only |

---

## Role-Based Access Control

### User (Read-Only)
- ✅ View channels, campaigns, and leads
- ❌ Cannot create or modify anything

### Admin (Manage Channels & Campaigns)
- ✅ View and connect/disconnect channels
- ✅ View and create campaigns
- ✅ View leads (read-only)
- ❌ Cannot create or update leads

### Lead (Full Access)
- ✅ View and connect/disconnect channels
- ✅ View and create campaigns
- ✅ View, create, and update leads

---

## Authentication

- Register via `POST /api/register` with `username`, `password`, `tenant_name`, and `role`
- Login via `POST /api/login` with `username` and `password`
- Response includes `access_token`
- Protected routes require header: `Authorization: Bearer <access_token>`
- Auth persists in localStorage (survives page refresh)

---

## API Routes

| Method | Endpoint | Description | Required Role |
| ------ | -------- | ----------- | ------------- |
| GET | `/` | Health check | None |
| POST | `/api/register` | Register new user; returns token + user | None |
| POST | `/api/login` | Login; returns token + user (tenant, role) | None |
| POST | `/api/change-password` | Change password | Any authenticated |
| GET | `/api/channels` | List all 6 channel types with connection status | Any authenticated |
| POST | `/api/channels/toggle` | Connect/disconnect channel | admin, lead |
| GET | `/api/campaigns` | List campaigns (filtered by tenant) | Any authenticated |
| GET | `/api/campaigns/stats` | Campaign stats | Any authenticated |
| POST | `/api/campaigns` | Create campaign | admin, lead |
| GET | `/api/leads` | List leads | Any authenticated |
| POST | `/api/leads` | Create lead | lead |
| POST | `/api/leads/{id}/status` | Update lead status | lead |
| GET | `/api/tenants` | List tenants | Any authenticated |

---

## Frontend Routes

| URL | Description |
| --- | ----------- |
| `/login` | Login page |
| `/register` | Registration page |
| `/dashboard` | Dashboard (default) |
| `/channels` | Manage social channels |
| `/campaigns` | View and create campaigns |
| `/leads` | View and manage leads |
| `/settings` | User settings |

**Note:** All routes support refresh and direct navigation

---

## API Documentation (Swagger)

When the backend is running:

**http://127.0.0.1:8000/docs**

Use **Authorize** and enter the username (e.g. `admin`) to test protected routes.

---

## Notes

- Data is in-memory and resets when the backend restarts
- No persistent database
- CORS allows all origins in development
- Auth state persists in browser localStorage

---

## Features (Demo)

- **Registration**: Create new accounts with auto-tenant creation and role selection
- **Role-Based Access**: Three role types (user, admin, lead) with different permissions
- **6 channels**: Facebook, Instagram, LinkedIn, Twitter, YouTube, Google Ads
- **Multi-tenant**: Each registered user gets their own company/tenant
- **Campaigns**: Create per channel, view status, placeholder for results
- **Leads**: Status workflow (new → contacted → qualified → won/lost), follow-up for sales
- **Single Page App**: URL-based routing with refresh support

---

## Author

Dileep Kumar

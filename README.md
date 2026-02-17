# Social Platform (SocialMark)

A full-stack social media marketing platform with a **FastAPI** backend and **React + Vite** frontend. Multi-tenant demo supporting Facebook, Instagram, LinkedIn, Twitter, YouTube, and Google Ads. Users connect channels, create campaigns, view leads, and sales users can follow up on leads per company.

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
- Axios

---

## Project Structure

```
social-platform/
├── backend/
│   ├── social_app.py       # Main FastAPI app
│   ├── database.py         # In-memory dummy data
│   ├── routers/
│   │   ├── auth.py         # Login
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
│       │       ├── Dashboard.jsx
│       │       ├── Channels.jsx
│       │       ├── Campaigns.jsx
│       │       └── Leads.jsx
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

## Default Users (Multi-tenant Demo)

| Username      | Password   | Role    | Company    |
| ------------- | ---------- | ------- | ---------- |
| admin         | admin      | admin   | Acme Corp  |
| sales         | sales      | sales   | Acme Corp  |
| manager_emily | Manager@123| manager | Beta Inc   |
| sales_peter   | Sales@321  | sales   | Beta Inc   |

---

## Authentication

- Login via `POST /api/login` with `username` and `password`.
- Response includes `access_token`.
- Protected routes require header: `Authorization: Bearer <access_token>`.

---

## API Routes

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/` | Health check |
| POST | `/api/login` | Login; returns token + user (tenant, role) |
| GET | `/api/channels` | List all 6 channel types with connection status |
| POST | `/api/channels/toggle` | Connect/disconnect channel (body: `{ "channel_id": 1 }`) |
| GET | `/api/campaigns` | List campaigns (filtered by tenant) |
| GET | `/api/campaigns/stats` | Campaign stats |
| POST | `/api/campaigns` | Create campaign (body: `{ "name", "channel_id", "budget" }`) |
| GET | `/api/leads` | List leads (optional `?tenant_id=` for sales/admin) |
| POST | `/api/leads/{id}/status` | Update lead status (body: `{ "status": "contacted" }`) |
| GET | `/api/tenants` | List tenants (for sales company filter) |

---

## API Documentation (Swagger)

When the backend is running:

**http://127.0.0.1:8000/docs**

Use **Authorize** and enter the username (e.g. `admin`) to test protected routes.

---

## Notes

- Data is in-memory and resets when the backend restarts.
- No persistent database.
- CORS allows all origins in development.

---

## Features (Demo)

- **6 channels**: Facebook, Instagram, LinkedIn, Twitter, YouTube, Google Ads
- **Multi-tenant**: Acme Corp, Beta Inc, Gamma Ltd, Delta Co
- **Campaigns**: Create per channel, view status, placeholder for results
- **Leads**: Status workflow (new → contacted → qualified → won/lost), follow-up for sales
- **Role-based**: Admin/sales see company filter on leads

---

## Author

Dileep Kumar

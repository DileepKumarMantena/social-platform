# Social Platform

A full-stack social media marketing platform with a **FastAPI** backend and **React + Vite** frontend. Users can log in, manage channels, create campaigns, and view leads.

**Development Mode** — No real database; uses in-memory storage. Designed for frontend integration, learning, and testing.

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
│   │   └── leads.py        # Leads
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

## Default Users

| Username | Password |
| -------- | -------- |
| admin    | admin    |
| sales    | sales    |

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
| POST | `/api/login` | Login; returns token |
| GET | `/api/channels` | List channels |
| POST | `/api/channels/toggle` | Toggle channel (body: `{ "channel_id": 1 }`) |
| GET | `/api/campaigns` | List campaigns |
| POST | `/api/campaigns` | Create campaign (body: `{ "name", "channel_id", "budget" }`) |
| GET | `/api/leads` | List leads |

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

## Future Improvements

- JWT authentication
- PostgreSQL (or another DB)
- User registration
- Multi-tenant support
- Campaign analytics

---

## Author

Dileep Kumar

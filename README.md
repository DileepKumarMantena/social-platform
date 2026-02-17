# Social Platform API (Dev Mode)

A simple backend API built using **FastAPI** that simulates a social media marketing platform.
The application allows a user to log in, view social channels, create campaigns, and view leads.

This project currently runs in **Development Mode (No real authentication, no database)** using an in-memory dummy database.

---

## What the Application Does

The API mimics a marketing dashboard used by a company to manage:

* Connected social media channels (Facebook, Instagram, etc.)
* Marketing campaigns
* Leads generated from campaigns

It is designed mainly for:

* Frontend integration practice (React / HTML / Vite)
* Learning FastAPI
* Understanding API authentication flow
* Testing UI without a real database

---

## Tech Stack

* Python 3.10+
* FastAPI
* Uvicorn
* Pydantic

No external database is used.
All data is stored in memory inside `database.py`.

---

## Project Structure

```
backend/
│
├── social_app.py      # Main FastAPI application
├── database.py        # Dummy in-memory data
├── requirements.txt
└── README.md
```

---

## How Authentication Works (IMPORTANT)

This project does **NOT use JWT yet**.

Instead:

1. You login using username & password
2. The server returns a token
3. The token is actually just your username
4. Every protected API requires:

```
Authorization: Bearer <username>
```

Example:

```
Authorization: Bearer admin
```

---

## Default Users

| Username | Password |
| -------- | -------- |
| admin    | admin    |
| sales    | sales    |

---

## Installation & Running the Project

### 1. Create virtual environment

Mac/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

Windows:

```
python -m venv venv
venv\Scripts\activate
```

---

### 2. Install dependencies

```
pip install fastapi uvicorn
```

(Or if you have requirements.txt)

```
pip install -r requirements.txt
```

---

### 3. Run the server

```
python -m uvicorn social_app:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## API Documentation (Swagger)

After starting the server, open:

```
http://127.0.0.1:8000/docs
```

This is the interactive API UI where you can test all routes.

---

## How to Login

Endpoint:

```
POST /api/login
```

Request body:

```json
{
  "username": "admin",
  "password": "admin"
}
```

Response:

```json
{
  "access_token": "admin",
  "token_type": "bearer"
}
```

---

## IMPORTANT — Using Protected Routes

1. Open `/docs`
2. Click **Authorize 🔒**
3. Enter:

```
admin
```

4. Click Authorize

Now all APIs will work.

---

## Available API Routes

### Health Check

```
GET /
```

Checks if API is running.

---

### Login

```
POST /api/login
```

Returns access token.

---

### Channels

```
GET /api/channels
```

Returns all social channels.

```
POST /api/channels/toggle
```

Enable or disable a channel.

Request:

```json
{
  "channel_id": 1
}
```

---

### Campaigns

```
GET /api/campaigns
```

List campaigns.

```
POST /api/campaigns
```

Create campaign.

Request:

```json
{
  "name": "Summer Sale",
  "channel_id": 1,
  "budget": 5000
}
```

---

### Leads

```
GET /api/leads
```

Returns all leads.

---

## Notes

* Data resets when server restarts
* No real database yet
* No real authentication yet
* This is a development/testing backend

---

## Future Improvements

* JWT Authentication
* PostgreSQL database
* User registration
* Multi-tenant support
* Campaign analytics

---

## Author

Dileep Kumar

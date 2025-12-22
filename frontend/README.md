# Frontend (moved into `frontend/`)

This is your existing Vue 3 + Vite app moved under the `frontend` folder, now integrated with the FastAPI backend.

## Run

1) Install deps (from `frontend`):
```
cd frontend
npm install
```

2) Start dev server:
```
npm run dev
```

It runs at http://localhost:5173

## Backend API

Ensure the FastAPI backend is running at http://localhost:8000 (default).

The frontend fetches articles from:
- `GET http://localhost:8000/api/articles?q=...`

You can override API base via `.env`:
```
# frontend/.env
VITE_API_BASE=http://localhost:8000
```








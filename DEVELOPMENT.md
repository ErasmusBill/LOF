# Local Development (No Docker)

This project can run locally on Windows without Docker.

## Prerequisites

- Python 3.12
- `uv` installed and available in PATH

## Setup

From project root:

```powershell
.\scripts\dev-setup.ps1
```

What this does:

- creates `.venv` with Python 3.12
- installs dependencies from `requirements.txt`
- creates `.env.local` from `.env.local.example` (if missing)
- runs database migrations

## Run the server

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open:

- http://127.0.0.1:8000/

## Notes

- `.env` remains the shared/Docker config.
- `.env.local` overrides `.env` for local non-Docker development.
- Local default DB is SQLite (`db.sqlite3`) through `.env.local`.

# Shortly: URL Shortener

A Flask URL shortener with authentication, per-link click tracking, a paginated
personal dashboard, and PostgreSQL migrations.

## Features
- Email/password signup, login, logout (hashed passwords, Flask-Login sessions)
- CSRF protection on all forms
- 6-character random short codes, collision-safe (unique constraint + retry)
- Atomic click counting on redirect
- Users can only see and delete their own links
- Server-side pagination on the dashboard
- Tests with pytest

## Stack
Python, Flask, SQLAlchemy, Flask-Migrate (Alembic), PostgreSQL, Jinja2, Tailwind CSS

## Run locally
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:password@localhost/shortly   # optional, defaults to SQLite
export SECRET_KEY=change-me
flask --app run db init
flask --app run db migrate -m "initial"
flask --app run db upgrade
python run.py
```

## Tests
```bash
pytest
```

## Roadmap
- Custom aliases and link expiry
- Daily click analytics
- Docker + deployment
- Admin role / RBAC

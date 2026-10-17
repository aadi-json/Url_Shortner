# Shortly: URL Shortener

A Bitly-inspired URL shortener built with Flask, Python, SQLAlchemy, and SQLite, featuring user authentication, URL redirection, click tracking, and a personal dashboard.

## Features

- User registration, login, and logout
- Secure password hashing and session management
- CSRF protection on forms
- Unique, randomly generated 6-character short URLs
- Automatic click tracking on redirects
- Personal dashboard with server-side pagination
- Users can view and delete only their own links
- Database migrations using Flask-Migrate and Alembic
- Automated tests using pytest

## Tech Stack

- **Language:** Python
- **Backend:** Flask
- **Database:** SQLite (default), PostgreSQL support if configured
- **ORM:** SQLAlchemy
- **Migrations:** Flask-Migrate and Alembic
- **Authentication:** Flask-Login
- **Frontend:** HTML, CSS, Jinja2, Tailwind CSS

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/aadi-json/Url_Shortner.git
cd Url_Shortner
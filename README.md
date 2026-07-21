# NGO Volunteer Sign-In

A lightweight web app that lets NGOs collect volunteer sign-ins via a shared link on
event day, and lets event owners export the collected data as CSV or XLSX afterwards.

Built with **Flask**, **SQLAlchemy**, and **Flask-Login**.

## How it works

**Volunteers** (no account needed)
1. The event owner shares a link, e.g. `https://yourapp.com/signin/beach-cleanup-a1b2c3`
2. The volunteer opens it on their phone and fills in name, email, phone
3. They see an instant confirmation — no login required

**Owners** (authenticated)
1. Log in at `/admin/login`
2. Create events from the dashboard — each gets a unique, auto-generated sign-in link
3. View live sign-in counts per event
4. Download the volunteer list as CSV or XLSX at any time

## Project structure

ngo-signin/
├── app/
│ ├── init.py # App factory
│ ├── models.py # Owner, Event, Volunteer
│ ├── validation.py # Form-validation logic
│ ├── export.py # CSV/XLSX generation via pandas
│ ├── routes/
│ │ ├── public.py # Volunteer sign-in routes
│ │ └── admin.py # Owner login, dashboard, export
│ ├── templates/
│ └── static/
├── requirements.txt
└── run.py

## Setup

```bash
python -m venv venv
source venv/Scripts/activate    # Windows Git Bash; use venv\Scripts\activate on cmd/PowerShell
pip install -r requirements.txt
```

Create an owner account:

```bash
flask --app run.py create-owner
```

Run the dev server:

```bash
flask --app run.py run --debug
```

Visit `http://127.0.0.1:5000` — volunteers sign in via `/signin/<slug>`,
owners log in via `/admin/login`.

## Production considerations (not implemented, noted for context)

- Swap SQLite for PostgreSQL via `DATABASE_URL`
- Add CSRF protection (Flask-WTF) on forms
- Rate-limit the public sign-in endpoint
- HTTPS + secure cookie flags in production config
- Support multiple owner accounts per NGO (currently one flat `Owner` table)
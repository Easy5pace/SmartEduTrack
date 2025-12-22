# SmartEduTrack Documentation

## Overview
SmartEduTrack is a Flask-based web application for managing educational data, including students, teachers, parents, and admins. It provides dashboards, analytics, and CRUD operations for all user types, with role-based access and PDF export features.

## Features
- User roles: Admin, Student, Teacher, Parent
- Role-specific dashboards
- Student marks, attendance, and assignments management
- Teacher analytics: class performance, attendance graphs, weak students
- Admin management: add/edit/remove users, view user info
- Parent view: child progress, feedback
- PDF export for student progress cards
- Demo data seeding

## Project Structure
```
SmartEduTrack/
<!-- SmartEduTrack README -->

# SmartEduTrack

Lightweight school management demo app built with Flask. Use it to manage students, teachers, parents and admins, track marks/attendance, assign work, view analytics and export student progress as PDFs.

This README covers quick setup, architecture, developer workflow, and next steps for turning the demo into a production-ready app.

## Quick links
- App entry: `run.py`
- App package: `app/`
- Templates: `app/templates/`
- Static: `app/static/`
- Models: `app/models.py`
- Routes: `app/routes.py`
- Forms: `app/forms.py`
- Requirements: `requirements.txt`

## Quickstart (local)
1. Create & activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app (development server):

```powershell
python run.py
```

4. Seed demo data (optional):

Open your browser to: `http://127.0.0.1:5000/seed` (creates sample admin, teacher, students and parent).

## Tech stack (at-a-glance)
- Backend: Python, Flask
- ORM: SQLAlchemy (Flask-SQLAlchemy)
- Auth/forms: Flask-Login, Flask-WTF
- DB: SQLite (default; configurable via `DATABASE_URL` env var)
- Frontend: Jinja2 templates, Bootstrap, Plotly, Chart.js
- PDF: xhtml2pdf
- Analytics: pandas, plotly

Exact versions are pinned in `requirements.txt`.

## Architecture & Key files
- `app/__init__.py` — app factory, extension init, blueprint registration
- `app/models.py` — SQLAlchemy models (User, Student, Teacher, Parent, Mark, Attendance, Assignment, Feedback)
- `app/forms.py` — WTForms used across dashboards
- `app/routes.py` — All HTTP routes and dashboard logic
- `app/utils.py` — helpers (PDF rendering)
- `app/templates/` — Jinja2 templates (dashboard_*.html, base.html, login/register)
- `app/static/` — JS/CSS assets

## Routes / Features (MVP)
- Authentication: `/login`, `/register`, `/logout`
- Dashboards: `/dashboard/student`, `/dashboard/teacher`, `/dashboard/parent`, `/dashboard/admin`
- Admin CRUD: `/admin/add-student`, `/admin/add-teacher`, `/admin/add-parent` (+AJAX edit/remove)
- Student progress: `/progress-card/<id>` and `/progress-card/<id>/pdf`
- Assignment grading: `POST /assignment/<id>/update`
- Seed: `/seed` (demo data)

## Developer notes & recommended improvements
This project is a demo and intentionally light on production features. Priority improvements before production:

- Password hashing: currently passwords are plain text. Integrate `werkzeug.security` or `bcrypt` to hash passwords on save and verify on login.
- Database migrations: add Flask-Migrate / Alembic to manage schema changes.
- Replace SQLite with Postgres (or another RDBMS) for production. Update `DATABASE_URL` env var accordingly.
- Disable or remove `/seed` in production builds. Seed only in dev/test.
- Add tests (unit + integration) and a CI pipeline (GitHub Actions) to run tests on push/PR.
- Add Dockerfile + docker-compose for reproducible development and optional deployment.

## Environment variables
- `SECRET_KEY` — Flask secret key (default: development fallback in code)
- `DATABASE_URL` — SQLAlchemy database URI (defaults to local sqlite file `smartedutrack.db`)

Example (PowerShell):

```powershell
$env:SECRET_KEY = 'change-me'
$env:DATABASE_URL = 'sqlite:///smartedutrack.db'
python run.py
```

## Testing & CI (suggested)
- Add `pytest` and a few unit tests for models and routes. Example tests:
  - registration/login flows
  - admin creates a student
  - teacher assigns to class and grades
- Add a GitHub Actions workflow to run the test suite and lint on PRs.

## Data model notes
- Assignments are modeled per student (there is a `student_id` FK). The teacher UI bulk-creates one Assignment row per student in the class when assigning to the whole class. This avoids a separate join table in the MVP.

## Security & privacy
- Don't store real user passwords in plain text. Migrate to hashed passwords ASAP.
- Protect seed and admin-only routes in production.
- Sanitize and validate user input (scores, dates, text) and add rate-limiting if exposed publicly.

## Getting help / contributing
- Read `.github/copilot-instructions.md` for repo-specific conventions used by contributors and bots.
- To contribute: fork, branch, implement feature, add tests, open a PR.

## License
This repo is provided as a demo. Add an explicit license file (e.g., MIT) if you want to publish or share the project.

---

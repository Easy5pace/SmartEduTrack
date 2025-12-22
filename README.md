# SmartEduTrack 

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
# SmartEduTrack

SmartEduTrack is a lightweight Flask application for tracking student progress, attendance, assignments, and basic classroom analytics. It is suitable for local development and simple deployment to services like Render.

---

## Features

- User roles: student, teacher, parent, admin
- Track attendance, marks/grades, and assignments
- Basic analytics and charts (Plotly / Chart.js)
- Export progress card (xhtml2pdf)

---

## Quick Start (local)

Prerequisites: Python 3.10+, pip

1. Clone the repository and open the project root.

2. Create and activate a virtual environment, then install dependencies:

```powershell
cd 'D:\D\Projects\SmartEduTrack\SmartEduTrack'
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
```

3. Run the app:

```powershell
python run.py
```

4. Open http://127.0.0.1:5000 in your browser.

---

## Configuration / Environment Variables

- `SECRET_KEY` — Flask secret key. Always set this in production.
- `DATABASE_URL` — SQLAlchemy URL for the database. Defaults to a local sqlite file `smartedutrack.db` if unset.

Tip: set environment variables in your shell or via your hosting provider's environment settings.

---

## Database

- Development default: SQLite file at project root (`smartedutrack.db`).
- Recommended production DB: PostgreSQL (set `DATABASE_URL` accordingly).
- Optional: Use Flask-Migrate for schema migrations.

Example Flask-Migrate commands (if enabled):

```powershell
flask db init
flask db migrate -m "initial"
flask db upgrade
```

---

## Deployment (Render example)

1. Ensure the repo contains `requirements.txt` and `Procfile` at the repository root.
2. Create a new Web Service on Render and connect it to the GitHub repository.
3. Set the Start Command to:

```
gunicorn run:app
```

4. Add environment variables on Render: `SECRET_KEY` and (optional) `DATABASE_URL`.
5. Trigger or wait for a deploy; Render will install dependencies from `requirements.txt`.

---

## Recent fixes in this branch

- `requirements.txt`: pinned `Werkzeug<3.0.0` to resolve `Flask-WTF` recaptcha compatibility with Werkzeug 3.x.
- `app/templates/base.html`: corrected Bootstrap CDN version so CSS/JS load successfully.

---

## Troubleshooting

- Static assets appear unstyled:
  - Hard-refresh the browser and check DevTools → Network to ensure `/static/css/styles.css` returns 200 and CDN files are reachable.
- Error `cannot import name 'url_encode'` from `werkzeug.urls`:
  - Pin `Werkzeug` to a 2.x release (`Werkzeug<3.0.0`) or upgrade to a `Flask-WTF` version compatible with Werkzeug 3.x.
- Git / push issues:
  - Confirm remote is configured and push your branch; use PR workflow for safe changes.

---

## Testing

Run tests (project includes `pytest` in `requirements.txt` if needed):

```powershell
pip install -r requirements.txt
pytest
```

---

## Project structure (high level)

- `app/` — application package (routes, models, forms, templates, static)
- `run.py` — application entrypoint
- `requirements.txt` — Python dependencies
- `Procfile` — process start for PaaS (gunicorn)

---

## Contributing

- Create a topic branch and open a Pull Request for review.
- Keep commit messages clear and scoped.

---

## License

Add a `LICENSE` file to the repository (e.g., MIT) and reference it here.

---

If you want, I can commit this updated `README.md`, add a `.gitignore`, and push them to a branch for your review.

## Getting help / contributing
- Read `.github/copilot-instructions.md` for repo-specific conventions used by contributors and bots.
- To contribute: fork, branch, implement feature, add tests, open a PR.

## License
This repo is provided as a demo. Add an explicit license file (e.g., MIT) if you want to publish or share the project.

---

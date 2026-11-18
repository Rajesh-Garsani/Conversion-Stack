# Operational Agency Website

A standalone, admin-managed agency website built with Django, Django REST Framework, React, Tailwind CSS, and SQLite. The starter identity is intentionally neutral: update **Site settings** in Django Admin before launch.

## Included

- Premium responsive pages for home, about, services, projects, technologies, contact, privacy, terms, and 404 states
- Dynamic services, project case studies, clients, testimonials, technologies, navigation, hero, CTAs, legal pages, social links, and footer content
- Full-screen video carousel with admin-controlled slides, ordering, timing, poster images, overlay strength, publishing, and calls to action
- Admin-managed “Meet Our Team” profiles with name, designation, photo, description, email, and LinkedIn links
- Django Admin with ordering, filtering, search, inlines, publishing controls, and media fields
- REST API with consistent success/error envelopes, public read-only content, contact validation, throttling, and spam honeypot protection
- SQLite for local development and `DATABASE_URL` support for PostgreSQL later
- Loading, empty, validation, network, and not-found states
- SEO metadata, semantic markup, accessible focus states, reduced-motion support, and responsive navigation
- Backend tests, frontend API tests, seed data, and production build commands

## Prerequisites

- Python 3.11 or newer
- Node.js 20 or newer
- npm 10 or newer

## 1. Start the backend

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp backend/.env.example backend/.env
python backend/manage.py migrate
python backend/manage.py seed_content
python backend/manage.py createsuperuser
python backend/manage.py runserver
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item backend\.env.example backend\.env
py backend\manage.py migrate
py backend\manage.py seed_content
py backend\manage.py createsuperuser
py backend\manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/` and Django Admin at `http://127.0.0.1:8000/admin/`.

## 2. Start the frontend

Open a second terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

On Windows PowerShell, replace the copy command with:

```powershell
Copy-Item .env.example .env
```

Open `http://localhost:5173`.

## Customize the website

1. Sign in at `http://127.0.0.1:8000/admin/`.
2. Open **Site settings** and replace the neutral agency name, contact details, SEO defaults, logo, and favicon.
3. Edit the hero, about content, navigation, services, projects, technologies, CTAs, and footer links.
4. Add **Hero video slides**. Use optimized MP4/WebM files up to 60 MB or direct video-file URLs; provide poster images for fast loading and reduced-motion visitors.
5. Add approved profiles under **Team members** and use display order and visibility to control the section.
6. Add real clients and testimonials only when approved. The seed command intentionally creates none.
7. Replace the draft privacy policy and terms with language reviewed for your jurisdiction before launch.

Run `python backend/manage.py seed_content` again only when you want to restore or update the starter content. Existing clients and testimonials are not affected.

## Tests and checks

```bash
python backend/manage.py check
python backend/manage.py test core
cd frontend
npm run test
npm run lint
npm run build
```

## Production checklist

- Set a long random `SECRET_KEY` and keep `DEBUG=False`.
- Configure `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` to exact HTTPS origins.
- Set `DATABASE_URL` to PostgreSQL and run migrations.
- Configure a production email backend and `CONTACT_NOTIFICATION_EMAIL`.
- Serve uploaded media through object storage or a hardened media server.
- Use HTTPS, a reverse proxy, backups, monitoring, and restricted admin access.
- Run `python backend/manage.py check --deploy` and review warnings in the context of your proxy and hosting setup.
- Replace `example.com` in `frontend/public/robots.txt` and `frontend/public/sitemap.xml`, then include live dynamic service and project URLs.

## API routes

Core endpoints include `/api/bootstrap/`, `/api/hero-slides/`, `/api/team/`, `/api/services/`, `/api/projects/`, `/api/clients/`, `/api/testimonials/`, `/api/technologies/`, `/api/pages/`, `/api/site-settings/`, `/api/navigation/`, and `/api/contact/`.

## Project structure

```text
operational-agency-website/
├── backend/
│   ├── config/            # Django configuration
│   ├── core/              # Models, admin, API, validation, tests, seed command
│   └── manage.py
├── frontend/
│   ├── src/api/           # Reusable REST client
│   ├── src/App.jsx        # Routes and reusable site sections
│   └── src/styles.css     # Tailwind layers and responsive visual system
├── requirements.txt
└── README.md
```

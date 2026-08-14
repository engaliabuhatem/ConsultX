# ConsultX

Django site + admin panel for ConsultX Engineering Consultancy. English primary, Arabic (RTL) as a language toggle.

## Status

This is an early checkpoint, not a finished build. See `PROJECT_BRIEF.md` for the open
questions (real contact info, a real project portfolio, and a couple of source-document
conflicts) that still need answers before launch. `HUMAN_TASKS.md` lists everything that
requires a real account, payment, or legal sign-off and can't be done by writing code.

**Done:** project scaffold, all content models, Django admin (Unfold theme), every public
page (home, about, team, services list/detail, projects list/detail with a real empty
state, insights list/detail, contact form with basic rate limiting), EN/AR toggle with
genuine RTL mirroring, a real Tailwind build.

**Not done yet:** rich text editor, drag-and-drop admin ordering, image thumbnails,
bilingual model fields (`django-modeltranslation`), Docker/Nginx/deployment, sitemap.xml
+ robots.txt + Schema.org markup, an automated test suite, and real content — nothing here
is populated with anything beyond what the admin panel needs to hold it.

## Local setup

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements/development.txt

cp .env.example .env   # then fill in DJANGO_SECRET_KEY at minimum

python manage.py migrate
python manage.py createsuperuser

npm install
npm run build:css      # or: npm run watch:css while developing

python manage.py runserver
```

Visit `/` for the site and `/admin/` for the admin panel.

## Rebuilding CSS

Templates use Tailwind utility classes. After editing any template, or `assets/input.css`,
run `npm run build:css` (or leave `npm run watch:css` running) before the style changes
show up — `static/css/output.css` is a build artifact, not something to hand-edit.

## Rate limiting

The contact form's spam guard (`apps/contact/views.py`) uses Django's default cache, which
is per-process. That's fine for a single dev server or a single production worker; with
more than one worker or app server, point `CACHES` at a shared backend (Redis) or switch to
`django-ratelimit`, or each process will enforce its own separate limit.

## Deploying

Use `config.settings.production` and set every variable in `.env.example`'s production
section, especially `DATABASE_URL` and `DJANGO_CSRF_TRUSTED_ORIGINS`. Run
`python manage.py check --deploy` before every release — it should report zero warnings.
Docker/Nginx/Gunicorn configuration isn't written yet (see Status above).

## Project structure

```
config/settings/{base,development,production}.py   — environment-specific settings
apps/core/            — shared abstract models (timestamps, ordering, SEO fields)
apps/siteconfig/      — global site settings singleton (logo, contact, social, footer)
apps/home/            — homepage sections (hero, stats, CTA banner)
apps/services/        — service categories + services
apps/projects/        — project case studies (empty by design — see Status)
apps/team/            — team members, about page
apps/testimonials/    — client testimonials
apps/blog/            — insights: technical articles + whitepapers
apps/contact/         — contact form + inbound submissions
templates/            — base.html, partials/, pages/
assets/input.css      — Tailwind source (not served directly — see "Rebuilding CSS")
```

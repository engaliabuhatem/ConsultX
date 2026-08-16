
## Local setup

```bash
python3 -m venv venv && source venv/bin/activate
# Windows (PowerShell):  py -m venv venv; .\venv\Scripts\Activate.ps1
pip install -r requirements/development.txt

cp .env.example .env   # then fill in DJANGO_SECRET_KEY at minimum

python manage.py migrate
python manage.py createsuperuser

npm install
npm run build:css      # or: npm run watch:css while developing

python manage.py runserver
```

Visit `/` for the site and `/admin/` for the admin panel.

Templates and Python source both define Tailwind classes (see
`apps/core/forms.py`), so **re-run `npm run build:css` after adding classes
in either** — a class that exists only in a `.py` file still needs the
rebuild to reach `static/css/output.css`.

## Public forms

Four public forms write to the database: contact, partner registration
(`/partners/`), job application (`/careers/<slug>/`) and speculative
application (`/careers/apply/`). All four are admin-readable only — the
`ModelAdmin`s set `has_add_permission` to `False`, because a submission is
something that happened, not something staff should be able to author.

Shared pieces live in `apps/core/`: `forms.py` (widget styling),
`ratelimit.py`, `validators.py`, and the `partials/form_field.html` /
`form_field_checkbox.html` templates that carry the accessibility wiring
(label association, `aria-describedby`, `aria-invalid`, `role="alert"`).

### Rate limiting

Each form allows 5 submissions per IP per hour, counted in Django's cache
(`apps/core/ratelimit.py`). This is correct for a single-process dev server.
**In production the cache backend must be a shared store (Redis)** or each
app server will enforce its own separate limit, multiplying the real limit
by the number of servers. `django-ratelimit` is the documented fast-follow
if per-view decorators and better key strategies are wanted.

### Uploads

CVs, cover letters and partner documents are validated on **extension and
size only** (`apps/core/validators.py`, 10 MB, `pdf`/`doc`/`docx`). Neither
check inspects file contents, so neither proves the upload is really a PDF.
That is acceptable while these files are only ever downloaded by staff from
the admin. **If they are ever served to the public, add real content
sniffing (`python-magic`) and serve them from a non-executable location
first.**

Uploads land under `MEDIA_ROOT`, which is not covered by WhiteNoise —
production needs a real media server or object storage in front of it.

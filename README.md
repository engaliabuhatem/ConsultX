
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
in either**. Tailwind's automatic source detection only walks markup, so
`assets/input.css` carries an explicit `@source "../apps/**/*.py"` — without
it, a utility used only in a widget class string is dropped from the build
silently, and only form controls break.

## Design system

Everything visual comes from the approved homepage comp. Tokens, component
classes and textures live in one file, `assets/input.css`:

- **Chrome** — ink `#15150f` on paper `#f2efe4`.
- **Three practice palettes** — A sustainability (gold/forest), B heavy
  infrastructure (clay/grey), C hydraulic authority (teal/mint). A
  `PracticeChapter`'s `palette` field picks one; the template reads it and
  never needs to know which chapter it is drawing.
- **Type** — Bricolage Grotesque for display, Manrope for body and UI,
  Fraunces italic for pull-quote kickers, all from Google Fonts.
- **Legacy token names** (`graphite`, `warm-white`, `accent`, `technical`…)
  still exist and now point at the new palette, so pages written against
  them picked up the redesign without being edited. New work should prefer
  the semantic names (`ink`, `paper`, `gold`, `clay`, `teal`).

`SiteSettings.accent_color` still overrides `--color-accent` site-wide with
no rebuild, exactly as before.

Page structure:

- The homepage (`pages/home.html`) sets `nav_overlay` so the header starts
  transparent over the hero and turns ink-solid on scroll. Every other page
  gets the solid bar from the first frame.
- Every non-homepage view opens with `partials/page_header.html` — pass it
  `eyebrow`, `title`, `subtitle`, and a `width` matching the page's own
  content max-width, or the heading and the content start on different left
  edges. A few detail pages write the same band out inline because they
  carry a back-link or metadata pills the partial has no slot for.
- `static/js/animations.js` draws the pressure-gauge motif, sweeps its
  needle with scroll progress, and runs the reveal observer. All of it is
  gated on `prefers-reduced-motion`, and the CSS is written so content is
  visible even if the JS never runs.

## Admin panel

Django Unfold, themed to the same palette (`UNFOLD` in
`config/settings/base.py`). The `base`/`primary` ramps are OKLCH conversions
of the brand hexes — clay for primary, because Unfold paints white text on
`primary-600` and gold cannot carry white text at any usable lightness. Gold
is applied deliberately, on dark surfaces only, in `static/css/admin.css`.

The sidebar is grouped the way the *site* is organised rather than by app
label, and `templates/admin/index.html` replaces Unfold's bare app list with
a dashboard: what needs attention (unhandled counts, not totals), how much
of the site is filled in (each tile links to its own "add" screen), and the
latest enquiries. Its data comes from `apps/core/dashboard.py`.

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

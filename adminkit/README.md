# adminkit

A portable Django admin skin: the ConsultX admin's look, dashboard and sidebar
with every ConsultX-specific value pulled out into arguments.

Copy the `adminkit/` directory into another Django project and you get the same
admin in about fifteen minutes. Nothing in here imports a project model or
hardcodes a project color.

---

## What is in it

| File | Does |
|---|---|
| `palette.py` | Brand hex → the eleven-step OKLCH ramps Unfold wants |
| `theme.py` | `build_unfold()` — assembles the whole `UNFOLD` settings dict |
| `nav.py` | `group()` / `item()` — sidebar entries without hand-typed URL names |
| `dashboard.py` | `Dashboard` / `Attention` / `Tile` / `Recent` — the landing page, declared |
| `templates/admin/index.html` | The landing page itself. Names no model |
| `static/adminkit/css/adminkit.css` | Components + chrome, every color a CSS variable |
| `tests.py` | 37 tests, using only models that ship with Django |

---

## Install

**1. Dependency**

```
django-unfold==0.104.1
```

**2. Copy the folder** into the project root, next to `manage.py`.

**3. `INSTALLED_APPS`** — order is load-bearing. `adminkit` must precede
`unfold` so its `admin/index.html` wins; `unfold` must precede
`django.contrib.admin` or Unfold's templates never load at all.

```python
INSTALLED_APPS = [
    "adminkit",
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    ...
]
```

**4. Sidebar and `UNFOLD`**, in `settings.py`:

```python
from adminkit.nav import dashboard_item, group, item
from adminkit.theme import build_unfold

ADMIN_NAVIGATION = [
    group("Overview", [
        dashboard_item(),
        item("siteconfig.SiteSettings", "Site settings", icon="tune"),
    ]),
    group("Catalogue", [
        item("shop.Product", "Products", icon="inventory_2"),
        item("shop.Category", "Categories", icon="category"),
    ]),
]

UNFOLD = build_unfold(
    title="Acme Admin",
    header="Acme",
    subheader="Content & Orders",
    brand="#2563eb",     # accent — drives the whole primary ramp
    neutral="#f4f4f5",   # tints the greys
    navigation=ADMIN_NAVIGATION,
    dashboard_callback="apps.core.dashboard.dashboard_callback",
    extra_styles=["css/admin-brand.css"],
)
```

Models are named as `"app_label.ModelName"` strings, not imported classes:
`settings.py` is read before the app registry is populated, so importing a
model there raises `AppRegistryNotReady`.

Icons are [Material Symbols](https://fonts.google.com/icons) names.

**5. Dashboard** — `apps/core/dashboard.py`:

```python
from adminkit.dashboard import Attention, Dashboard, Recent, Tile
from apps.shop.models import Order, Product

dashboard_callback = Dashboard(
    attention=[
        Attention(Order, "Unfulfilled orders", where={"status": "new"}),
    ],
    tiles=[Tile(Product, "Products")],
    recent=Recent(
        Order, order_by="-placed_at", title="Latest orders",
        label_field="reference", meta_field="customer_name",
        date_field="placed_at", unread_field="is_handled",
    ),
).as_callback()
```

Here models *are* imported directly — this module is loaded on request, long
after the registry is ready.

`where={...}` is used twice: to count the rows, and to build the changelist
link. Booleans become `__exact=0/1` and bare keys get `__exact`, so the number
on the card and the rows on the page it opens always match.

**6. Brand file** — `static/css/admin-brand.css`. Variables only:

```css
:root {
  --ak-accent-1: #fad02c;   /* also the focus ring — keep this one bright */
  --ak-accent-2: #9c5539;
  --ak-accent-3: #48a899;
  --ak-hero-from: #0a0b08;
  --ak-hero-to: #2c5043;
  --ak-display: "Bricolage Grotesque", ui-sans-serif, system-ui, sans-serif;
}
html.dark {
  --ak-text: #f2efe4;
  --ak-text-soft: rgb(242 239 228 / 0.6);
}
```

The full variable list is documented at the top of `adminkit.css`. Never edit
`adminkit.css` itself — that is what makes the next copy a copy rather than a
fork.

**7. Every `admin.py`** in the project swaps one import:

```python
from unfold.admin import ModelAdmin, TabularInline, StackedInline
```

instead of the `django.contrib.admin` versions. This is the step that themes
each changelist and edit form. Miss it on one model and that screen renders as
unstyled Django admin — the fastest way to check is to click through the
sidebar once.

---

## Choosing the two colors

`brand` and `neutral` are the only color decisions.

- **brand** — your accent. Unfold paints white text on `primary-600`, so the
  ramp pins that step near L 53% and darkens a light brand color to reach it.
  A yellow passed as `brand` comes out as a usable dark amber, not yellow; if
  you want the yellow itself, put it in `--ak-accent-1` and give `brand`
  something that can carry white text.
- **neutral** — a near-grey whose *hue* tints the admin greys. Pass your page
  background. A warm paper makes the greys warm; `tint=0` gives pure grey.

Preview a ramp without booting the site:

```
python -c "from adminkit.palette import primary_ramp; print(primary_ramp('#2563eb'))"
```

---

## Verify

```
python manage.py test adminkit
```

37 tests: the palette math (including that `primary-600` can always carry white
text), the query-param translation, the dashboard cards, the sidebar
references, and that the landing page renders adminkit's template rather than
Unfold's. They use only `auth.User` and `contenttypes.ContentType`, so they
pass in a fresh project on day one.

Then log in and check the four things the tests cannot see: the sidebar groups,
the dashboard, dark mode (the toggle, top right), and one changelist plus one
edit form.

---

## Notes

- **Overriding the landing page.** A project that wants a different one puts its
  own `templates/admin/index.html` in a `TEMPLATES["DIRS"]` directory, which
  outranks every app template.
- **Unregistered models.** Cards for models absent from the admin render
  without a link rather than raising. The dashboard is the first page staff see
  after login; it must never be the thing that takes the admin down.
- **Anything Unfold supports** that `build_unfold()` has no argument for can be
  passed as an extra keyword — `build_unfold(title="A", TABS=[...])` — or
  assigned onto the returned dict afterwards.

"""
Declarative admin dashboard.

The hand-written version of this file counted rows model by model, which meant
every new project rewrote the same twenty lines. Here you describe the cards and
the callback is generated:

    from adminkit.dashboard import Dashboard, Attention, Tile, Recent
    from apps.contact.models import ContactSubmission
    from apps.services.models import Service

    dashboard_callback = Dashboard(
        attention=[
            Attention(ContactSubmission, "Unread enquiries", where={"is_read": False}),
        ],
        tiles=[Tile(Service, "Services")],
        recent=Recent(ContactSubmission, order_by="-submitted_at"),
    ).as_callback()

Then point UNFOLD["DASHBOARD_CALLBACK"] at it.

Every URL lookup is guarded: a model that is not registered in the admin yields
a card without a link rather than a 500. The dashboard is the first page staff
see after login and must never be the thing that takes the admin down.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from django.db.models import Model, QuerySet
from django.urls import NoReverseMatch, reverse

__all__ = ["Dashboard", "Attention", "Tile", "Recent", "changelist_url", "add_url"]

# Accent slots, not color names: the stylesheet maps a1/a2/a3 onto whatever the
# consuming project set --ak-accent-1/2/3 to. Naming these "gold" and "teal"
# was what made the original impossible to reuse.
TONES = ("a1", "a2", "a3")


def _admin_url(model: type[Model], action: str) -> str | None:
    meta = model._meta
    try:
        return reverse(f"admin:{meta.app_label}_{meta.model_name}_{action}")
    except NoReverseMatch:
        return None


def _as_query(where: dict[str, Any]) -> str:
    """Translate an ORM-style filter dict into changelist query params, so the
    card and the page it links to always show the same set of rows.

    `{"is_read": False}` -> `is_read__exact=0`; a key that already carries a
    lookup (`status__in`) is passed through untouched.
    """
    parts = []
    for key, value in where.items():
        param = key if "__" in key else f"{key}__exact"
        if isinstance(value, bool):
            value = int(value)
        parts.append(f"{param}={value}")
    return "&".join(parts)


def changelist_url(model: type[Model], **where: Any) -> str | None:
    url = _admin_url(model, "changelist")
    if url and where:
        url += "?" + _as_query(where)
    return url


def add_url(model: type[Model]) -> str | None:
    return _admin_url(model, "add")


@dataclass
class Attention:
    """A "needs attention" card: an outstanding count against a total."""

    model: type[Model]
    label: str
    where: dict[str, Any] = field(default_factory=dict)
    tone: str | None = None  # defaults to position in the list

    def render(self, index: int) -> dict[str, Any]:
        outstanding = self.model._default_manager.filter(**self.where).count()
        return {
            "label": self.label,
            "value": outstanding,
            "total": self.model._default_manager.count(),
            "url": changelist_url(self.model, **self.where),
            "tone": self.tone or TONES[index % len(TONES)],
        }


@dataclass
class Tile:
    """A content tile: how many rows exist, plus a shortcut to add one."""

    model: type[Model]
    label: str | None = None
    where: dict[str, Any] = field(default_factory=dict)

    def render(self) -> dict[str, Any]:
        manager = self.model._default_manager
        return {
            "label": self.label or self.model._meta.verbose_name_plural.title(),
            "value": manager.filter(**self.where).count() if self.where else manager.count(),
            "url": changelist_url(self.model, **self.where),
            "add": add_url(self.model),
        }


@dataclass
class Recent:
    """The short "latest activity" list under the tiles.

    `fields` are the model attributes the template may read. They are passed to
    .only() so the list costs one narrow query however wide the model is.
    """

    model: type[Model]
    order_by: str = "-pk"
    limit: int = 5
    title: str = "Latest activity"
    fields: Sequence[str] = ()
    # Attribute holding a date, and a boolean marking a row as already handled.
    # Both optional — the template skips whatever is missing.
    date_field: str | None = None
    unread_field: str | None = None
    label_field: str = "__str__"
    meta_field: str | None = None

    def render(self) -> list[dict[str, Any]]:
        qs: QuerySet = self.model._default_manager.order_by(self.order_by)
        wanted = [f for f in (*self.fields, self.date_field, self.unread_field,
                              self.meta_field, self.label_field)
                  if f and f != "__str__"]
        if wanted:
            qs = qs.only(*dict.fromkeys(wanted))
        rows = []
        for obj in qs[: self.limit]:
            rows.append({
                "label": str(obj) if self.label_field == "__str__"
                         else getattr(obj, self.label_field, ""),
                "meta": getattr(obj, self.meta_field, "") if self.meta_field else "",
                "date": getattr(obj, self.date_field, None) if self.date_field else None,
                "handled": bool(getattr(obj, self.unread_field, False))
                           if self.unread_field else False,
            })
        return rows


@dataclass
class Dashboard:
    attention: Sequence[Attention] = ()
    tiles: Sequence[Tile] = ()
    recent: Recent | None = None
    greeting: str = "Welcome back, {name}."
    tiles_title: str = "Site content"
    attention_title: str = "Needs attention"

    def as_callback(self) -> Callable[[Any, dict], dict]:
        """Return a function suitable for UNFOLD['DASHBOARD_CALLBACK']."""

        def dashboard_callback(request, context):
            cards = [card.render(i) for i, card in enumerate(self.attention)]
            context["ak_attention"] = cards
            context["ak_attention_total"] = sum(c["value"] for c in cards)
            context["ak_attention_title"] = self.attention_title
            context["ak_tiles"] = [tile.render() for tile in self.tiles]
            context["ak_tiles_title"] = self.tiles_title
            context["ak_recent"] = self.recent.render() if self.recent else []
            context["ak_recent_title"] = self.recent.title if self.recent else ""
            # Formatted here rather than in the template: Django templates have
            # no str.format, and the greeting is a project-supplied string.
            user = request.user
            context["ak_greeting"] = self.greeting.format(
                name=user.get_short_name() or user.get_username()
            )
            return context

        return dashboard_callback

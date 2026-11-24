"""
Sidebar helpers.

Unfold's SIDEBAR navigation wants a reversed admin URL per item, spelled
`admin:<app_label>_<modelname>_changelist`. Typing that string by hand is the
single most common way to break this config: it fails at import time with a
NoReverseMatch that names a URL, not the menu entry that asked for it.

    from adminkit.nav import group, item, dashboard_item

    NAVIGATION = [
        group("Overview", [dashboard_item()]),
        group("Expertise", [item("services.Service", "Services", icon="engineering")]),
    ]

Models are named as "app_label.ModelName" strings rather than imported classes
because this list is built inside the settings module, which Django imports
before the app registry is populated — importing a model there raises
AppRegistryNotReady. A model class is accepted too, for callers building the
list somewhere later in the boot sequence.

Icons are Google Material Symbols names — https://fonts.google.com/icons.
"""

from typing import Any, Callable, Sequence

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

__all__ = ["group", "item", "link", "dashboard_item"]


def _route(model: Any) -> tuple[str, str]:
    """('services.Service' | Service) -> ('services', 'service')."""
    if isinstance(model, str):
        try:
            app_label, model_name = model.split(".")
        except ValueError:
            raise ValueError(
                f"expected 'app_label.ModelName', got {model!r}"
            ) from None
        return app_label.lower(), model_name.lower()
    meta = model._meta
    return meta.app_label, meta.model_name


def group(title: str, items: Sequence[dict], *, collapsible: bool = False) -> dict:
    entry = {"title": _(title), "items": list(items)}
    if collapsible:
        entry["collapsible"] = True
    return entry


def item(model: Any, title: str | None = None, *, icon: str = "list",
         action: str = "changelist",
         permission: str | Callable[[Any], bool] | None = None) -> dict:
    """A menu entry pointing at a model's admin page.

    `model` is "app_label.ModelName" or a model class. `title` is required for
    string refs — the verbose name cannot be read without importing the model.
    """
    app_label, model_name = _route(model)
    if title is None:
        if isinstance(model, str):
            raise ValueError(f"a title is required for the string reference {model!r}")
        title = str(model._meta.verbose_name_plural).title()
    entry = {
        "title": _(title),
        "icon": icon,
        "link": reverse_lazy(f"admin:{app_label}_{model_name}_{action}"),
    }
    if permission is not None:
        entry["permission"] = permission
    return entry


def link(title: str, url_name: str, *, icon: str = "link", **kwargs) -> dict:
    """A menu entry pointing at any named URL — a custom admin view, a report."""
    return {"title": _(title), "icon": icon, "link": reverse_lazy(url_name, kwargs=kwargs or None)}


def dashboard_item(title: str = "Dashboard", *, icon: str = "dashboard") -> dict:
    return {"title": _(title), "icon": icon, "link": reverse_lazy("admin:index")}

"""
One call that builds the whole UNFOLD settings dict.

    from adminkit.theme import build_unfold

    UNFOLD = build_unfold(
        title="Acme Admin",
        header="Acme",
        brand="#2563eb",
        neutral="#f4f4f5",
        navigation=NAVIGATION,
        dashboard_callback="apps.core.dashboard.dashboard_callback",
    )

Anything Unfold supports that is not spelled out as an argument can be passed
through as **extra, and anything here can be overridden afterwards by assigning
into the returned dict. See django-unfold's own docs for the full option list.
"""

from typing import Any, Sequence

from django.templatetags.static import static

from .palette import ramps

__all__ = ["build_unfold"]


def build_unfold(
    *,
    title: str,
    header: str | None = None,
    subheader: str = "",
    brand: str = "#9c5539",
    neutral: str = "#f2efe4",
    saturation: float = 1.0,
    tint: float = 1.0,
    navigation: Sequence[dict] = (),
    dashboard_callback: str | None = None,
    site_url: str = "/",
    site_symbol: str = "domain",
    login_image: str | None = None,
    extra_styles: Sequence[str] = (),
    border_radius: str = "8px",
    show_history: bool = True,
    **extra: Any,
) -> dict:
    """Assemble UNFOLD.

    `brand` drives the accent ramp and `neutral` the greys — see palette.py for
    why those two hex values are enough. `extra_styles` are static paths loaded
    after adminkit's own stylesheet, which is where a project's brand variable
    overrides go.
    """
    styles = ["adminkit/css/adminkit.css", *extra_styles]

    config: dict[str, Any] = {
        "SITE_TITLE": title,
        "SITE_HEADER": header or title,
        "SITE_SUBHEADER": subheader,
        "SITE_SYMBOL": site_symbol,
        "SITE_URL": site_url,
        "SHOW_HISTORY": show_history,
        "SHOW_VIEW_ON_SITE": True,
        "SHOW_BACK_BUTTON": True,
        "BORDER_RADIUS": border_radius,
        # Late binding through a lambda: static() needs the staticfiles app
        # ready, and settings are imported before that happens.
        "STYLES": [(lambda path: (lambda request: static(path)))(p) for p in styles],
        "COLORS": ramps(brand, neutral, saturation=saturation, tint=tint),
        "SIDEBAR": {
            "show_search": True,
            "show_all_applications": True,
            "navigation": list(navigation),
        },
    }
    if dashboard_callback:
        config["DASHBOARD_CALLBACK"] = dashboard_callback
    if login_image:
        config["LOGIN"] = {"image": (lambda p: (lambda request: static(p)))(login_image)}

    config.update(extra)
    return config

"""
Single source of truth for the primary navigation.

The desktop bar (disclosure dropdowns) and the mobile drawer (accordion)
need structurally different markup, so they cannot share one template
partial the way a flat list could. Defining the tree here instead means the
two renderings still cannot drift apart — they loop the same data.

Grouping follows the standard engineering-consultancy IA (Arup, AECOM, WSP
and peers all converge on it): what we know, what we've built, what we've
written, how to engage. Ten flat links become seven top-level items, five of
which are single words.

URLs are reversed per request, never at import time — i18n_patterns makes
reverse() language-dependent, so a module-level constant would freeze every
link to whichever language happened to load first.
"""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

#: label      visible text
#: url        url name to reverse
#: match      view names marking this item current. A trailing ":" means
#:            "any view in this namespace" (so /services/foo/ still lights
#:            up Services); anything else is matched exactly, which is what
#:            team needs since it owns both About and Leadership.
#: blurb      one-line description shown under the link in the dropdown
#: key        stable id fragment for aria-controls
NAV_TREE = [
    {
        "label": _("Home"),
        "url": "home:index",
        "match": ("home:index",),
    },
    {
        "label": _("About"),
        "key": "about",
        "children": [
            {
                "label": _("About Us"),
                "url": "team:about",
                "match": ("team:about",),
                "blurb": _("Who we are and how we work."),
            },
            {
                "label": _("Leadership"),
                "url": "team:leadership",
                "match": ("team:leadership",),
                "blurb": _("The people accountable for our engineering."),
            },
        ],
    },
    {
        "label": _("Expertise"),
        "key": "expertise",
        "children": [
            {
                "label": _("Services"),
                "url": "services:list",
                "match": ("services:",),
                "blurb": _("The disciplines we deliver."),
            },
            {
                "label": _("Sectors"),
                "url": "sectors:list",
                "match": ("sectors:",),
                "blurb": _("The industries we deliver them into."),
            },
        ],
    },
    {
        "label": _("Projects"),
        "url": "projects:list",
        "match": ("projects:",),
    },
    {
        "label": _("Insights"),
        "key": "insights",
        "children": [
            {
                "label": _("Publications"),
                "url": "publications:list",
                "match": ("publications:",),
                "blurb": _("Whitepapers and technical reports to download."),
            },
            {
                "label": _("Articles"),
                "url": "blog:list",
                "match": ("blog:",),
                "blurb": _("Shorter technical writing from the team."),
            },
        ],
    },
    {
        "label": _("Work With Us"),
        "key": "work-with-us",
        "children": [
            {
                "label": _("Careers"),
                "url": "careers:list",
                "match": ("careers:",),
                "blurb": _("Open roles, and speculative applications."),
            },
            {
                "label": _("Become a Partner"),
                "url": "partners:index",
                "match": ("partners:",),
                "blurb": _("Register your firm as a partner or supplier."),
            },
        ],
    },
    {
        "label": _("Contact Us"),
        "url": "contact:index",
        "match": ("contact:",),
        "cta": True,
    },
]


def _is_current(view_name, patterns):
    """A trailing ":" makes a pattern a namespace prefix; otherwise exact."""
    if not view_name:
        return False
    return any(
        view_name.startswith(p) if p.endswith(":") else view_name == p
        for p in patterns
    )


def _resolve_leaf(item, view_name):
    return {
        "label": item["label"],
        "url": reverse(item["url"]),
        "blurb": item.get("blurb", ""),
        "is_current": _is_current(view_name, item["match"]),
    }


def build_nav(request):
    """Resolve NAV_TREE against the current request."""
    match = getattr(request, "resolver_match", None)
    view_name = match.view_name if match else None

    items = []
    for entry in NAV_TREE:
        if "children" in entry:
            children = [_resolve_leaf(child, view_name) for child in entry["children"]]
            items.append({
                "label": entry["label"],
                "key": entry["key"],
                "children": children,
                # A group is current when any child is — so the top-level
                # label stays highlighted while you're inside the section.
                "is_current": any(c["is_current"] for c in children),
                "is_group": True,
            })
        else:
            items.append({
                "label": entry["label"],
                "url": reverse(entry["url"]),
                "is_current": _is_current(view_name, entry["match"]),
                "is_group": False,
                "cta": entry.get("cta", False),
            })
    return items


def navigation(request):
    """Context processor — exposes {{ nav_items }} to every template."""
    return {"nav_items": build_nav(request)}

"""
Shared IP rate limiting for public form submissions.

Lifted out of apps/contact/views.py now that three public forms need it.
Same caveat as before: correct for a single-process dev server, but in
production the cache backend must be a shared store (Redis) or each app
server enforces its own separate limit. See README "Rate limiting".
"""

from django.core.cache import cache


def client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")


def is_rate_limited(request, scope, limit, window_seconds):
    """True if this IP has already hit `limit` submissions for `scope`."""
    return cache.get(f"{scope}_rate:{client_ip(request)}", 0) >= limit


def record_submission(request, scope, window_seconds):
    """Count one submission against this IP's budget for `scope`."""
    key = f"{scope}_rate:{client_ip(request)}"
    cache.set(key, cache.get(key, 0) + 1, window_seconds)

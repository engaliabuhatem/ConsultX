from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect, render

from .forms import ContactForm

RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW_SECONDS = 60 * 60


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")


def contact_view(request):
    """
    Basic anti-spam rate limit using Django's cache framework: 5 submissions
    per IP per hour. This is correct for a single-process dev server; in
    production the cache backend must be a shared store (Redis) — see
    README "Rate limiting" note — or each app server enforces its own
    separate limit. django-ratelimit is a documented fast-follow if
    something more robust (form + view decorators, better key strategies)
    is needed later.
    """
    if request.method == "POST":
        cache_key = f"contact_rate:{_client_ip(request)}"
        submissions = cache.get(cache_key, 0)
        if submissions >= RATE_LIMIT_MAX:
            messages.error(request, "Too many submissions — please try again later.")
            return redirect("contact:index")

        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            cache.set(cache_key, submissions + 1, RATE_LIMIT_WINDOW_SECONDS)
            messages.success(request, "Thanks — we'll be in touch shortly.")
            return redirect("contact:index")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})

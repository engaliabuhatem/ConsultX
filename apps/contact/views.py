from django.contrib import messages
from django.shortcuts import redirect, render

from apps.core.ratelimit import is_rate_limited, record_submission

from .forms import ContactForm

RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW_SECONDS = 60 * 60
RATE_LIMIT_SCOPE = "contact"


def contact_view(request):
    """
    Anti-spam rate limit: 5 submissions per IP per hour. The mechanics now
    live in apps/core/ratelimit.py, shared with the careers and partner
    forms — see that module for the production caveat about needing a
    shared cache backend.
    """
    if request.method == "POST":
        if is_rate_limited(request, RATE_LIMIT_SCOPE, RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_SECONDS):
            messages.error(request, "Too many submissions — please try again later.")
            return redirect("contact:index")

        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            record_submission(request, RATE_LIMIT_SCOPE, RATE_LIMIT_WINDOW_SECONDS)
            messages.success(request, "Thanks — we'll be in touch shortly.")
            return redirect("contact:index")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})

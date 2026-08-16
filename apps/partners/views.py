from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from apps.core.ratelimit import is_rate_limited, record_submission

from .forms import PartnerApplicationForm

RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW_SECONDS = 60 * 60
RATE_LIMIT_SCOPE = "partners"


def partner_view(request):
    if request.method == "POST":
        if is_rate_limited(request, RATE_LIMIT_SCOPE, RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_SECONDS):
            messages.error(request, _("Too many submissions — please try again later."))
            return redirect("partners:index")

        form = PartnerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            record_submission(request, RATE_LIMIT_SCOPE, RATE_LIMIT_WINDOW_SECONDS)
            messages.success(
                request,
                _("Thank you — we've received your details and will be in touch about next steps."),
            )
            return redirect("partners:index")
    else:
        form = PartnerApplicationForm()

    return render(request, "pages/partners.html", {"form": form})

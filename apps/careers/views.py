from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.generic import ListView

from apps.core.ratelimit import is_rate_limited, record_submission

from .forms import JobApplicationForm
from .models import JobOpening

RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW_SECONDS = 60 * 60
RATE_LIMIT_SCOPE = "careers"


class JobOpeningListView(ListView):
    model = JobOpening
    template_name = "pages/careers_list.html"
    context_object_name = "openings"

    def get_queryset(self):
        # Closed roles are hidden rather than greyed out — a role that can't
        # be applied to is noise on a careers page.
        return JobOpening.objects.filter(is_open=True)


def _handle_application(request, opening, template, extra_context=None):
    """Shared POST handling for both the per-role and speculative forms."""
    if request.method == "POST":
        if is_rate_limited(request, RATE_LIMIT_SCOPE, RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_SECONDS):
            messages.error(request, _("Too many applications submitted — please try again later."))
            return redirect(request.path)

        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.position = opening
            application.save()
            record_submission(request, RATE_LIMIT_SCOPE, RATE_LIMIT_WINDOW_SECONDS)
            messages.success(
                request,
                _("Thank you — your application has been received. We review every submission."),
            )
            return redirect(request.path)
    else:
        form = JobApplicationForm()

    context = {"form": form, "opening": opening}
    context.update(extra_context or {})
    return render(request, template, context)


def job_detail_view(request, slug):
    opening = get_object_or_404(JobOpening, slug=slug, is_open=True)
    if not opening.accepts_applications:
        # Open but past its closing date: still readable, no form.
        return render(request, "pages/career_detail.html", {"opening": opening, "form": None})
    return _handle_application(request, opening, "pages/career_detail.html")


def general_application_view(request):
    """Speculative application, not tied to any advertised role."""
    return _handle_application(request, None, "pages/career_apply.html")

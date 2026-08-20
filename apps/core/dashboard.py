from django.urls import NoReverseMatch, reverse

from apps.blog.models import Post
from apps.careers.models import JobApplication, JobOpening
from apps.contact.models import ContactSubmission
from apps.home.models import PracticeChapter
from apps.partners.models import PartnerApplication
from apps.projects.models import Project
from apps.sectors.models import Sector
from apps.services.models import Service
from apps.team.models import TeamMember


def _changelist(model, **params):
    """URL of a model's changelist, optionally filtered. Returns None rather
    than raising if the model isn't registered — the dashboard should never
    be the thing that takes the admin down."""
    meta = model._meta
    try:
        url = reverse(f"admin:{meta.app_label}_{meta.model_name}_changelist")
    except NoReverseMatch:
        return None
    if params:
        url += "?" + "&".join(f"{k}={v}" for k, v in params.items())
    return url


def _addlink(model):
    meta = model._meta
    try:
        return reverse(f"admin:{meta.app_label}_{meta.model_name}_add")
    except NoReverseMatch:
        return None


def dashboard_callback(request, context):
    unread_enquiries = ContactSubmission.objects.filter(is_read=False).count()
    new_applications = JobApplication.objects.filter(status="new").count()
    new_partners = PartnerApplication.objects.filter(status="new").count()

    context["inbox"] = [
        {
            "label": "Unread enquiries",
            "value": unread_enquiries,
            "total": ContactSubmission.objects.count(),
            "url": _changelist(ContactSubmission, is_read__exact=0),
            "tone": "gold",
        },
        {
            "label": "New job applications",
            "value": new_applications,
            "total": JobApplication.objects.count(),
            "url": _changelist(JobApplication, status__exact="new"),
            "tone": "clay",
        },
        {
            "label": "New partner applications",
            "value": new_partners,
            "total": PartnerApplication.objects.count(),
            "url": _changelist(PartnerApplication, status__exact="new"),
            "tone": "teal",
        },
    ]
    context["inbox_total"] = unread_enquiries + new_applications + new_partners

    context["content"] = [
        {"label": "Services", "value": Service.objects.count(),
         "url": _changelist(Service), "add": _addlink(Service)},
        {"label": "Sectors", "value": Sector.objects.count(),
         "url": _changelist(Sector), "add": _addlink(Sector)},
        {"label": "Projects", "value": Project.objects.count(),
         "url": _changelist(Project), "add": _addlink(Project)},
        {"label": "Team members", "value": TeamMember.objects.count(),
         "url": _changelist(TeamMember), "add": _addlink(TeamMember)},
        {"label": "Insight posts", "value": Post.objects.count(),
         "url": _changelist(Post), "add": _addlink(Post)},
        {"label": "Open roles", "value": JobOpening.objects.filter(is_open=True).count(),
         "url": _changelist(JobOpening), "add": _addlink(JobOpening)},
        {"label": "Chapters", "value": PracticeChapter.objects.count(),
         "url": _changelist(PracticeChapter), "add": _addlink(PracticeChapter)},
    ]

    context["latest_enquiries"] = (
        ContactSubmission.objects.order_by("-submitted_at")
        .only("name", "company", "submitted_at", "is_read")[:5]
    )
    return context

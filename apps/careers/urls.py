from django.urls import path

from .views import JobOpeningListView, general_application_view, job_detail_view

app_name = "careers"
urlpatterns = [
    path("", JobOpeningListView.as_view(), name="list"),
    # Sits above <slug:slug> so "apply" is never captured as a role slug.
    path("apply/", general_application_view, name="apply"),
    path("<slug:slug>/", job_detail_view, name="detail"),
]

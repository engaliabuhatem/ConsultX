from django.urls import path

from .views import PublicationDetailView, PublicationListView

app_name = "publications"
urlpatterns = [
    path("", PublicationListView.as_view(), name="list"),
    path("<slug:slug>/", PublicationDetailView.as_view(), name="detail"),
]

from django.urls import path

from .views import SectorDetailView, SectorListView

app_name = "sectors"
urlpatterns = [
    path("", SectorListView.as_view(), name="list"),
    path("<slug:slug>/", SectorDetailView.as_view(), name="detail"),
]

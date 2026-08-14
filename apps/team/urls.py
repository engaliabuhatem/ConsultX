from django.urls import path

from .views import AboutView, TeamListView

app_name = "team"
urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("team/", TeamListView.as_view(), name="list"),
]

from django.urls import path

from .views import AboutView, LeadershipListView, TeamListView

app_name = "team"
urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("team/", TeamListView.as_view(), name="list"),
    path("leadership/", LeadershipListView.as_view(), name="leadership"),
]

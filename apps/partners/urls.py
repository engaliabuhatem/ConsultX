from django.urls import path

from .views import partner_view

app_name = "partners"
urlpatterns = [
    path("", partner_view, name="index"),
]

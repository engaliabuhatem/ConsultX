from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ("client_name", "project", "is_published", "order")
    list_editable = ("order",)
    list_filter = ("is_published",)
    search_fields = ("client_name", "quote")
    ordering = ("order",)

from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Sector


@admin.register(Sector)
class SectorAdmin(ModelAdmin):
    list_display = ("name", "is_featured", "order")
    list_editable = ("order",)
    list_filter = ("is_featured",)
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("related_services",)
    fieldsets = (
        (None, {"fields": ("name", "slug", "is_featured", "order")}),
        ("Content", {"fields": ("short_description", "description", "icon", "image")}),
        ("Related", {"fields": ("related_services",)}),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "canonical_url"),
        }),
    )

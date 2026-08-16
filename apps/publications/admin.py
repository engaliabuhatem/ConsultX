from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
    list_display = ("title", "category", "published_date", "is_published")
    list_filter = ("category", "is_published", "published_date")
    search_fields = ("title", "abstract")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("authors",)
    date_hierarchy = "published_date"
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "published_date", "is_published")}),
        ("Content", {"fields": ("abstract", "pdf_file", "cover_image", "authors")}),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "canonical_url"),
        }),
    )

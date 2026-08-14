from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import InsightCategory, Post


@admin.register(InsightCategory)
class InsightCategoryAdmin(ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("title", "content_type", "category", "author", "is_published", "published_at")
    list_filter = ("content_type", "category", "is_published")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "content_type", "author")}),
        ("Content", {"fields": ("excerpt", "content", "featured_image", "whitepaper_file")}),
        ("Publishing", {"fields": ("is_published", "published_at")}),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "canonical_url"),
        }),
    )

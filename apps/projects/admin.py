from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Project, ProjectImage


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        "title", "client_display", "category", "date_completed", "is_published", "order",
    )
    list_editable = ("order",)
    list_filter = ("category", "is_published", "is_confidential")
    search_fields = ("title", "client_name", "location")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "order", "is_published")}),
        ("Client", {"fields": ("client_name", "is_confidential", "location")}),
        ("Scope", {"fields": ("role", "scope", "date_completed", "cover_image")}),
        ("Case study", {"fields": ("challenge", "response", "outcome")}),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "canonical_url"),
        }),
    )

    @admin.display(description="Client")
    def client_display(self, obj):
        return "Confidential" if obj.is_confidential else (obj.client_name or "—")

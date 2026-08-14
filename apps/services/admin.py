from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Service, ServiceCategory, ServiceFeature


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order",)


class ServiceFeatureInline(TabularInline):
    model = ServiceFeature
    extra = 1


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ("title", "category", "is_featured", "order")
    list_editable = ("order",)
    list_filter = ("category", "is_featured")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceFeatureInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "is_featured", "order")}),
        ("Content", {"fields": ("short_description", "description", "icon", "image")}),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "canonical_url"),
        }),
    )

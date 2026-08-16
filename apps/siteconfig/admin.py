from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("logo", "favicon", "accent_color")}),
        ("Contact", {"fields": ("contact_phone", "contact_email", "contact_address")}),
        ("Social", {"fields": ("linkedin_url", "x_url", "instagram_url", "youtube_url")}),
        ("Footer", {"fields": ("footer_text", "professional_indemnity_notice")}),
        ("Default SEO", {"fields": (
            "default_meta_title", "default_meta_description", "og_image", "canonical_url",
        )}),
    )

    def has_add_permission(self, request):
        # Singleton — block "Add" once a row exists so staff can't create a second one.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

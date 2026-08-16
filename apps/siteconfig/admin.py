from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = "__all__"
        widgets = {
            "custom_css": forms.Textarea(attrs={
                "rows": 16,
                "spellcheck": "false",
                "style": "font-family: ui-monospace, monospace; font-size: 13px; "
                         "white-space: pre;",
                "placeholder": ".hero h1 {\n  font-size: 3rem;\n}",
            }),
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    form = SiteSettingsForm
    fieldsets = (
        ("Branding", {"fields": ("logo", "favicon", "accent_color")}),
        ("Advanced: Custom CSS", {
            "classes": ("collapse",),
            "fields": ("custom_css",),
            "description": "For anyone comfortable writing CSS. This is added to every page "
                            "after everything else, so it can override any style on the site.",
        }),
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

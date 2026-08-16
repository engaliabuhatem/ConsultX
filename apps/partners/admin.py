from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import PartnerApplication


@admin.register(PartnerApplication)
class PartnerApplicationAdmin(ModelAdmin):
    list_display = (
        "company_name", "country", "partnership_type",
        "has_conflict_of_interest", "status", "created_at",
    )
    list_filter = (
        "status", "partnership_type", "country",
        "has_professional_indemnity", "has_conflict_of_interest", "created_at",
    )
    search_fields = ("company_name", "contact_name", "contact_email", "capabilities")
    list_editable = ("status",)
    date_hierarchy = "created_at"
    filter_horizontal = ("sectors",)

    readonly_fields = (
        "company_name", "registration_number", "tax_id", "website", "country", "city",
        "year_established", "employee_count", "contact_name", "contact_title",
        "contact_email", "contact_phone", "partnership_type", "capabilities",
        "key_clients", "annual_turnover", "certifications", "has_professional_indemnity",
        "has_conflict_of_interest", "conflict_details", "company_profile_file",
        "trade_licence_file", "message", "consent", "created_at",
    )
    fieldsets = (
        ("Triage", {"fields": ("status", "notes")}),
        ("Company", {
            "fields": ("company_name", "registration_number", "tax_id", "website",
                       "country", "city", "year_established", "employee_count", "created_at"),
        }),
        ("Contact", {"fields": ("contact_name", "contact_title", "contact_email", "contact_phone")}),
        ("Capability", {
            "fields": ("partnership_type", "sectors", "capabilities", "key_clients", "annual_turnover"),
        }),
        ("Standing", {
            "fields": ("certifications", "has_professional_indemnity",
                       "has_conflict_of_interest", "conflict_details"),
        }),
        ("Documents", {"fields": ("company_profile_file", "trade_licence_file")}),
        ("Meta", {"fields": ("message", "consent")}),
    )

    def has_add_permission(self, request):
        # Applications only ever arrive from the public partner form.
        return False

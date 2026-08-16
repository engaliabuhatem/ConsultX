from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import JobApplication, JobOpening


@admin.register(JobOpening)
class JobOpeningAdmin(ModelAdmin):
    list_display = ("title", "department", "location", "employment_type", "is_open", "closing_date")
    list_filter = ("is_open", "employment_type", "workplace_type", "department")
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "department", "is_open")}),
        ("Placement", {"fields": ("location", "workplace_type", "employment_type")}),
        ("Content", {"fields": ("summary", "description", "requirements")}),
        ("Dates", {"fields": ("posted_date", "closing_date")}),
        ("SEO", {
            "classes": ("collapse",),
            "fields": ("meta_title", "meta_description", "og_image", "canonical_url"),
        }),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(ModelAdmin):
    list_display = ("full_name", "position_title", "email", "years_experience", "status", "created_at")
    list_filter = ("status", "position", "created_at")
    search_fields = ("full_name", "email", "current_employer", "cover_note")
    list_editable = ("status",)
    date_hierarchy = "created_at"

    # Everything the applicant submitted is read-only: staff triage via
    # status/notes, they don't edit somebody else's application.
    readonly_fields = (
        "position", "position_title", "full_name", "email", "phone", "location",
        "years_experience", "current_employer", "notice_period", "expected_salary",
        "linkedin_url", "portfolio_url", "cv_file", "cover_letter_file", "cover_note",
        "heard_about", "consent", "created_at",
    )
    fieldsets = (
        ("Triage", {"fields": ("status", "notes")}),
        ("Applicant", {"fields": ("full_name", "email", "phone", "location", "created_at")}),
        ("Role", {"fields": ("position", "position_title")}),
        ("Experience", {
            "fields": ("years_experience", "current_employer", "notice_period", "expected_salary"),
        }),
        ("Links", {"fields": ("linkedin_url", "portfolio_url")}),
        ("Documents", {"fields": ("cv_file", "cover_letter_file", "cover_note")}),
        ("Meta", {"fields": ("heard_about", "consent")}),
    )

    def has_add_permission(self, request):
        # Applications only ever arrive from the public careers form.
        return False

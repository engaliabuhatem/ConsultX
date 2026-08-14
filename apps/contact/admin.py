from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import ContactSubmission


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(ModelAdmin):
    list_display = ("name", "email", "service_interest", "submitted_at", "is_read")
    list_filter = ("is_read", "service_interest")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("name", "email", "phone", "company", "service_interest", "message", "submitted_at")
    list_editable = ("is_read",)

    def has_add_permission(self, request):
        # Submissions only ever come from the public contact form.
        return False

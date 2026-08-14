from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ("name", "title", "is_founder", "order")
    list_editable = ("order",)
    list_filter = ("is_founder",)
    search_fields = ("name", "title")
    ordering = ("order",)

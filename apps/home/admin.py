from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import CTABanner, HomeHero, StatCounter


class SingletonAdminMixin:
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeHero)
class HomeHeroAdmin(SingletonAdminMixin, ModelAdmin):
    list_display = ("headline",)


@admin.register(CTABanner)
class CTABannerAdmin(SingletonAdminMixin, ModelAdmin):
    list_display = ("headline",)


@admin.register(StatCounter)
class StatCounterAdmin(ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)
    ordering = ("order",)

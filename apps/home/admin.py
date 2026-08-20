from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import CTABanner, HomeHero, PracticeChapter, StatCounter


class SingletonAdminMixin:
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomeHero)
class HomeHeroAdmin(SingletonAdminMixin, ModelAdmin):
    list_display = ("headline",)
    fieldsets = (
        ("Headline", {
            "fields": ("headline", "subheadline"),
            "description": "The first thing anyone reads. The headline sits over the hero "
                            "image at up to 5.6rem, so keep it to one short sentence.",
        }),
        ("Background", {"fields": ("background_image",)}),
        ("Call to action", {"fields": ("cta_label", "cta_url")}),
    )


@admin.register(CTABanner)
class CTABannerAdmin(SingletonAdminMixin, ModelAdmin):
    list_display = ("headline",)
    fieldsets = (
        ("Banner", {"fields": ("headline", "subtext")}),
        ("Button", {"fields": ("button_label", "button_url")}),
    )


@admin.register(StatCounter)
class StatCounterAdmin(ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(PracticeChapter)
class PracticeChapterAdmin(ModelAdmin):
    list_display = ("title", "swatch", "eyebrow", "order")
    list_editable = ("order",)
    list_display_links = ("title",)
    ordering = ("order",)
    fieldsets = (
        ("Copy", {
            "fields": ("eyebrow", "title", "body"),
            "description": "One full-width band on the homepage. Three of them read as a "
                            "sequence, so keep the three headings the same shape.",
        }),
        ("Look", {
            "fields": ("image", "palette"),
            "description": "The palette tints the photograph and colors the heading rule, "
                            "the number and the label — pick the practice this band is about.",
        }),
        ("Link", {"fields": ("link_url", "link_label")}),
        ("Order", {"fields": ("order",)}),
    )

    #: Mirrors the three practice palettes in assets/input.css. Kept here as
    #: plain hex rather than read from the stylesheet so the changelist has no
    #: build-step dependency — if the palette moves, both change together.
    PALETTE_SWATCHES = {
        "a": ("#fad02c", "#2c5043", "Sustainability"),
        "b": ("#9c5539", "#787d7b", "Heavy Infrastructure"),
        "c": ("#48a899", "#00524d", "Hydraulic Authority"),
    }

    @admin.display(description="Palette")
    def swatch(self, obj):
        primary, secondary, label = self.PALETTE_SWATCHES.get(
            obj.palette, ("#636864", "#dcd8c9", "—")
        )
        return format_html(
            '<span style="display:inline-flex;align-items:center;gap:.5rem">'
            '<span style="display:inline-flex;width:34px;height:12px;border-radius:99px;'
            'overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,.12)">'
            '<span style="flex:1;background:{}"></span>'
            '<span style="flex:1;background:{}"></span>'
            "</span>{}</span>",
            primary, secondary, label,
        )

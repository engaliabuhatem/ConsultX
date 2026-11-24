"""
adminkit's own tests.

Deliberately self-contained: every model used here ships with Django, so this
file keeps working when the app is copied into a project that has none of
ConsultX's models. Project-specific assertions (which cards appear, which brand
stylesheet loads) belong in that project's tests — see apps/core/tests.py.
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings
from django.urls import reverse

from adminkit.dashboard import Attention, Dashboard, Recent, Tile, _as_query
from adminkit.nav import dashboard_item, group, item, link
from adminkit.palette import base_ramp, hex_to_oklch, oklch_to_hex, primary_ramp
from adminkit.theme import build_unfold

User = get_user_model()


def _parse(value: str) -> tuple[float, float, float]:
    lightness, chroma, hue = value.removeprefix("oklch(").removesuffix(")").split()
    return float(lightness.rstrip("%")), float(chroma), float(hue)


class PaletteTests(TestCase):
    def test_known_conversion(self):
        lightness, chroma, hue = hex_to_oklch("#9c5539")
        self.assertAlmostEqual(lightness, 52.8, places=1)
        self.assertAlmostEqual(chroma, 0.103, places=3)
        self.assertAlmostEqual(hue, 41.8, places=1)

    def test_roundtrip(self):
        for value in ("#9c5539", "#f2efe4", "#2563eb", "#000000", "#ffffff"):
            with self.subTest(value=value):
                self.assertEqual(oklch_to_hex(*hex_to_oklch(value)), value)

    def test_short_hex(self):
        self.assertEqual(hex_to_oklch("#fff"), hex_to_oklch("#ffffff"))

    def test_rejects_bad_hex(self):
        with self.assertRaises(ValueError):
            hex_to_oklch("#12345")

    def test_generated_ramp_matches_hand_tuned_values(self):
        """The ConsultX ramps were tuned by hand before this generator existed;
        reproducing them exactly is what makes the generator trustworthy for
        the next project."""
        primary = primary_ramp("#9c5539")
        self.assertEqual(primary["600"], "oklch(52.8% 0.103 41.8)")
        self.assertEqual(primary["50"], "oklch(97.2% 0.014 41.8)")
        self.assertEqual(primary["950"], "oklch(22.0% 0.042 41.8)")

        base = base_ramp("#f2efe4")
        self.assertEqual(base["50"], "oklch(98.4% 0.006 94.2)")
        self.assertEqual(base["950"], "oklch(15.5% 0.010 107.4)")

    def test_step_600_can_carry_white_text(self):
        """Unfold paints white on primary-600. A brand color too light to reach
        that lightness must be darkened by the ramp, not passed through."""
        for brand in ("#fad02c", "#ffffff", "#2563eb", "#000000"):
            with self.subTest(brand=brand):
                lightness, _, _ = _parse(primary_ramp(brand)["600"])
                self.assertLess(lightness, 60.0)

    def test_ramp_holds_one_hue(self):
        hues = {_parse(v)[2] for v in primary_ramp("#2563eb").values()}
        self.assertEqual(len(hues), 1)

    def test_greyscale_brand_still_produces_chroma(self):
        """A near-grey brand color has almost no chroma of its own; the floor
        keeps the mid-ramp from collapsing to grey."""
        self.assertGreater(_parse(primary_ramp("#808080")["500"])[1], 0.04)

    def test_saturation_and_tint_scale_the_ramps(self):
        muted = _parse(primary_ramp("#9c5539", saturation=0.5)["600"])[1]
        full = _parse(primary_ramp("#9c5539")["600"])[1]
        self.assertAlmostEqual(muted, full / 2, places=2)
        self.assertEqual(_parse(base_ramp("#f2efe4", tint=0)["500"])[1], 0.0)


class QueryTranslationTests(TestCase):
    """A card's number and the page it links to must describe the same rows."""

    def test_booleans_become_admin_flags(self):
        self.assertEqual(_as_query({"is_active": False}), "is_active__exact=0")
        self.assertEqual(_as_query({"is_active": True}), "is_active__exact=1")

    def test_plain_key_gets_exact_lookup(self):
        self.assertEqual(_as_query({"status": "new"}), "status__exact=new")

    def test_explicit_lookup_is_left_alone(self):
        self.assertEqual(_as_query({"status__in": "new,open"}), "status__in=new,open")


class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            "editor", email="e@example.com", password="x",
            is_staff=True, is_superuser=True,
        )
        cls.dormant = User.objects.create_user(
            "dormant", email="d@example.com", password="x", is_active=False,
        )

    def _request(self):
        return type("R", (), {"user": self.staff})()

    def _context(self):
        return Dashboard(
            attention=[Attention(User, "Inactive", where={"is_active": False})],
            tiles=[Tile(User, "Users")],
            recent=Recent(
                User,
                order_by="-date_joined",
                label_field="username",
                meta_field="email",
                date_field="date_joined",
                unread_field="is_active",
            ),
        ).as_callback()(self._request(), {})

    def test_attention_counts_and_links_agree(self):
        card = self._context()["ak_attention"][0]
        self.assertEqual(card["value"], 1)
        self.assertEqual(card["total"], 2)
        self.assertIn("is_active__exact=0", card["url"])

    def test_attention_total_sums_the_cards(self):
        self.assertEqual(self._context()["ak_attention_total"], 1)

    def test_tile_without_filter_counts_everything(self):
        self.assertEqual(self._context()["ak_tiles"][0]["value"], 2)

    def test_tile_label_defaults_to_verbose_name(self):
        self.assertEqual(Tile(User).render()["label"], "Users")

    def test_tones_cycle_by_position(self):
        cards = Dashboard(
            attention=[Attention(User, f"c{i}") for i in range(4)]
        ).as_callback()(self._request(), {})["ak_attention"]
        self.assertEqual([c["tone"] for c in cards], ["a1", "a2", "a3", "a1"])

    def test_explicit_tone_wins(self):
        card = Attention(User, "x", tone="a3").render(0)
        self.assertEqual(card["tone"], "a3")

    def test_recent_rows_carry_display_fields(self):
        rows = self._context()["ak_recent"]
        self.assertEqual(rows[0]["label"], "dormant")
        self.assertEqual(rows[0]["meta"], "d@example.com")
        self.assertFalse(rows[0]["handled"])
        self.assertTrue(rows[1]["handled"])

    def test_recent_respects_the_limit(self):
        rows = Recent(User, order_by="-date_joined", limit=1).render()
        self.assertEqual(len(rows), 1)

    def test_greeting_is_formatted_with_the_user(self):
        self.assertEqual(self._context()["ak_greeting"], "Welcome back, editor.")

    def test_empty_dashboard_is_valid(self):
        context = Dashboard().as_callback()(self._request(), {})
        self.assertEqual(context["ak_attention"], [])
        self.assertEqual(context["ak_recent"], [])
        self.assertEqual(context["ak_attention_total"], 0)

    def test_unregistered_model_yields_a_card_without_a_link(self):
        """A model missing from the admin must not 500 the landing page."""
        card = Tile(ContentType, "Content types").render()
        self.assertIsNone(card["url"])
        self.assertIsNone(card["add"])


class NavTests(TestCase):
    def test_string_reference_resolves_to_the_admin_route(self):
        entry = item("auth.User", "People", icon="groups")
        self.assertEqual(str(entry["link"]), reverse("admin:auth_user_changelist"))
        self.assertEqual(entry["icon"], "groups")

    def test_model_class_reference_works_too(self):
        self.assertEqual(
            str(item(User, icon="groups")["link"]),
            reverse("admin:auth_user_changelist"),
        )

    def test_add_action(self):
        entry = item("auth.User", "Add person", action="add")
        self.assertEqual(str(entry["link"]), reverse("admin:auth_user_add"))

    def test_string_reference_requires_a_title(self):
        with self.assertRaises(ValueError):
            item("auth.User")

    def test_malformed_reference_is_rejected(self):
        with self.assertRaises(ValueError):
            item("User", "People")

    def test_permission_is_only_set_when_given(self):
        self.assertNotIn("permission", item("auth.User", "People"))
        self.assertIn("permission", item("auth.User", "People", permission="auth.view_user"))

    def test_group_and_named_link(self):
        entry = group("Overview", [dashboard_item(), link("Home", "admin:index")])
        self.assertEqual(str(entry["title"]), "Overview")
        self.assertEqual(len(entry["items"]), 2)
        self.assertEqual(str(entry["items"][0]["link"]), reverse("admin:index"))


class BuildUnfoldTests(TestCase):
    def test_minimal_call_produces_a_usable_config(self):
        config = build_unfold(title="Acme Admin", brand="#2563eb", neutral="#f4f4f5")
        self.assertEqual(config["SITE_TITLE"], "Acme Admin")
        self.assertEqual(config["SITE_HEADER"], "Acme Admin")
        self.assertIn("primary", config["COLORS"])
        self.assertIn("base", config["COLORS"])
        self.assertEqual(len(config["COLORS"]["primary"]), 11)
        self.assertNotIn("DASHBOARD_CALLBACK", config)
        self.assertNotIn("LOGIN", config)

    def test_styles_resolve_in_order_with_brand_last(self):
        """Late binding matters: static() cannot run at settings-import time,
        and the brand file must load after adminkit's own to override it."""
        config = build_unfold(title="A", extra_styles=["css/brand.css"])
        resolved = [style(None) for style in config["STYLES"]]
        self.assertEqual(len(resolved), 2)
        self.assertTrue(resolved[0].endswith("adminkit/css/adminkit.css"))
        self.assertTrue(resolved[1].endswith("css/brand.css"))

    def test_login_image_is_lazy(self):
        config = build_unfold(title="A", login_image="img/x.jpg")
        self.assertTrue(config["LOGIN"]["image"](None).endswith("img/x.jpg"))

    def test_extra_kwargs_pass_through_and_override(self):
        config = build_unfold(title="A", SHOW_VIEW_ON_SITE=False, TABS=[{"x": 1}])
        self.assertFalse(config["SHOW_VIEW_ON_SITE"])
        self.assertEqual(config["TABS"], [{"x": 1}])


@override_settings(ALLOWED_HOSTS=["testserver"])
class DashboardPageTests(TestCase):
    """The landing page must render from adminkit's template, not Unfold's —
    which only happens while "adminkit" precedes "unfold" in INSTALLED_APPS."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            "boss", password="x", is_staff=True, is_superuser=True
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_index_renders_adminkit_components(self):
        html = self.client.get(reverse("admin:index")).content.decode()
        for marker in ("ak-hero", "ak-accentbar", "ak-section-title", "ak-tile"):
            with self.subTest(marker=marker):
                self.assertIn(marker, html)

    def test_stylesheet_is_linked(self):
        html = self.client.get(reverse("admin:index")).content.decode()
        self.assertIn("adminkit/css/adminkit.css", html)

    def test_app_list_is_still_rendered_below_the_dashboard(self):
        """The override adds rows above Unfold's app list; it must not replace
        it, or models missing from the sidebar become unreachable."""
        html = self.client.get(reverse("admin:index")).content.decode()
        self.assertIn(reverse("admin:auth_user_changelist"), html)

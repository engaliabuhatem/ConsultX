from django.test import RequestFactory, TestCase
from django.urls import reverse

from .navigation import NAV_TREE, build_nav


class NavigationTreeTests(TestCase):
    """The nav renders on every page, so a broken entry takes the whole site
    down at once rather than one view."""

    def _flat_leaves(self):
        for entry in NAV_TREE:
            if "children" in entry:
                yield from entry["children"]
            else:
                yield entry

    def test_every_destination_resolves_and_responds(self):
        for leaf in self._flat_leaves():
            with self.subTest(url=leaf["url"]):
                response = self.client.get(reverse(leaf["url"]))
                self.assertEqual(response.status_code, 200)

    def test_all_ten_destinations_are_reachable_from_the_nav(self):
        """Grouping reduced the top-level count, but nothing was dropped."""
        urls = {leaf["url"] for leaf in self._flat_leaves()}
        self.assertEqual(urls, {
            "home:index", "team:about", "team:leadership",
            "services:list", "sectors:list", "projects:list",
            "publications:list", "blog:list",
            "careers:list", "partners:index", "contact:index",
        })

    def test_group_keys_are_unique(self):
        """Keys become aria-controls ids; duplicates would point two buttons
        at the same panel."""
        keys = [e["key"] for e in NAV_TREE if "children" in e]
        self.assertEqual(len(keys), len(set(keys)))


class NavigationActiveStateTests(TestCase):
    def _nav_for(self, url_name):
        response = self.client.get(reverse(url_name))
        return response.context["nav_items"]

    def test_group_is_current_when_a_child_is(self):
        nav = self._nav_for("sectors:list")
        expertise = next(i for i in nav if i.get("key") == "expertise")

        self.assertTrue(expertise["is_current"])
        sectors = next(c for c in expertise["children"] if c["label"] == "Sectors")
        services = next(c for c in expertise["children"] if c["label"] == "Services")
        self.assertTrue(sectors["is_current"])
        self.assertFalse(services["is_current"])

    def test_sibling_namespaces_do_not_both_match(self):
        """team owns About and Leadership — namespace matching would light
        up both at once."""
        nav = self._nav_for("team:leadership")
        about_group = next(i for i in nav if i.get("key") == "about")

        current = [c["label"] for c in about_group["children"] if c["is_current"]]
        self.assertEqual(current, ["Leadership"])

    def test_detail_pages_keep_their_section_highlighted(self):
        """A namespace pattern ("services:") must match detail views too."""
        factory = RequestFactory()
        request = factory.get("/services/some-slug/")
        request.resolver_match = type("M", (), {"view_name": "services:detail"})()

        expertise = next(i for i in build_nav(request) if i.get("key") == "expertise")
        self.assertTrue(expertise["is_current"])

    def test_no_item_is_current_on_an_unmatched_view(self):
        factory = RequestFactory()
        request = factory.get("/nowhere/")
        request.resolver_match = None
        self.assertFalse(any(i["is_current"] for i in build_nav(request)))


class DisclosurePatternTests(TestCase):
    """
    The rendered dropdowns must follow the W3C APG *disclosure navigation*
    pattern. The menubar pattern's roles promise arrow-key composite focus
    management this nav does not implement.
    """

    def setUp(self):
        self.html = self.client.get(reverse("home:index")).content.decode()

    def test_triggers_are_buttons_with_the_required_aria(self):
        for key in ("about", "expertise", "insights", "work-with-us"):
            with self.subTest(group=key):
                self.assertIn(f'id="nav-{key}-trigger"', self.html)
                self.assertIn(f'aria-controls="nav-{key}"', self.html)
                self.assertIn(f'id="nav-{key}"', self.html)

    def test_menu_roles_are_not_used(self):
        self.assertNotIn('role="menu"', self.html)
        self.assertNotIn('role="menuitem"', self.html)

    def test_escape_returns_focus_to_the_trigger(self):
        self.assertIn("$refs.trigger.focus()", self.html)

    def test_dropdown_closes_when_focus_leaves_the_group(self):
        self.assertIn("$el.contains($event.relatedTarget)", self.html)

    def test_hover_to_open_is_gated_on_pointer_capability(self):
        """Otherwise a touch tap opens on mouseenter then closes on click."""
        self.assertIn("(hover: hover)", self.html)

    def test_current_page_is_marked(self):
        self.assertIn('aria-current="page"', self.html)


class FormFieldRenderingTests(TestCase):
    def test_help_text_is_linked_by_aria_describedby(self):
        html = self.client.get(reverse("partners:index")).content.decode()
        self.assertIn('id="id_key_clients_help"', html)
        self.assertIn('aria-describedby="id_key_clients_help"', html)

    def test_required_fields_expose_aria_required(self):
        html = self.client.get(reverse("partners:index")).content.decode()
        self.assertIn('aria-required="true"', html)

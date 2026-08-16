from django.test import TestCase
from django.urls import reverse


class NavigationTests(TestCase):
    """
    The nav is included on every page, so a broken {% url %} in it takes the
    whole site down at once rather than one view. These assert the ten
    primary destinations resolve and are actually rendered.
    """

    EXPECTED_LINKS = [
        ("home:index", "Home"),
        ("team:about", "About"),
        ("services:list", "Services"),
        ("sectors:list", "Sectors"),
        ("projects:list", "Projects"),
        ("team:leadership", "Leadership"),
        ("publications:list", "Publications"),
        ("partners:index", "Partner"),
        ("careers:list", "Careers"),
        ("contact:index", "Contact Us"),
    ]

    def test_every_nav_destination_resolves_and_responds(self):
        for url_name, label in self.EXPECTED_LINKS:
            with self.subTest(link=label):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_nav_renders_all_ten_links(self):
        response = self.client.get(reverse("home:index"))
        html = response.content.decode()
        for url_name, label in self.EXPECTED_LINKS:
            with self.subTest(link=label):
                self.assertIn(f'href="{reverse(url_name)}"', html)
                self.assertIn(f">{label}<", html)

    def test_active_link_is_marked_for_assistive_tech(self):
        response = self.client.get(reverse("careers:list"))
        html = response.content.decode()
        self.assertIn('aria-current="page"', html)

    def test_sibling_namespaces_do_not_both_light_up(self):
        """team owns both About and Leadership — matching on namespace alone
        would mark two links current at once."""
        response = self.client.get(reverse("team:leadership"))
        # Desktop bar + mobile drawer each render it once; two, never four.
        self.assertEqual(response.content.decode().count('aria-current="page"'), 2)


class FormFieldRenderingTests(TestCase):
    def test_help_text_is_linked_by_aria_describedby(self):
        response = self.client.get(reverse("partners:index"))
        html = response.content.decode()

        # key_clients carries help text, so it must be announced on focus.
        self.assertIn('id="id_key_clients_help"', html)
        self.assertIn('aria-describedby="id_key_clients_help"', html)

    def test_required_fields_expose_aria_required(self):
        response = self.client.get(reverse("partners:index"))
        self.assertIn('aria-required="true"', response.content.decode())

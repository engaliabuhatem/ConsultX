"""
Guards against a Django footgun that fails silently.

`{# ... #}` is a SINGLE-LINE comment: the docs state "no newlines are
permitted between the {# and #} delimiters". Span one across two lines and
Django does not recognise it as a comment token at all — it renders the
whole thing to the page as literal text, with no error and no warning.

That shipped here: a three-line {# #} in partials/nav.html printed its own
text under the header on every page, and two more in base.html sat inside
<head>, where leaked text forces the browser to close <head> early and
reopen as <body> — dumping the remaining <style>/<script> tags into the
document body and breaking layout.

Multi-line comments must use {% comment %}...{% endcomment %}.
"""

import pathlib
import re

from django.conf import settings
from django.test import TestCase

TEMPLATE_ROOT = pathlib.Path(settings.BASE_DIR) / "templates"


class TemplateCommentSyntaxTests(TestCase):
    def test_no_multiline_short_comments(self):
        offenders = []
        for path in sorted(TEMPLATE_ROOT.rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"\{#.*?#\}", text, re.S):
                if "\n" in match.group(0):
                    line = text[: match.start()].count("\n") + 1
                    offenders.append(
                        f"{path.relative_to(TEMPLATE_ROOT).as_posix()}:{line}"
                    )

        self.assertEqual(
            offenders, [],
            "Multi-line {# #} comments render as visible page text. "
            "Use {% comment %}...{% endcomment %} instead. Found at: "
            + ", ".join(offenders),
        )


class RenderedOutputTests(TestCase):
    """Belt and braces: even if a new comment form slips past the source
    scan, no page may ever emit a raw template delimiter."""

    PATHS = [
        "/", "/about/", "/services/", "/sectors/", "/projects/",
        "/leadership/", "/publications/", "/insights/", "/careers/",
        "/careers/apply/", "/partners/", "/contact/",
    ]

    def test_no_template_delimiters_leak_into_any_page(self):
        for path in self.PATHS:
            with self.subTest(path=path):
                html = self.client.get(path).content.decode()
                self.assertNotIn("{#", html)
                self.assertNotIn("#}", html)
                self.assertNotIn("{%", html)

    def test_head_is_not_terminated_early_by_stray_text(self):
        """A leaked comment in <head> pushes <style>/<script> into <body>."""
        from apps.siteconfig.models import SiteSettings

        site = SiteSettings.load()
        site.accent_color = "#1e40af"
        site.custom_css = "body{color:red}"
        site.save()

        html = self.client.get("/").content.decode()
        head = html[html.find("<head"): html.find("</head>")]

        # Both style blocks must still be inside <head>.
        self.assertIn("--color-accent: #1e40af", head)
        self.assertIn("body{color:red}", head)
        self.assertNotIn("{#", html)

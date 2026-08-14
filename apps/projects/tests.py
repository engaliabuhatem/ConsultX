from django.test import TestCase
from django.urls import reverse

from .models import Project


class ProjectViewTests(TestCase):
    def test_empty_state_copy_shows_when_no_published_projects(self):
        response = self.client.get(reverse("projects:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "newly founded practice")

    def test_published_project_appears_in_list(self):
        Project.objects.create(title="Nile Delta Flood Study", slug="nile-delta-flood-study",
                                is_published=True, order=1)
        response = self.client.get(reverse("projects:list"))
        self.assertContains(response, "Nile Delta Flood Study")
        self.assertNotContains(response, "newly founded practice")

    def test_unpublished_project_hidden_from_list(self):
        Project.objects.create(title="Draft Project", slug="draft-project",
                                is_published=False, order=1)
        response = self.client.get(reverse("projects:list"))
        self.assertNotContains(response, "Draft Project")

    def test_unpublished_project_detail_returns_404(self):
        """A draft project must not be reachable by guessing its URL."""
        Project.objects.create(title="Draft Project", slug="draft-project",
                                is_published=False, order=1)
        response = self.client.get(reverse("projects:detail", kwargs={"slug": "draft-project"}))
        self.assertEqual(response.status_code, 404)

    def test_confidential_project_hides_client_name(self):
        Project.objects.create(title="Confidential Water Project", slug="confidential-water-project",
                                client_name="Should Not Appear", is_confidential=True,
                                is_published=True, order=1)
        response = self.client.get(reverse("projects:detail", kwargs={"slug": "confidential-water-project"}))
        self.assertContains(response, "Confidential")
        self.assertNotContains(response, "Should Not Appear")

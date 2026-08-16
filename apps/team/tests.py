from django.test import TestCase
from django.urls import reverse

from .models import TeamMember


class TeamViewTests(TestCase):
    def test_about_page_loads(self):
        response = self.client.get(reverse("team:about"))
        self.assertEqual(response.status_code, 200)

    def test_team_list_loads_and_shows_members(self):
        TeamMember.objects.create(name="Ahmed H. Suleiman", title="Founder", is_founder=True, order=1)
        response = self.client.get(reverse("team:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ahmed H. Suleiman")


class LeadershipViewTests(TestCase):
    def test_leadership_page_shows_only_flagged_members(self):
        TeamMember.objects.create(
            name="Ahmed H. Suleiman", title="Managing Director", is_leadership=True, order=1
        )
        TeamMember.objects.create(name="Junior Drafter", title="Drafter", order=2)

        response = self.client.get(reverse("team:leadership"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ahmed H. Suleiman")
        self.assertNotContains(response, "Junior Drafter")

    def test_leadership_is_independent_of_founder_flag(self):
        """A hired MD is leadership without being a founder, and vice versa."""
        TeamMember.objects.create(name="Hired MD", title="MD", is_leadership=True, order=1)
        TeamMember.objects.create(
            name="Silent Founder", title="Founder", is_founder=True, order=2
        )

        response = self.client.get(reverse("team:leadership"))
        self.assertContains(response, "Hired MD")
        self.assertNotContains(response, "Silent Founder")

    def test_empty_state(self):
        response = self.client.get(reverse("team:leadership"))
        self.assertContains(response, "Leadership profiles will appear here")

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

"""
The ConsultX admin dashboard.

Card layout, URL building and query-param translation all live in
adminkit/dashboard.py; this file only says which models appear and in what
order. Adding a card is one line.
"""

from adminkit.dashboard import Attention, Dashboard, Recent, Tile

from apps.blog.models import Post
from apps.careers.models import JobApplication, JobOpening
from apps.contact.models import ContactSubmission
from apps.home.models import PracticeChapter
from apps.partners.models import PartnerApplication
from apps.projects.models import Project
from apps.sectors.models import Sector
from apps.services.models import Service
from apps.team.models import TeamMember

dashboard_callback = Dashboard(
    greeting="Welcome back, {name}.",
    attention_title="Needs attention",
    attention=[
        Attention(ContactSubmission, "Unread enquiries", where={"is_read": False}),
        Attention(JobApplication, "New job applications", where={"status": "new"}),
        Attention(PartnerApplication, "New partner applications", where={"status": "new"}),
    ],
    tiles_title="Site content",
    tiles=[
        Tile(Service, "Services"),
        Tile(Sector, "Sectors"),
        Tile(Project, "Projects"),
        Tile(TeamMember, "Team members"),
        Tile(Post, "Insight posts"),
        Tile(JobOpening, "Open roles", where={"is_open": True}),
        Tile(PracticeChapter, "Chapters"),
    ],
    recent=Recent(
        ContactSubmission,
        title="Latest enquiries",
        order_by="-submitted_at",
        limit=5,
        label_field="name",
        meta_field="company",
        date_field="submitted_at",
        unread_field="is_read",
    ),
).as_callback()

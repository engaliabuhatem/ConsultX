"""
Seeds the three homepage chapters from the approved design comp.

Content models in this project are deliberately not pre-seeded — a
consultancy's services and sectors are positioning decisions, and inventing
them would be inventing credentials (see apps/sectors/models.py). These
three are the exception, and for the opposite reason: they are not claims
about the firm, they *are* the design. The comp specifies three bands with
this copy and these photographs; seeding them means the homepage ships
looking like the thing that was signed off, and every word stays editable.

Idempotent, and only ever runs into an empty table — if anyone has already
created chapters by hand, theirs are left alone.
"""

from django.db import migrations

CHAPTERS = [
    {
        "order": 0,
        "eyebrow": "Direction A · Sustainability",
        "title": "Impact through precision.",
        "body": (
            "Systems-first. Bright by design. Nothing wasted. Our sustainability practice "
            "designs infrastructure that performs today without borrowing against tomorrow."
        ),
        "palette": "a",
    },
    {
        "order": 1,
        "eyebrow": "Direction B · Heavy Infrastructure",
        "title": "As we evolve, our execution should too.",
        "body": (
            "Complex challenges, met without the baggage of the past — the agility of a "
            "startup with the rigorous technical standards heavy infrastructure demands."
        ),
        "palette": "b",
    },
    {
        "order": 2,
        "eyebrow": "Direction C · Hydraulic Authority",
        "title": "From source to surface.",
        "body": (
            "Precision-engineered hydraulic systems and industrial solutions, powering the "
            "machines that move the world — from deep authority to bright clarity."
        ),
        "palette": "c",
    },
]


def seed(apps, schema_editor):
    PracticeChapter = apps.get_model("home", "PracticeChapter")
    if PracticeChapter.objects.exists():
        return
    PracticeChapter.objects.bulk_create(
        PracticeChapter(link_url="", link_label="Explore the practice", **c) for c in CHAPTERS
    )


def unseed(apps, schema_editor):
    PracticeChapter = apps.get_model("home", "PracticeChapter")
    PracticeChapter.objects.filter(title__in=[c["title"] for c in CHAPTERS]).delete()


class Migration(migrations.Migration):
    dependencies = [("home", "0003_practicechapter")]

    operations = [migrations.RunPython(seed, unseed)]

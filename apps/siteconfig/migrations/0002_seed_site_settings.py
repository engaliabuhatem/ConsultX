from django.db import migrations


def create_site_settings(apps, schema_editor):
    SiteSettings = apps.get_model("siteconfig", "SiteSettings")
    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(pk=1)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("siteconfig", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_site_settings, noop_reverse),
    ]

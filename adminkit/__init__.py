"""
adminkit — a portable Django admin skin.

Everything project-specific about the ConsultX admin (the OKLCH color ramps,
the dashboard cards, the grouped sidebar, the CSS chrome) generalised into one
app you can copy into any Django project. Nothing in here imports a ConsultX
model or hardcodes a ConsultX color.

See README.md in this directory for the install checklist.
"""

default_app_config = "adminkit.apps.AdminKitConfig"

from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.forms import StyledModelForm

from .models import PartnerApplication


class PartnerApplicationForm(StyledModelForm):
    """
    Grouped into fieldsets by the template (partners.html), not here — the
    ordering below is the order they render in.
    """

    class Meta:
        model = PartnerApplication
        fields = [
            "company_name", "registration_number", "tax_id", "website",
            "country", "city", "year_established", "employee_count",
            "contact_name", "contact_title", "contact_email", "contact_phone",
            "partnership_type", "sectors", "capabilities", "key_clients", "annual_turnover",
            "certifications", "has_professional_indemnity",
            "has_conflict_of_interest", "conflict_details",
            "company_profile_file", "trade_licence_file",
            "message", "consent",
        ]
        labels = {
            "company_name": _("Company name"),
            "registration_number": _("Commercial registration number"),
            "tax_id": _("Tax identification number"),
            "website": _("Company website"),
            "country": _("Country"),
            "city": _("City"),
            "year_established": _("Year established"),
            "employee_count": _("Number of employees"),
            "contact_name": _("Contact name"),
            "contact_title": _("Job title"),
            "contact_email": _("Contact email"),
            "contact_phone": _("Contact phone"),
            "partnership_type": _("Type of partnership sought"),
            "sectors": _("Sectors you can deliver into"),
            "capabilities": _("Capabilities and services offered"),
            "key_clients": _("Reference clients or projects"),
            "annual_turnover": _("Approximate annual turnover"),
            "certifications": _("Certifications and registrations"),
            "has_professional_indemnity": _("We hold professional indemnity insurance"),
            "has_conflict_of_interest": _("We have a potential conflict of interest to declare"),
            "conflict_details": _("Details of the conflict"),
            "company_profile_file": _("Company profile"),
            "trade_licence_file": _("Trade licence"),
            "message": _("Anything else we should know?"),
            "consent": _("I agree to ConsultX storing this information to assess the partnership."),
        }
        help_texts = {
            "key_clients": _("Only name clients you are contractually free to name."),
            "annual_turnover": _("Optional. Include the currency, e.g. \"EGP 25M\"."),
            "sectors": _("Hold Ctrl / Cmd to select more than one."),
            "certifications": _("One per line — ISO 9001, syndicate registration, trade licence."),
            "company_profile_file": _("Optional. PDF, DOC or DOCX, maximum 10 MB."),
            "trade_licence_file": _("Optional. PDF, DOC or DOCX, maximum 10 MB."),
        }
        widgets = {
            "capabilities": forms.Textarea(attrs={"rows": 5}),
            "key_clients": forms.Textarea(attrs={"rows": 4}),
            "certifications": forms.Textarea(attrs={"rows": 4}),
            "conflict_details": forms.Textarea(attrs={"rows": 3}),
            "message": forms.Textarea(attrs={"rows": 4}),
            "sectors": forms.SelectMultiple(attrs={"size": 6}),
            "contact_email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "contact_phone": forms.TextInput(attrs={"inputmode": "tel", "autocomplete": "tel"}),
            "company_name": forms.TextInput(attrs={"autocomplete": "organization"}),
            "website": forms.URLInput(attrs={"placeholder": "https://"}),
            "year_established": forms.NumberInput(attrs={"min": 1800}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["consent"].required = True
        self.fields["consent"].error_messages["required"] = _(
            "We can't accept the application without this consent."
        )
        # Bound at request time, not import time — a long-running process
        # would otherwise freeze the max year at whenever it booted.
        self.fields["year_established"].widget.attrs["max"] = timezone.localdate().year

    def clean_year_established(self):
        year = self.cleaned_data.get("year_established")
        if year and year > timezone.localdate().year:
            raise forms.ValidationError(_("That year is in the future."))
        return year

    def clean(self):
        cleaned = super().clean()
        # A declared conflict with no detail is not a declaration.
        if cleaned.get("has_conflict_of_interest") and not cleaned.get("conflict_details"):
            self.add_error(
                "conflict_details",
                _("Please describe the conflict you are declaring."),
            )
        return cleaned

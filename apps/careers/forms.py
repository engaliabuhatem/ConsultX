from django import forms
from django.utils.translation import gettext_lazy as _

from apps.core.forms import StyledModelForm

from .models import JobApplication


class JobApplicationForm(StyledModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "full_name", "email", "phone", "location",
            "years_experience", "current_employer", "notice_period", "expected_salary",
            "linkedin_url", "portfolio_url",
            "cv_file", "cover_letter_file", "cover_note",
            "heard_about", "consent",
        ]
        labels = {
            "full_name": _("Full name"),
            "email": _("Email address"),
            "phone": _("Phone number"),
            "location": _("Where are you based?"),
            "years_experience": _("Years of relevant experience"),
            "current_employer": _("Current or most recent employer"),
            "notice_period": _("Notice period"),
            "expected_salary": _("Expected salary"),
            "linkedin_url": _("LinkedIn profile"),
            "portfolio_url": _("Portfolio or personal site"),
            "cv_file": _("CV / résumé"),
            "cover_letter_file": _("Cover letter (file)"),
            "cover_note": _("Or write a short note instead"),
            "heard_about": _("How did you hear about this role?"),
            "consent": _("I agree to ConsultX storing this application for recruitment purposes."),
        }
        help_texts = {
            # Restated for applicants; the model help_text is written for staff.
            "cv_file": _("PDF, DOC or DOCX. Maximum 10 MB."),
            "cover_letter_file": _("Optional. PDF, DOC or DOCX, maximum 10 MB."),
            "cover_note": _("Optional. A few sentences on why this role interests you."),
            "expected_salary": _("Optional — a range is fine."),
            "years_experience": _("Whole years, e.g. 7."),
        }
        widgets = {
            "cover_note": forms.Textarea(attrs={"rows": 5}),
            "phone": forms.TextInput(attrs={"inputmode": "tel", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "years_experience": forms.NumberInput(attrs={"min": 0, "max": 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Blank ModelForm booleans are optional by default; consent is the
        # lawful basis for storing the rest of this data, so it must be ticked.
        self.fields["consent"].required = True
        self.fields["consent"].error_messages["required"] = _(
            "We can't accept the application without this consent."
        )
        self.fields["phone"].required = True

    def clean(self):
        cleaned = super().clean()
        # A CV alone is enough; but if someone attaches nothing *and* writes
        # nothing, there is no covering context at all — ask for one of them.
        if not cleaned.get("cover_letter_file") and not cleaned.get("cover_note"):
            self.add_error(
                "cover_note",
                _("Please attach a cover letter or write a short note."),
            )
        return cleaned

from django import forms

from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "company", "service_interest", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

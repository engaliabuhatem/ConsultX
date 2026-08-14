from django import forms

from .models import ContactSubmission

FIELD_CLASSES = (
    "w-full rounded-md border border-technical-soft bg-white px-4 py-2.5 text-sm "
    "focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent"
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "phone", "company", "service_interest", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": FIELD_CLASSES, "placeholder": "John Doe"}),
            "email": forms.EmailInput(attrs={"class": FIELD_CLASSES, "placeholder": "john@company.com"}),
            "phone": forms.TextInput(attrs={"class": FIELD_CLASSES, "placeholder": "+20 XXX XXX XXXX"}),
            "company": forms.TextInput(attrs={"class": FIELD_CLASSES, "placeholder": "Company Name"}),
            "service_interest": forms.Select(attrs={"class": FIELD_CLASSES}),
            "message": forms.Textarea(attrs={
                "class": FIELD_CLASSES, "rows": 5, "placeholder": "Tell us about your project...",
            }),
        }

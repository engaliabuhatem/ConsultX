"""
Shared widget styling for every public form.

apps/contact/forms.py declares a per-field `widgets` dict. That is fine for
six fields and unmanageable for the twenty-plus on the partner form, so the
classes live here and are applied by widget *type* instead. Anything a form
sets explicitly still wins — every attribute below uses setdefault.
"""

from django import forms

FIELD_CLASSES = (
    "w-full rounded-md border border-technical-soft bg-white px-4 py-2.5 text-sm "
    "focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent "
    "aria-[invalid=true]:border-accent aria-[invalid=true]:ring-1 aria-[invalid=true]:ring-accent"
)

FILE_CLASSES = (
    "w-full rounded-md border border-dashed border-technical-soft bg-white px-4 py-3 text-sm "
    "file:me-4 file:rounded file:border-0 file:bg-accent/10 file:px-4 file:py-2 "
    "file:text-sm file:font-medium file:text-accent hover:file:bg-accent/20 "
    "focus:outline-none focus:ring-2 focus:ring-accent"
)

CHECKBOX_CLASSES = (
    "h-4 w-4 rounded border-technical-soft text-accent "
    "focus:ring-2 focus:ring-accent focus:ring-offset-0"
)


class StyledFormMixin:
    """Applies the design-system classes and the ARIA hooks the field
    template needs. Mix in *before* forms.ModelForm."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", CHECKBOX_CLASSES)
            elif isinstance(widget, forms.FileInput):
                widget.attrs.setdefault("class", FILE_CLASSES)
            else:
                widget.attrs.setdefault("class", FIELD_CLASSES)

            # WCAG 3.3.2: required state must be exposed to assistive tech,
            # not implied by the "*" in the visible label alone.
            if field.required:
                widget.attrs.setdefault("aria-required", "true")


class StyledModelForm(StyledFormMixin, forms.ModelForm):
    pass

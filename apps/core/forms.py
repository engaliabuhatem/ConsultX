"""
Shared widget styling for every public form.

apps/contact/forms.py declares a per-field `widgets` dict. That is fine for
six fields and unmanageable for the twenty-plus on the partner form, so the
classes live here and are applied by widget *type* instead. Anything a form
sets explicitly still wins — every attribute below uses setdefault.
"""

from django import forms

#: No focus:ring-* here on purpose. The base layer in assets/input.css gives
#: every focusable element one dual-tone :focus-visible indicator — an ink
#: outline that reads on paper plus a gold glow that reads on the ink-dark
#: bands — and a per-widget ring would only compete with it. What the widget
#: classes do own is the resting look and the invalid state.
FIELD_CLASSES = (
    "w-full rounded-xl border border-stone-line bg-white px-4 py-3 text-sm "
    "transition-colors hover:border-stone/50 focus:border-accent "
    "aria-[invalid=true]:border-accent aria-[invalid=true]:bg-accent/5"
)

FILE_CLASSES = (
    "w-full rounded-xl border border-dashed border-stone-line bg-white px-4 py-3 text-sm "
    "transition-colors hover:border-stone/50 "
    "file:me-4 file:rounded-full file:border-0 file:bg-accent/10 file:px-4 file:py-2 "
    "file:text-sm file:font-semibold file:text-accent hover:file:bg-accent/20"
)

CHECKBOX_CLASSES = "h-4.5 w-4.5 rounded border-stone-line text-accent"


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

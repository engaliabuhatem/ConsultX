from django import template

register = template.Library()


@register.filter
def render_accessible(field):
    """
    Render a bound field with its ARIA wiring resolved.

    `{{ field }}` can't take arguments in a template, and the attributes
    needed here depend on validation state (which help/error nodes exist),
    so they can't be baked into the widget at form-definition time either.
    Hence a filter: it is the only place that knows both.
    """
    attrs = {}
    described_by = []

    if field.help_text:
        described_by.append(f"{field.auto_id}_help")
    if field.errors:
        described_by.append(f"{field.auto_id}_error")
        attrs["aria-invalid"] = "true"

    if described_by:
        attrs["aria-describedby"] = " ".join(described_by)

    return field.as_widget(attrs=attrs)

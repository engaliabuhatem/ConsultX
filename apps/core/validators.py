"""
Shared upload validation for the two public forms that accept files
(careers CV/cover letter, partner company documents).

Deliberately extension + size only. Neither check inspects file *contents*,
so neither proves the upload is really a PDF — a renamed executable passes
both. That is acceptable here because these files are only ever downloaded
by staff from the admin, never served back to the public and never executed.
If they are ever exposed on the front end, add real content sniffing
(python-magic) and serve them from a non-executable location — see
README "Uploads".
"""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB

DOCUMENT_EXTENSIONS = ["pdf", "doc", "docx"]

validate_document_extension = FileExtensionValidator(
    allowed_extensions=DOCUMENT_EXTENSIONS,
    message=_("Upload a PDF, DOC or DOCX file."),
)


def validate_upload_size(value):
    """Reject oversized uploads with a message that states the actual limit."""
    if value.size > MAX_UPLOAD_BYTES:
        raise ValidationError(
            _("That file is %(size)s. The maximum accepted size is %(limit)s."),
            params={
                "size": filesizeformat(value.size),
                "limit": filesizeformat(MAX_UPLOAD_BYTES),
            },
        )


#: Convenience pair for FileField(validators=DOCUMENT_VALIDATORS).
DOCUMENT_VALIDATORS = [validate_document_extension, validate_upload_size]

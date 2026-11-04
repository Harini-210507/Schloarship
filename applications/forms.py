import os
from django import forms
from django.conf import settings
from .models import ScholarshipApplication, UploadedDocument

ALLOWED_EXTENSIONS = getattr(settings, 'ALLOWED_DOC_EXTENSIONS', ['.pdf', '.jpg', '.jpeg', '.png'])
MAX_SIZE_MB        = getattr(settings, 'MAX_UPLOAD_SIZE_MB', 5)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = ScholarshipApplication
        fields = []   # No extra fields; student & scholarship are set in the view


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model  = UploadedDocument
        fields = ('file',)

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            ext  = os.path.splitext(f.name)[1].lower()
            size = f.size / (1024 * 1024)
            if ext not in ALLOWED_EXTENSIONS:
                raise forms.ValidationError(
                    f'Only {", ".join(ALLOWED_EXTENSIONS)} files are allowed.'
                )
            if size > MAX_SIZE_MB:
                raise forms.ValidationError(
                    f'File must be under {MAX_SIZE_MB} MB. Yours is {size:.1f} MB.'
                )
        return f


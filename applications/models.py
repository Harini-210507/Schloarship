import os
from django.db import models
from django.contrib.auth.models import User
from scholarships.models import Scholarship, RequiredDocument


class ScholarshipApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted',    'Submitted'),
        ('under_review', 'Under Review'),
        ('approved',     'Approved'),
        ('rejected',     'Rejected'),
    ]

    student      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    scholarship  = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    reviewed_at  = models.DateTimeField(null=True, blank=True)
    reviewed_by  = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_applications'
    )
    review_notes = models.TextField(blank=True, help_text='Reason for approval or rejection.')

    class Meta:
        unique_together = ('student', 'scholarship')
        ordering        = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} → {self.scholarship.title} [{self.status}]"

    def get_status_badge_class(self):
        return {
            'submitted':    'badge-info',
            'under_review': 'badge-warning',
            'approved':     'badge-success',
            'rejected':     'badge-danger',
        }.get(self.status, 'badge-secondary')

    def all_mandatory_docs_verified(self):
        """Return True if every mandatory required document has a verified upload."""
        mandatory_docs = self.scholarship.required_documents.filter(is_mandatory=True)
        for req_doc in mandatory_docs:
            upload = self.uploaded_documents.filter(required_document=req_doc).first()
            if not upload or upload.status != 'verified':
                return False
        return True

    def has_rejected_documents(self):
        return self.uploaded_documents.filter(status='rejected').exists()


def document_upload_path(instance, filename):
    """Store files under media/applications/<app_id>/<filename>."""
    ext  = os.path.splitext(filename)[1].lower()
    safe = os.path.splitext(filename)[0][:40]
    return f"applications/{instance.application.pk}/{safe}{ext}"


class UploadedDocument(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    application       = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE, related_name='uploaded_documents')
    required_document = models.ForeignKey(RequiredDocument, on_delete=models.CASCADE, related_name='uploads')
    file              = models.FileField(upload_to=document_upload_path)
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason  = models.TextField(blank=True)
    uploaded_at       = models.DateTimeField(auto_now_add=True)
    reviewed_at       = models.DateTimeField(null=True, blank=True)

    class Meta:
        # One active upload per required document per application
        unique_together = ('application', 'required_document')

    def __str__(self):
        return f"{self.application} – {self.required_document.name}"

    def filename(self):
        return os.path.basename(self.file.name)

    def get_status_badge_class(self):
        return {
            'pending':  'badge-warning',
            'verified': 'badge-success',
            'rejected': 'badge-danger',
        }.get(self.status, 'badge-secondary')

    def is_image(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        return ext in ('.jpg', '.jpeg', '.png')

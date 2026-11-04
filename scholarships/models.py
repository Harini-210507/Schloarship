from django.db import models
from django.contrib.auth.models import User


class Scholarship(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField()
    eligibility = models.TextField(help_text='Describe who is eligible for this scholarship.')
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    deadline    = models.DateField()
    is_active   = models.BooleanField(default=True)
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='scholarships_created')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_open(self):
        from django.utils import timezone
        return self.is_active and self.deadline >= timezone.now().date()


class RequiredDocument(models.Model):
    scholarship  = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='required_documents')
    name         = models.CharField(max_length=100)
    description  = models.TextField(blank=True)
    is_mandatory = models.BooleanField(default=True)
    order        = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.scholarship.title} – {self.name}"

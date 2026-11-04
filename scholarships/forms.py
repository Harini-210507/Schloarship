from django import forms
from .models import Scholarship, RequiredDocument


class ScholarshipForm(forms.ModelForm):
    class Meta:
        model  = Scholarship
        fields = ('title', 'description', 'eligibility', 'amount', 'deadline', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'eligibility': forms.Textarea(attrs={'rows': 3}),
            'deadline':    forms.DateInput(attrs={'type': 'date'}),
        }


class RequiredDocumentForm(forms.ModelForm):
    class Meta:
        model  = RequiredDocument
        fields = ('name', 'description', 'is_mandatory', 'order')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


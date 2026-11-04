from django.contrib import admin
from .models import ScholarshipApplication, UploadedDocument


class UploadedDocumentInline(admin.TabularInline):
    model  = UploadedDocument
    extra  = 0
    fields = ('required_document', 'file', 'status', 'rejection_reason')


@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    list_display  = ('student', 'scholarship', 'status', 'submitted_at')
    list_filter   = ('status', 'scholarship')
    search_fields = ('student__username', 'scholarship__title')
    inlines       = [UploadedDocumentInline]


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'required_document', 'status', 'uploaded_at')
    list_filter  = ('status',)

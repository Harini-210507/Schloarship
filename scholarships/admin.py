from django.contrib import admin
from .models import Scholarship, RequiredDocument


class RequiredDocumentInline(admin.TabularInline):
    model = RequiredDocument
    extra = 1


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display  = ('title', 'amount', 'deadline', 'is_active', 'created_at')
    list_filter   = ('is_active',)
    search_fields = ('title',)
    inlines       = [RequiredDocumentInline]


@admin.register(RequiredDocument)
class RequiredDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'scholarship', 'is_mandatory', 'order')

from django.contrib import admin
from .models import DocumentTemplate, DocumentVariable

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active', 'user')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DocumentVariable)
class DocumentVariableAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'label')
    readonly_fields = ('created_at',)

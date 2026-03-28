from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'access_level', 'affiliate', 'uploaded_by', 'uploaded_at']
    list_filter = ['category', 'access_level', 'affiliate']
    search_fields = ['title', 'description']
    ordering = ['-uploaded_at']
    readonly_fields = ['uploaded_at', 'updated_at']

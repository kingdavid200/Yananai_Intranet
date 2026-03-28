from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'affiliate', 'is_pinned', 'created_at']
    list_filter = ['is_pinned', 'affiliate']
    search_fields = ['title', 'body']
    ordering = ['-is_pinned', '-created_at']
    readonly_fields = ['created_at', 'updated_at']

from django.contrib import admin
from .models import Project, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ['title', 'assigned_to', 'status', 'priority', 'due_date']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'affiliate', 'owner', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'affiliate']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'status', 'priority', 'due_date']
    list_filter = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    ordering = ['status', '-priority']

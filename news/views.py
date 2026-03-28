from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Announcement
from .forms import AnnouncementForm


@login_required
def news_list(request):
    user = request.user
    announcements = Announcement.objects.filter(
        Q(affiliate__isnull=True) | Q(affiliate=user.affiliate)
    ).select_related('author', 'affiliate').order_by('-is_pinned', '-created_at')

    return render(request, 'news/list.html', {'announcements': announcements})


@login_required
def news_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    user = request.user

    # Access check: if affiliate-specific, only that affiliate or admin can see it
    if announcement.affiliate and not user.is_admin:
        if announcement.affiliate != user.affiliate:
            messages.error(request, "You do not have access to this announcement.")
            return redirect('news:list')

    return render(request, 'news/detail.html', {'announcement': announcement})


@login_required
def news_create(request):
    if not request.user.is_admin:
        messages.error(request, "Only administrators can create announcements.")
        return redirect('news:list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            messages.success(request, "Announcement published.")
            return redirect('news:list')
    else:
        form = AnnouncementForm()

    return render(request, 'news/form.html', {'form': form, 'action': 'Create'})


@login_required
def news_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not request.user.is_admin:
        messages.error(request, "Only administrators can edit announcements.")
        return redirect('news:list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated.")
            return redirect('news:detail', pk=pk)
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'news/form.html', {'form': form, 'action': 'Edit', 'announcement': announcement})


@login_required
def news_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if not request.user.is_admin:
        messages.error(request, "Only administrators can delete announcements.")
        return redirect('news:list')

    if request.method == 'POST':
        title = announcement.title
        announcement.delete()
        messages.success(request, f"'{title}' has been deleted.")
        return redirect('news:list')

    return render(request, 'news/delete_confirm.html', {'announcement': announcement})

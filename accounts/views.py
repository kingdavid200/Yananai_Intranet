from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .forms import LoginForm, UserRegistrationForm, UserProfileForm
from .models import User, Affiliate
from documents.models import Document
from news.models import Announcement
from projects.models import Project


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_display_name()}!")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect('login')


@login_required
def register_view(request):
    if not request.user.is_admin:
        messages.error(request, "Only administrators can register new users.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.get_display_name()}.")
            return redirect('directory:list')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard_view(request):
    user = request.user

    # Stats
    total_staff = User.objects.filter(is_active=True).count()
    total_documents = Document.objects.count()
    if not user.is_admin:
        total_documents = Document.objects.filter(
            Q(access_level='global') |
            Q(access_level='affiliate', affiliate=user.affiliate)
        ).count()

    active_projects = Project.objects.filter(status='active').count()
    latest_announcements = Announcement.objects.filter(
        Q(affiliate__isnull=True) | Q(affiliate=user.affiliate)
    ).order_by('-is_pinned', '-created_at')[:3]

    context = {
        'total_staff': total_staff,
        'total_documents': total_documents,
        'active_projects': active_projects,
        'latest_announcements': latest_announcements,
    }
    return render(request, 'dashboard.html', context)

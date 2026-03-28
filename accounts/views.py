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
    team = user.team

    # ── Global stats (visible to all) ────────────────────────────────────────
    total_staff = User.objects.filter(is_active=True).count()
    active_projects = Project.objects.filter(status='active').count()

    # Documents — admins see everything; others see global + their affiliate
    if user.is_admin:
        total_documents = Document.objects.count()
        recent_docs = Document.objects.order_by('-created_at')[:5]
    else:
        doc_qs = Document.objects.filter(
            Q(access_level='global') |
            Q(access_level='affiliate', affiliate=user.affiliate)
        )
        total_documents = doc_qs.count()
        recent_docs = doc_qs.order_by('-created_at')[:5]

    # Announcements — global ones + affiliate-specific
    latest_announcements = Announcement.objects.filter(
        Q(affiliate__isnull=True) | Q(affiliate=user.affiliate)
    ).order_by('-is_pinned', '-created_at')[:5]

    # ── Team-specific context ─────────────────────────────────────────────────

    # IT Admin — sees all users breakdown by team + affiliate counts
    team_breakdown = None
    affiliate_counts = None
    if team == 'it_admin' or user.is_admin:
        team_breakdown = (
            User.objects.filter(is_active=True)
            .values('team')
            .annotate(count=Count('id'))
            .order_by('team')
        )
        affiliate_counts = (
            User.objects.filter(is_active=True)
            .values('affiliate__name')
            .annotate(count=Count('id'))
            .order_by('affiliate__name')
        )

    # Global Exec / Board — org-wide project overview
    all_projects = None
    if team in ('global_exec', 'board', 'it_admin') or user.is_admin:
        all_projects = Project.objects.select_related('affiliate').order_by('-created_at')[:10]

    # Regional + country teams — their affiliate's projects and staff
    affiliate_projects = None
    affiliate_staff = None
    if team in ('regional_mgmt', 'india', 'south_africa', 'zambia', 'zimbabwe', 'uk'):
        if user.affiliate:
            affiliate_projects = Project.objects.filter(
                affiliate=user.affiliate, status='active'
            ).order_by('-created_at')[:5]
            affiliate_staff = User.objects.filter(
                affiliate=user.affiliate, is_active=True
            ).order_by('full_name')[:10]

    # ── Team colour for badge ─────────────────────────────────────────────────
    team_color = User.TEAM_COLORS.get(team, User.TEAM_COLORS['general'])
    team_label = dict(User.TEAM_CHOICES).get(team, 'Staff')

    context = {
        # global stats
        'total_staff': total_staff,
        'total_documents': total_documents,
        'active_projects': active_projects,
        'latest_announcements': latest_announcements,
        'recent_docs': recent_docs,
        # team identity
        'user_team': team,
        'team_color': team_color,
        'team_label': team_label,
        # team-specific
        'team_breakdown': team_breakdown,
        'affiliate_counts': affiliate_counts,
        'all_projects': all_projects,
        'affiliate_projects': affiliate_projects,
        'affiliate_staff': affiliate_staff,
    }
    return render(request, 'dashboard.html', context)

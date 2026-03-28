from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import User, Affiliate


@login_required
def directory_list(request):
    users = User.objects.filter(is_active=True).select_related('affiliate')

    # Search
    query = request.GET.get('q', '')
    if query:
        users = users.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(job_title__icontains=query)
        )

    # Filter by role
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)

    # Filter by affiliate/country
    affiliate_filter = request.GET.get('affiliate', '')
    if affiliate_filter:
        users = users.filter(affiliate__id=affiliate_filter)

    affiliates = Affiliate.objects.all().order_by('name')

    context = {
        'users': users,
        'affiliates': affiliates,
        'query': query,
        'role_filter': role_filter,
        'affiliate_filter': affiliate_filter,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'directory/list.html', context)


@login_required
def directory_detail(request, pk):
    profile_user = get_object_or_404(User, pk=pk, is_active=True)
    return render(request, 'directory/detail.html', {'profile_user': profile_user})

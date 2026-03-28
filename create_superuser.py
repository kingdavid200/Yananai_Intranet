"""
Script to create the default superuser and team test accounts for Project Yananai Intranet.
Runs automatically on Railway startup via Procfile.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Affiliate

# ── Affiliates ──────────────────────────────────────────────────────────────
affiliates_data = [
    {'name': 'Yananai UK',           'country': 'United Kingdom', 'timezone': 'Europe/London'},
    {'name': 'Yananai Zambia',       'country': 'Zambia',         'timezone': 'Africa/Lusaka'},
    {'name': 'Yananai India',        'country': 'India',          'timezone': 'Asia/Kolkata'},
    {'name': 'Yananai Zimbabwe',     'country': 'Zimbabwe',       'timezone': 'Africa/Harare'},
    {'name': 'Yananai South Africa', 'country': 'South Africa',   'timezone': 'Africa/Johannesburg'},
]

for data in affiliates_data:
    affiliate, created = Affiliate.objects.get_or_create(
        name=data['name'],
        defaults={'country': data['country'], 'timezone': data['timezone']}
    )
    if created:
        print(f"Created affiliate: {affiliate.name}")

# Handy affiliate lookups
uk_aff = Affiliate.objects.filter(name='Yananai UK').first()
zambia_aff = Affiliate.objects.filter(name='Yananai Zambia').first()
india_aff = Affiliate.objects.filter(name='Yananai India').first()
zimbabwe_aff = Affiliate.objects.filter(name='Yananai Zimbabwe').first()
sa_aff = Affiliate.objects.filter(name='Yananai South Africa').first()

# ── Default accounts ─────────────────────────────────────────────────────────
DEFAULT_PASSWORD = 'Yananai2024!'

accounts = [
    # (email, full_name, role, team, is_superuser, affiliate, job_title)
    (
        'admin@yananai.org',
        'David Harris Chukwuebuka',
        'admin', 'it_admin', True, uk_aff,
        'Webmaster & User Support Engineer',
    ),
    (
        'ceo@yananai.org',
        'Global Executive Lead',
        'staff', 'global_exec', False, uk_aff,
        'Chief Executive Officer',
    ),
    (
        'board@yananai.org',
        'Board Member',
        'staff', 'board', False, uk_aff,
        'Board of Trustees',
    ),
    (
        'regional@yananai.org',
        'Regional Manager',
        'staff', 'regional_mgmt', False, uk_aff,
        'Regional Management Team',
    ),
    (
        'india@yananai.org',
        'India Team Member',
        'staff', 'india', False, india_aff,
        'India Operations',
    ),
    (
        'southafrica@yananai.org',
        'South Africa Team Member',
        'staff', 'south_africa', False, sa_aff,
        'South Africa Operations',
    ),
    (
        'zambia@yananai.org',
        'Zambia Team Member',
        'staff', 'zambia', False, zambia_aff,
        'Zambia Operations',
    ),
    (
        'zimbabwe@yananai.org',
        'Zimbabwe Team Member',
        'staff', 'zimbabwe', False, zimbabwe_aff,
        'Zimbabwe Operations',
    ),
]

for email, full_name, role, team, is_su, affiliate, job_title in accounts:
    if not User.objects.filter(email=email).exists():
        if is_su:
            user = User.objects.create_superuser(
                email=email,
                password='Admin1234!',
                full_name=full_name,
                role=role,
                team=team,
                job_title=job_title,
                affiliate=affiliate,
            )
        else:
            user = User.objects.create_user(
                email=email,
                password=DEFAULT_PASSWORD,
                full_name=full_name,
                role=role,
                team=team,
                job_title=job_title,
                affiliate=affiliate,
                is_staff=False,
            )
        print(f"Created user: {email} (team={team})")
    else:
        # Ensure existing users have the right team set
        u = User.objects.get(email=email)
        if u.team == 'general' and team != 'general':
            u.team = team
            u.save(update_fields=['team'])
            print(f"Updated team for: {email} → {team}")
        else:
            print(f"User already exists: {email}")

print("\n✓ Setup complete.")
print("Admin login:  admin@yananai.org / Admin1234!")
print(f"Team accounts password: {DEFAULT_PASSWORD}")

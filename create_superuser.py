"""
Script to create the default superuser for Project Yananai Intranet.
Run via: python manage.py shell < create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Affiliate

# Create default affiliates
affiliates_data = [
    {'name': 'Yananai UK', 'country': 'United Kingdom', 'timezone': 'Europe/London'},
    {'name': 'Yananai Zambia', 'country': 'Zambia', 'timezone': 'Africa/Lusaka'},
    {'name': 'Yananai India', 'country': 'India', 'timezone': 'Asia/Kolkata'},
    {'name': 'Yananai Zimbabwe', 'country': 'Zimbabwe', 'timezone': 'Africa/Harare'},
    {'name': 'Yananai South Africa', 'country': 'South Africa', 'timezone': 'Africa/Johannesburg'},
]

for data in affiliates_data:
    affiliate, created = Affiliate.objects.get_or_create(
        name=data['name'],
        defaults={'country': data['country'], 'timezone': data['timezone']}
    )
    if created:
        print(f"Created affiliate: {affiliate.name}")

# Create superuser
email = 'admin@yananai.org'
password = 'Admin1234!'

if not User.objects.filter(email=email).exists():
    uk_affiliate = Affiliate.objects.filter(name='Yananai UK').first()
    user = User.objects.create_superuser(
        email=email,
        password=password,
        full_name='David Harris Chukwuebuka',
        role='admin',
        job_title='Webmaster & User Support Engineer',
        affiliate=uk_affiliate,
    )
    print(f"Superuser created: {email}")
    print(f"Password: {password}")
else:
    print(f"Superuser already exists: {email}")

print("\nSetup complete. Visit http://127.0.0.1:8000 to access the intranet.")
print(f"Admin login: {email} / {password}")

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="team",
            field=models.CharField(
                choices=[
                    ("it_admin", "IT Admin"),
                    ("global_exec", "Global Executive Leadership Team"),
                    ("board", "Board of Trustees"),
                    ("regional_mgmt", "Regional Management Team"),
                    ("india", "India Team"),
                    ("south_africa", "South Africa Team"),
                    ("zambia", "Zambia Team"),
                    ("zimbabwe", "Zimbabwe Team"),
                    ("uk", "UK Team"),
                    ("general", "General Staff"),
                ],
                default="general",
                max_length=20,
            ),
        ),
    ]

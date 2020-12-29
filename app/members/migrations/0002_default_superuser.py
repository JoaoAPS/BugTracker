import os
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    def generate_superuser(apps, schema_editor):
        """Create a default superuser if no superuser already exists"""
        from django.contrib.auth import get_user_model

        UserModel = get_user_model()

        if not UserModel.objects.filter(is_superuser=True).exists():
            UserModel.objects.create_superuser(
                name=os.environ.get('DEFAULT_SUPERUSER_NAME'),
                email=os.environ.get('DEFAULT_SUPERUSER_EMAIL'),
                password=os.environ.get('DEFAULT_SUPERUSER_PASSWORD')
            )

    operations = [
        migrations.RunPython(generate_superuser),
    ]

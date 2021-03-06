# Generated by Django 3.1.4 on 2020-12-14 13:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bugs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='_status',
            field=models.CharField(default='WAITING', max_length=15),
        ),
        migrations.AlterField(
            model_name='bug',
            name='assigned_members',
            field=models.ManyToManyField(blank=True, related_name='assigned_bugs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bug',
            name='closingDate',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='bug',
            name='creationDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

# Generated by Django 5.1.1 on 2025-03-14 09:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0101_barangayclearance_resident_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='residents',
            name='auth_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resident_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]

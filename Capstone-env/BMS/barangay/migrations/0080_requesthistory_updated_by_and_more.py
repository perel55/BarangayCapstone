# Generated by Django 5.1.1 on 2025-01-17 02:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0079_requesthistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='requesthistory',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='requesthistory',
            name='status',
            field=models.CharField(max_length=20),
        ),
    ]

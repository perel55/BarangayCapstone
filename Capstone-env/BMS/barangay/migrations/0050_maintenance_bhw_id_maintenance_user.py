# Generated by Django 5.1.1 on 2024-12-03 04:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0049_remove_maintenance_bhw_id_remove_maintenance_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='bhw_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.bhw'),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 5.1.1 on 2024-12-03 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0050_maintenance_bhw_id_maintenance_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenance',
            name='bhw_id',
        ),
    ]

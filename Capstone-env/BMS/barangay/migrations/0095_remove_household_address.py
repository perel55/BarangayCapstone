# Generated by Django 5.1.1 on 2025-01-17 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0094_merge_20250118_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='household',
            name='address',
        ),
    ]

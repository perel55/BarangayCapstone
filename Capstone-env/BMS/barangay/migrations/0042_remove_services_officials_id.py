# Generated by Django 5.1.1 on 2024-12-07 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0041_services_officials_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='officials_id',
        ),
    ]

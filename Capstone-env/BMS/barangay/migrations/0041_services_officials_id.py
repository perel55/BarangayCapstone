# Generated by Django 5.1.1 on 2024-12-07 07:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0040_remove_services_officials_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='officials_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.personnel'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-07 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0017_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='residents',
            name='is_profile_complete',
            field=models.BooleanField(default=False),
        ),
    ]

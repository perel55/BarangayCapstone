# Generated by Django 5.1.1 on 2025-01-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0080_requesthistory_updated_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='secretary',
            name='is_profile_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='secretary',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-08 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0018_residents_is_profile_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='r_date',
        ),
        migrations.AddField(
            model_name='request',
            name='schedule_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='schedule_end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='schedule_start_time',
            field=models.TimeField(null=True),
        ),
    ]
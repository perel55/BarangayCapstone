# Generated by Django 5.1.1 on 2024-10-14 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0010_schedule_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='time',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

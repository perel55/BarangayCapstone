# Generated by Django 5.1.1 on 2024-11-23 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0034_alter_residents_auth_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='age',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='phonenum',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='purok',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='time',
        ),
    ]
# Generated by Django 5.1.1 on 2024-12-05 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0056_remove_maintenance_resident'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maintenance',
            old_name='user',
            new_name='auth_user',
        ),
        migrations.RenameField(
            model_name='maintenance',
            old_name='schedule_id',
            new_name='schedule',
        ),
        migrations.RemoveField(
            model_name='maintenance',
            name='bhwService',
        ),
    ]
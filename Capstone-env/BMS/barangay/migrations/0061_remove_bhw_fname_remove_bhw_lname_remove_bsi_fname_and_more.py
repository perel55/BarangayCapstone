# Generated by Django 5.1.1 on 2024-12-09 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0060_rename_schedule_id_maintenance_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bhw',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='bhw',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='bsi',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='bsi',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='healthadmin',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='healthadmin',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='lname',
        ),
        migrations.RemoveField(
            model_name='residents',
            name='fname',
        ),
        migrations.RemoveField(
            model_name='residents',
            name='lname',
        ),
    ]

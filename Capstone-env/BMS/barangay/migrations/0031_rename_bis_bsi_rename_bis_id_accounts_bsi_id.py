# Generated by Django 5.1.1 on 2024-11-21 00:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0030_rename_bns_bis_rename_bns_id_accounts_bis_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Bis',
            new_name='Bsi',
        ),
        migrations.RenameField(
            model_name='accounts',
            old_name='bis_id',
            new_name='bsi_id',
        ),
    ]
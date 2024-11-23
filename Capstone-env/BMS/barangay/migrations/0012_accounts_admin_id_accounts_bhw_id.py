# Generated by Django 5.1.1 on 2024-11-06 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0011_alter_schedule_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='admin_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.personnel'),
        ),
        migrations.AddField(
            model_name='accounts',
            name='bhw_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.bhw'),
        ),
    ]

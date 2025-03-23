# Generated by Django 5.1.1 on 2025-03-11 01:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0102_remove_payment_resident_remove_payment_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='resident',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.residents'),
        ),
        migrations.AddField(
            model_name='payment',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.services'),
        ),
    ]

# Generated by Django 5.1.1 on 2025-03-12 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0103_payment_resident_payment_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='service',
            new_name='service_id',
        ),
    ]

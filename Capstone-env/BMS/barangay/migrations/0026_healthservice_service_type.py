# Generated by Django 5.1.1 on 2024-11-14 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0025_outbreaks_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthservice',
            name='service_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-12-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0086_alter_immunize_fifth_visit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immunize',
            name='vaccine_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

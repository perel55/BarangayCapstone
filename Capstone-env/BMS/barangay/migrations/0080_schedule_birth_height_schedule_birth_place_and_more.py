# Generated by Django 5.1.1 on 2024-12-18 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0079_remove_immunize_date_remove_immunize_resident_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='birth_height',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='birth_place',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='birth_weight',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='sex',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
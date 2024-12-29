# Generated by Django 5.1.1 on 2024-12-27 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0083_immunizedate_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='immunize',
            name='fifth_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='immunize',
            name='first_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='immunize',
            name='fourth_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='immunize',
            name='second_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='immunize',
            name='third_visit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='ImmunizeDate',
        ),
    ]
# Generated by Django 5.1.1 on 2024-12-29 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0088_alter_immunize_vaccine_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='birth_height',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='birth_weight',
        ),
        migrations.AddField(
            model_name='schedule',
            name='birthdate',
            field=models.DateField(max_length=255, null=True),
        ),
    ]

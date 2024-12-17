# Generated by Django 5.1.1 on 2024-12-16 17:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0072_rename_img_schedule_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Immunize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=100)),
                ('vaccine_description', models.TextField(null=True)),
                ('vaccine_dose', models.IntegerField(null=True)),
                ('age', models.CharField(max_length=100)),
                ('resident_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.residents')),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.schedule')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
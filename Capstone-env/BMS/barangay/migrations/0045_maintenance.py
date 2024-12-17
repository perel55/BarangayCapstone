# Generated by Django 5.1.1 on 2024-12-02 15:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0044_alter_outbreaks_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.CharField(max_length=100)),
                ('date', models.DateField(null=True)),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('bhw_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.bhw')),
                ('healthservice_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.healthservice')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

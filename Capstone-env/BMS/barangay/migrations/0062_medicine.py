# Generated by Django 5.1.1 on 2024-12-11 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0061_remove_bhw_fname_remove_bhw_lname_remove_bsi_fname_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=100)),
                ('medicine_description', models.TextField(null=True)),
                ('medicine_quantity', models.IntegerField(null=True)),
                ('expiration_date', models.DateField(null=True)),
                ('medicine_type', models.CharField(max_length=100)),
                ('picture', models.ImageField(null=True, upload_to='images/')),
                ('maintenece_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.maintenance')),
                ('resident_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='barangay.residents')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

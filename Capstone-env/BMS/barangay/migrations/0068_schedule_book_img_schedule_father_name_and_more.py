# Generated by Django 5.1.1 on 2024-12-15 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0067_rename_maintenance_id_medicine_maintenance'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='book_img',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='father_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='mother_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
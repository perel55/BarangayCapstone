# Generated by Django 5.1.1 on 2025-04-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0107_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communitynotice',
            name='notice_color',
            field=models.CharField(default='#007bff', max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='communitynotice',
            name='notice_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

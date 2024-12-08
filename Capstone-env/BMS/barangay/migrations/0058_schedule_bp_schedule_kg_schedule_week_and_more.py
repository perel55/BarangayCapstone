# Generated by Django 5.1.1 on 2024-12-06 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barangay', '0057_rename_user_maintenance_auth_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='bp',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='kg',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='week',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='status',
            field=models.CharField(default='Pending', max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Maintenance',
        ),
    ]

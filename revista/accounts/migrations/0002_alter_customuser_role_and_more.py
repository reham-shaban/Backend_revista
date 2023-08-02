# Generated by Django 4.2.3 on 2023-08-01 08:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('moderator', 'Moderator'), ('regular-user', 'Regular User'), ('admin', 'Admin')], default='regular-user', max_length=25),
        ),
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 9, 22, 44, 716608, tzinfo=datetime.timezone.utc)),
        ),
    ]
# Generated by Django 4.2.4 on 2023-08-08 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_role_and_more'),
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
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 8, 11, 47, 21, 264048, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-20 10:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_customuser_gender_passwordresetcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 10, 42, 0, 574269, tzinfo=datetime.timezone.utc)),
        ),
    ]

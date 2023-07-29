# Generated by Django 4.2.3 on 2023-07-29 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 29, 17, 39, 34, 489867, tzinfo=datetime.timezone.utc)),
        ),
    ]

<<<<<<< HEAD
# Generated by Django 4.2.3 on 2023-07-30 09:03
=======
# Generated by Django 4.2.3 on 2023-07-30 06:51
>>>>>>> 1b5ef8d192d325113bc1c1cd7734e0c6cc6fdd53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_customuser_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expires_at',
<<<<<<< HEAD
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 30, 9, 33, 51, 684044, tzinfo=datetime.timezone.utc)),
=======
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 30, 7, 21, 34, 508633, tzinfo=datetime.timezone.utc)),
>>>>>>> 1b5ef8d192d325113bc1c1cd7734e0c6cc6fdd53
        ),
    ]

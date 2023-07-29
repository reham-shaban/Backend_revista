# Generated by Django 4.2.3 on 2023-07-29 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='image',
            new_name='profile_image',
        ),
        migrations.AddField(
            model_name='notification',
            name='post_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='profile_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

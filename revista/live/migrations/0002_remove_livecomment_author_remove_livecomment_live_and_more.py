# Generated by Django 4.2.4 on 2023-08-17 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('live', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livecomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='livecomment',
            name='live',
        ),
        migrations.DeleteModel(
            name='Live',
        ),
        migrations.DeleteModel(
            name='LiveComment',
        ),
    ]

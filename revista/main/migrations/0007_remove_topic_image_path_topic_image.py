# Generated by Django 4.2.1 on 2023-05-22 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_topicfollow_unique_user_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='image_path',
        ),
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

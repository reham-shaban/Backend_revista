# Generated by Django 4.2.1 on 2023-05-27 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_profile_profile_image_alter_profile_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='topics/'),
        ),
    ]
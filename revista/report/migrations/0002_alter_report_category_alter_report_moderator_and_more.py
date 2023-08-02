# Generated by Django 4.2.3 on 2023-08-02 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='category',
            field=models.CharField(choices=[('spam', 'Spam'), ('harassment', 'Harassment'), ('inappropriate-content', 'Inappropriate content')], max_length=25),
        ),
        migrations.AlterField(
            model_name='report',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moderator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='moderator_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('resolved', 'Resolved'), ('pending', 'Pending'), ('redirected', 'Redirected')], max_length=25),
        ),
    ]
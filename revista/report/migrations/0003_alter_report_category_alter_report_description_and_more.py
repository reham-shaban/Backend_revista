# Generated by Django 4.2.3 on 2023-08-02 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_alter_report_category_alter_report_moderator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='category',
            field=models.CharField(choices=[('spam', 'Spam'), ('inappropriate-content', 'Inappropriate content'), ('harassment', 'Harassment')], max_length=25),
        ),
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('resolved', 'Resolved'), ('redirected', 'Redirected'), ('pending', 'Pending')], default='pending', max_length=25),
        ),
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.CharField(choices=[('chat', 'Chat'), ('post', 'Post'), ('user', 'User')], max_length=25),
        ),
    ]
# Generated by Django 4.2.3 on 2023-08-02 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reaction',
            field=models.IntegerField(blank=True, choices=[(3, 'haha'), (2, 'love'), (4, 'wow'), (6, 'angry'), (1, 'like'), (5, 'sad')], null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('voice_record', 'Voice Record'), ('text', 'Text'), ('image', 'Image')], max_length=20),
        ),
    ]

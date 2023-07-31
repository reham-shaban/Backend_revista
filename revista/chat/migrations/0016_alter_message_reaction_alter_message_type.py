# Generated by Django 4.2.3 on 2023-07-31 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_alter_message_reaction_alter_message_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reaction',
            field=models.IntegerField(blank=True, choices=[(3, 'haha'), (2, 'love'), (1, 'like'), (5, 'sad'), (6, 'angry'), (4, 'wow')], null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('image', 'Image'), ('text', 'Text'), ('voice_record', 'Voice Record')], max_length=20),
        ),
    ]
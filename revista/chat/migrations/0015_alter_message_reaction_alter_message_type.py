# Generated by Django 4.2.3 on 2023-07-30 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_alter_message_reaction_alter_message_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reaction',
            field=models.IntegerField(blank=True, choices=[(5, 'sad'), (6, 'angry'), (2, 'love'), (1, 'like'), (3, 'haha'), (4, 'wow')], null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='type',
            field=models.CharField(choices=[('text', 'Text'), ('voice_record', 'Voice Record'), ('image', 'Image')], max_length=20),
        ),
    ]

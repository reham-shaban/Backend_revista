# Generated by Django 4.2.4 on 2023-08-17 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0005_alter_message_reaction_alter_message_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_type', models.CharField(choices=[('voice', 'Voice'), ('video', 'Video')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('on_call', models.BooleanField(default=False)),
                ('callee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_calls', to=settings.AUTH_USER_MODEL)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_calls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

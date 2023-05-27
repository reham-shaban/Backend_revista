from django.db.models.signals import post_save  # signal
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser # sender
from main.models import Profile # receiver

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

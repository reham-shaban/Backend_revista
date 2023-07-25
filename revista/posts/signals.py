from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Point, Like, Comment

# Creat point object on creating a new post
@receiver(post_save, sender=Post)
def create_point_on_post_creation(sender, instance, created, **kwargs):
    if created:
        profile = instance.author
        Point.objects.create(post=instance, profile=profile, value=0)

# add 1 point per like
@receiver(post_save, sender=Like)
def increment_point_value(sender, instance, created, **kwargs):
    if created:
        point, created = Point.objects.get_or_create(post=instance.post, profile=instance.profile)
        point.value += 1
        point.save()

# add 3 points per comment
@receiver(post_save, sender=Comment)
def increment_point_value(sender, instance, created, **kwargs):
    if created:
        point, created = Point.objects.get_or_create(post=instance.post, profile=instance.author)
        point.value += 3
        point.save()

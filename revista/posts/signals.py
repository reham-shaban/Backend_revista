from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Point, Like, Comment, Reply

# Creat point object on creating a new post
@receiver(post_save, sender=Post)
def create_point_on_post_creation(sender, instance, created, **kwargs):
    if created:
        Point.objects.create(post=instance)

# add 1 point per like
@receiver(post_save, sender=Like)
def increment_point_value_per_like(sender, instance, created, **kwargs):
    if created:
        point, created = Point.objects.get_or_create(post=instance.post)
        point.value += 1
        point.save()

# add 3 points per comment
@receiver(post_save, sender=Comment)
def increment_point_value_per_comment(sender, instance, created, **kwargs):
    if created:
        point, created = Point.objects.get_or_create(post=instance.post)
        point.value += 3
        point.save()

#adding 4 points per reply
@receiver(post_save, sender=Reply)
def increment_point_vlaue_per_reply(sender, instance, created, **kwargs):
    if created:
        point, created = Point.objects.get_or_create(post=instance.post)
        point.value += 4
        point.save()

# Decrease 1 point per like deletion
@receiver(post_delete, sender=Like)
def decrement_point_value_for_like_deletion(sender, instance, **kwargs):
    point = Point.objects.get(post=instance.post)
    point.value -= 1
    point.save()

# Decrease 3 points per comment deletion
@receiver(post_delete, sender=Comment)
def decrement_point_value_for_comment_deletion(sender, instance, **kwargs):
    point = Point.objects.get(post=instance.post)
    point.value -= 3
    point.save()

# Decrease 3 points per reply deletion
@receiver(post_delete, sender=Reply)
def decrement_point_value_for_reply_deletion(sender, instance, **kwargs):
    point = Point.objects.get(post=instance.post)
    point.value -= 4
    point.save()

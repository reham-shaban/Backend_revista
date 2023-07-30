from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from main.models import Follow
from posts.models import Like, Comment
from .models import Notification

# Follow
@receiver(post_save, sender=Follow)
def send_notification_on_follow(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        # followed data
        followed_user = instance.followed.user
        id = followed_user.id        
        group_name = f'user-notifications-{id}'  # Create a separate group for each user   
        
        # follower data
        follower_username = instance.follower.user.username
        follower_profile_id = instance.follower.id
        detail = f'{follower_username} started following you.'
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        follower_profile_image = instance.follower.user.profile_image
        # check for image
        if not follower_profile_image:
            follower_profile_image = None       
       
        # Create a new Notification object
        notification = Notification.objects.create(
            user = followed_user,
            type = 'Follow',
            profile_image = follower_profile_image,
            profile_id = follower_profile_id,
            detail = detail,
        )       
        # Save the notification to the database
        notification.save()
            
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Follow',
                'profile_id': follower_profile_id,
                'profile_image': follower_profile_image.url,
                'detail' : detail,
                'created_at': created_at
            },
        }       
        print(event)
        
        try:
            async_to_sync(channel_layer.group_send)(group_name, event)
        except Exception as e:
            print('Exception in signals: ', e)

# Post's Notification
# Like
@receiver(post_save, sender=Like)
def send_notification_on_Like(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        post_id = instance.post.id
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        # the user how made the like DATA
        username = instance.profile.user.username
        detail = f'{username} liked your post'
        profile_image = instance.profile.user.profile_image
         
        # the post author DATA
        post_author = instance.post.author.user
        post_author_id = post_author.id
        group_name = f'user-notifications-{post_author_id}' 
        
        # Create a new Notification object
        notification = Notification.objects.create(
            user = post_author,
            type = 'Post',
            profile_image = profile_image,
            post_id = post_id,
            detail = detail,
        )
        # Save the notification to the database
        notification.save()      
        
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Post',
                'post_id': post_id,
                'profile_image': profile_image.url,
                'detail' : detail,
                'created_at': created_at
            },
        }
        print(event)
        
        try:
            async_to_sync(channel_layer.group_send)(group_name, event)
        except Exception as e:
            print('Exception in signals: ', e)

# Comment
@receiver(post_save, sender=Comment)
def send_notification_on_comment(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        post_id = instance.post.id
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        # the user how made the comment DATA
        username = instance.author.user.username
        detail = f'{username} commented on your post'
        profile_image = instance.author.user.profile_image
         
        # the post author DATA
        post_author = instance.post.author.user
        post_author_id = post_author.id
        group_name = f'user-notifications-{post_author_id}' 
        
        # Create a new Notification object
        notification = Notification.objects.create(
            user = post_author,
            type = 'Post',
            profile_image = profile_image,
            post_id = post_id,
            detail = detail,
        )
        # Save the notification to the database
        notification.save()      
        
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Post',
                'post_id': post_id,
                'profile_image': profile_image.url,
                'detail' : detail,
                'created_at': created_at
            },
        }
        print(event)
        
        try:
            async_to_sync(channel_layer.group_send)(group_name, event)
        except Exception as e:
            print('Exception in signals: ', e)

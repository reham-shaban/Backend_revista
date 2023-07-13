from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from main.models import Follow
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
            image = follower_profile_image,
            detail = detail,
        )       
        # Save the notification to the database
        notification.save()
            
        # send a message to the consumer
        event = {
            'type': 'follow_notification',
            'text': {
                'username': follower_username,
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

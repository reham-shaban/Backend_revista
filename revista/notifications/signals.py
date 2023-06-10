from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from django.conf import settings
from asgiref.sync import async_to_sync
import logging

from main.models import Follow

logger = logging.getLogger(__name__)

# signals

# Follow
@receiver(post_save, sender=Follow)
def send_notification_on_follow(sender, instance, created, **kwargs):
    print('Signal handler - send_notification_on_follow')
    
    if created:
        channel_layer = get_channel_layer()
        id = instance.followed.user.id
        group_name = f'user-notifications-{id}'  # Create a separate group for each user       
        
        follower_username = instance.follower.user.username
        follower_profile_image = instance.follower.user.profile_image
        
        if not follower_profile_image:
            follower_profile_image = None
        
        detail = f'{follower_username} started following you.'
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
       
        event = {
            'type': 'follow_notification',
            'text': {
                'username': follower_username,
                'profile_image': follower_profile_image,
                'detail' : detail,
                'created_at': created_at
            },
        }
        
        print(event)
        
        async_to_sync(channel_layer.group_send)(group_name, event)
        print(f'Sent follow_notification event to group {group_name}')


# register
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def send_notification_on_register(sender, instance, created, **kwargs):
#     if created:
#         logger.debug(f"New user {instance.username} registered")
#         # trigger notification to all consumers in the 'user-notification' group
#         channel_layer = get_channel_layer()
#         group_name = 'user-notifications'
#         event = {
#             'type' : 'user_joined',
#             'text' : instance.username
#         }
#         async_to_sync(channel_layer.group_send)(group_name, event)
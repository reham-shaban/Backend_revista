from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from main.models import Follow
from posts.models import Like, Comment, Reply
from chat.models import Message
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
            forward_id = follower_profile_id,
            detail = detail,
        )       
        # Save the notification to the database
        notification.save()
            
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Follow',
                'forward_id': follower_profile_id,
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
        like_author = instance.profile.user
        username = like_author.username
        detail = f'{username} liked your post'
        profile_image = like_author.profile_image
         
        # the post author DATA
        post_author = instance.post.author.user
        post_author_id = post_author.id
        group_name = f'user-notifications-{post_author_id}' 
        
        if like_author == post_author:
            return
        
        # Create a new Notification object
        notification = Notification.objects.create(
            user = post_author,
            type = 'Post',
            profile_image = profile_image,
            forward_id = post_id,
            detail = detail,
        )
        # Save the notification to the database
        notification.save()      
        
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Post',
                'forward_id': post_id,
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
        comment_author = instance.author.user
        username = comment_author.username
        detail = f'{username} commented on your post'
        profile_image = comment_author.profile_image
         
        # the post author DATA
        post_author = instance.post.author.user
        post_author_id = post_author.id
        group_name = f'user-notifications-{post_author_id}' 
        
        if comment_author == post_author:
            return
        
        # Create a new Notification object
        notification = Notification.objects.create(
            user = post_author,
            type = 'Post',
            profile_image = profile_image,
            forward_id = post_id,
            detail = detail,
        )
        # Save the notification to the database
        notification.save()      
        
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Post',
                'forward_id': post_id,
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

# Reply
@receiver(post_save, sender=Reply)
def send_notification_on_reply(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        comment_id = instance.comment.id
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        # the user how made the reply DATA
        reply_author = instance.author.user
        username = reply_author.username
        detail = f'{username} replied to your comment'
        profile_image = reply_author.profile_image
         
        # the comment author DATA
        comment_author = instance.comment.author.user
        comment_author_id = comment_author.id
        group_name = f'user-notifications-{comment_author_id}' 
        
        if reply_author == comment_author:
            return
        
        # Create a new Notification object
        notification = Notification.objects.create(
            user = comment_author,
            type = 'Reply',
            profile_image = profile_image,
            forward_id = comment_id,
            detail = detail,
        )
        # Save the notification to the database
        notification.save()      
        
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Reply',
                'forward_id': comment_id,
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
 
# Chat   
@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        chat = instance.chat
        created_at = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        # sender of message
        sender = instance.author
        profile_image = sender.profile_image
        
        # reciever user
        if sender == chat.user1:
            receiver = chat.user2
        else:
            receiver = chat.user1
        
        group_name = f'user-notifications-{receiver.id}'
        
        # detail
        if instance.type == 'text':
            detail = instance.text
        elif instance.type == 'image':
            detail = 'sent image'
        elif instance.type == 'voice_record':
            detail = 'sent voice_record'
        else:
            detail = ''
                
        # send a message to the consumer
        event = {
            'type': 'notification',
            'text': {
                'type': 'Chat',
                'username': sender.username,
                'forward_id': chat.id,
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

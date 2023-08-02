import random
from django.core.management.base import BaseCommand
from phonenumber_field.phonenumber import PhoneNumber
from faker import Faker
from main.models import Profile, Topic
from posts.models import Post, Like, Comment, Reply, SavedPost
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
      
        # Choose random image for profile
        images = ['\profile_images\ma.jpg', '\profile_images\jj.jpg', '\profile_images\mn.jpg']
        for user in CustomUser.objects.all():
            random_index = random.randint(0, len(images) - 1)
            user.profile_image = images[random_index]
            user.save()
        
        # Create saved posts for profiles
        # for profile in Profile.objects.all():
        #     num_saved_posts = random.randint(0, 5)
        #     posts = Post.objects.order_by('?')[:num_saved_posts]
        #     for post in posts:
        #         SavedPost.objects.get_or_create(
        #             post=post,
        #             profile=profile
        #         )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

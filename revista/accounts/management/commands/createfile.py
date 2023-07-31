import random
from django.core.management.base import BaseCommand
from phonenumber_field.phonenumber import PhoneNumber
from faker import Faker
from accounts.models import CustomUser
from main.models import Profile, Topic
from posts.models import Post, Like, Comment, Reply, SavedPost

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        image_paths = ['/profile_images/a.jpg', '/profile_images/b.jpg', '/profile_images/c.jpg', '/profile_images/d.jpg']

        # Create saved posts for profiles
        for user in CustomUser.objects.all():
            # random_path = random.choice(image_paths)
            # print(random_path)
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.save()
            print(user.first_name , user.last_name)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

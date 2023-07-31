import random
from django.core.management.base import BaseCommand
from phonenumber_field.phonenumber import PhoneNumber
from faker import Faker
from main.models import Profile, Topic
from posts.models import Post, Like, Comment, Reply, SavedPost

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create posts
        for _ in range(30):
            post = Post.objects.create(
                author=random.choice(Profile.objects.all()),
                content=fake.text(),
                link=fake.url(),
                image='\post_images\hyakkimaru.jpg',
            )
            # Add random topics to the post
            post.topics.set(Topic.objects.order_by('?')[:random.randint(1, 3)])
            
            # Create likes for posts
            for _ in range(random.randint(0, 10)):
                Like.objects.create(
                    post=post,
                    profile=random.choice(Profile.objects.all())
                )

            # Create comments for posts
            for _ in range(random.randint(0, 5)):
                comment = Comment.objects.create(
                 post=post,
                   author=random.choice(Profile.objects.all()),
                  content=fake.text()
                )
              
                # Create replies for comments
                for _ in range(random.randint(0, 3)):
                    Reply.objects.create(
                        comment=comment,
                        author=random.choice(Profile.objects.all()),
                        content=fake.text()
                    )

        # Create saved posts for profiles
        for profile in Profile.objects.all().order_by('?')[:random.randint(0, 5)]:
            SavedPost.objects.get_or_create(
                post=post,
                profile=profile
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

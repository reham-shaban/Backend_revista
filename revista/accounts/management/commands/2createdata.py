import random
from django.core.management.base import BaseCommand
from phonenumber_field.phonenumber import PhoneNumber
from faker import Faker
from accounts.models import CustomUser
from main.models import Profile, Topic, TopicFollow, Follow, Block

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create custom users
        images = ['\profile_images\ma.jpg', '\profile_images\jj.jpg', '\profile_images\mn.jpg']
        random_index = random.randint(0, len(images) - 1)
        
        for _ in range(10):
            email = fake.email()
            username = CustomUser.generate_username(email)  # Use the method from the CustomUser model
            user = CustomUser.objects.create_user(
                username=username,
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                email=email,
                password='password',
                profile_image=images[random_index],
                birth_date=fake.date_of_birth(),
                phone_number=PhoneNumber.from_string(fake.phone_number(), region='US'),
                )
            
        # Add dummy bio data for existing profiles
        for profile in Profile.objects.all():
            profile.bio = fake.text()
            profile.save()
            
        # TopicFollow for existing profiles and topics
        for _ in range(30):
            profile = random.choice(Profile.objects.all())
            topic = random.choice(Topic.objects.all())
            
            # Make sure the profile and topic combination is unique
            while TopicFollow.objects.filter(profile=profile, topic=topic).exists():
                profile = random.choice(Profile.objects.all())
                topic = random.choice(Topic.objects.all())

            TopicFollow.objects.create(
                profile=profile,
                topic=topic
            )
       
        # Create follow relationships
        for _ in range(40):
            follower = random.choice(Profile.objects.all())
            followed = random.choice(Profile.objects.exclude(pk=follower.pk))
            
            # Make sure the combination is unique
            while Follow.objects.filter(follower=follower, followed=followed).exists():
                follower = random.choice(Profile.objects.all())
                followed = random.choice(Profile.objects.exclude(pk=follower.pk))
                
            Follow.objects.create(
                follower=follower,
                followed=followed
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

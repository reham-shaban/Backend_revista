import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from phonenumber_field.phonenumber import PhoneNumber
from faker import Faker
from accounts.models import CustomUser, GENDER_CHOICES
from main.models import Profile, Topic, TopicFollow, Follow, Block

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create custom users
        images = ['\profile_images\zain.jpg', '\profile_images\zaamir.jpg', '\profile_images\man.jpg', '\profile_images\girl.jpg', '\profile_images\zz.jpg', '\profile_images\zzz.jpg']
        random_index = random.randint(0, len(images) - 1)
        gender=fake.random_element(elements=GENDER_CHOICES)[0]
        
        for _ in range(30):
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
                gender=gender,
                phone_number=PhoneNumber.from_string(fake.phone_number(), region='US'),
                )
            
        # Add dummy bio data for existing profiles
        for profile in Profile.objects.all():
            profile.bio = fake.text()
            profile.save()
            
        # TopicFollow for existing profiles and topics
        for _ in range(70):
            profile = random.choice(Profile.objects.all())
            topic = random.choice(Topic.objects.all())
            
            # Make sure the profile and topic combination is unique
            while TopicFollow.objects.filter(profile=profile, topic=topic).exists():
                profile = random.choice(Profile.objects.all())
                topic = random.choice(Topic.objects.all())                

            topicfollow = TopicFollow.objects.create(
                profile=profile,
                topic=topic,
                created_at = fake.date_time_between(start_date="-3y", end_date="now", tzinfo=timezone.utc)
            )
       
        # Create follow relationships
        for _ in range(70):
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

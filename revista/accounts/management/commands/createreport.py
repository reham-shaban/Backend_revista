import random
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser
from posts.models import Post
from report.models import Report, TYPE, CATEGORY, STATUS

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Generate dummy data
        for _ in range(30):
            reporter = random.choice(CustomUser.objects.all())
            reported_user = random.choice(CustomUser.objects.exclude(pk=reporter.pk))
            
            Report.objects.create(
                reporter=reporter,
                type=fake.random_element(elements=TYPE)[0],                
                category=fake.random_element(elements=CATEGORY)[0],
                reported_user=reported_user,
                description=fake.text(),
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))


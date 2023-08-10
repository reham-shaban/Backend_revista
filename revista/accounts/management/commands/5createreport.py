import random
from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser
from posts.models import Post
from chat.models import Chat
from report.models import Report, TYPE, CATEGORY, STATUS

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Generate dummy data
        for _ in range(30):
            reporter = random.choice(CustomUser.objects.all())
            reported_user = random.choice(CustomUser.objects.exclude(pk=reporter.pk))
            type = fake.random_element(elements=TYPE)[0]
            status=fake.random_element(elements=STATUS)[0]
            
            reported_post = None
            if type == 'post':
                reported_post = random.choice(Post.objects.all())
                
            reported_chat = None
            if type == 'chat':
                reported_chat = random.choice(Chat.objects.all())
                
            moderator = None
            moderator_comment = None
            if status == 'redirected' or status == 'resolved':
                moderator = random.choice(CustomUser.objects.filter(role='moderator'))
                moderator_comment = fake.text()
            
            Report.objects.create(
                reporter=reporter,
                type=type,                
                category=fake.random_element(elements=CATEGORY)[0],
                reported_user=reported_user,
                description=fake.text(),
                status=status,
                reported_post=reported_post,
                reported_chat=reported_chat,
                moderator=moderator,
                moderator_comment=moderator_comment
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))


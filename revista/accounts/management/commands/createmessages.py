import random
from django.core.management.base import BaseCommand
from phonenumber_field.phonenumber import PhoneNumber
from faker import Faker
from chat.models import Chat, Message, REACTIONS, TYPE

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Loop all chats
        for chat in Chat.objects.all():
            # Create messages for each chat
            for _ in range(random.randint(5, 20)):
                author = random.choice([chat.user1, chat.user2])
                message_type = 'text'
                text = fake.text(max_nb_chars=30) if message_type == 'text' else None
                reaction = random.choice([reaction[0] for reaction in REACTIONS]) if message_type == 'text' else None

                Message.objects.create(chat=chat, author=author, type=message_type, text=text, reaction=reaction)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

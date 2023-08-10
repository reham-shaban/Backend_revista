import random
from django.core.management.base import BaseCommand
from faker import Faker
from main.models import Topic

class Command(BaseCommand):
    help = 'Command information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        topics = [           
            {"name": "animals & pets", "image": "animals__pets.jpg"},
            {"name": "art & crafts", "image": "art__crafts.jpg"},
            {"name": "business", "image": "business.jpg"},
            {"name": "education", "image": "education.jpg"},
            {"name": "entertainment", "image": "entertainment.jpg"},
            {"name": "fashion", "image": "fashion.jpg"},
            {"name": "food", "image": "food.jpg"},
            {"name": "gaming", "image": "gaming.jpg"},
            {"name": "news", "image": "news.jpg"},
            {"name": "social life", "image": "social_life.jpg"},
            {"name": "sports", "image": "sports.jpg"},
            {"name": "travel", "image": "travel.jpg"},
        ]

        for topic_data in topics:
            Topic.objects.create(
                name=topic_data["name"],
                image=f'\\topics\{topic_data["image"]}',
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data.'))

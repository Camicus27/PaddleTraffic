from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from paddle_traffic.models import Location, Event
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Creates dummy data in the database. Clears all existing data from the database.'

    def handle(self, *args, **kwargs):
        # Predefined lists of names
        location_names = ['Central Park', 'Riverside Rec', 'Maple Court', 'Sunset Field', 'Oakwood Center', 'Lakeside Pavilion', 'Greenwood Park', 'Harbor Point', 'Meadowlands Court', 'Riverbend Park']
        user_names = ['Alex', 'Jamie', 'Sam', 'Taylor', 'Jordan', 'Casey', 'Morgan', 'Bailey', 'Cameron', 'Drew']
        event_names = ['Spring Slam', 'Autumn Open', 'Summer Showdown', 'Winter Classic', 'City Championships', 'Regional Cup', 'Friendly Match', 'Elite Tournament', 'Holiday Special', 'Nighttime Bash']

        # Clear existing data
        Location.objects.all().delete()
        Event.objects.all().delete()
        User.objects.all().delete()

        # Create dummy locations
        for name in location_names:
            location = Location(
                name=name,
                latitude=round(random.uniform(-90, 90), 6),
                longitude=round(random.uniform(-180, 180), 6),
                court_count=random.randint(1, 10),
                courts_occupied=random.randint(0, 5),
                number_waiting=random.randint(0, 20),
                estimated_wait_time=timezone.timedelta(minutes=random.randint(5, 120))
            )
            location.save()

        # Create dummy users
        for name in user_names:
            user = User.objects.create_user(username=name.lower(), password='password')
            user.save()

        # Create dummy events
        for name in event_names:
            event = Event(
                name=name,
                description=f'{name} Description',
                location=Location.objects.order_by('?').first(),  # Random location
                host=User.objects.order_by('?').first(),  # Random user
                date=timezone.now().date(),
                time=timezone.now().time()
            )
            event.save()
            # Optionally add some players
            for player in User.objects.order_by('?')[:random.randint(0, 5)]:
                event.players.add(player)
            event.save()

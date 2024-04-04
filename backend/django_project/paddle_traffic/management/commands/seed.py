from django.core.management.base import BaseCommand
from paddle_traffic.models import PickleUser, Group, Location, Event
import json
from datetime import datetime, timedelta, timezone
import os

class Command(BaseCommand):
    help = 'Creates dummy data in the database. Clears all existing data from the database.'

    def handle(self, *args, **kwargs):
        Location.objects.all().delete()
        PickleUser.objects.all().delete()
        Event.objects.all().delete()
        Group.objects.all().delete()

        # Predefined lists of names
        event_organizers, _ = Group.objects.get_or_create(name='Event Organizers')
        players, _ = Group.objects.get_or_create(name='Players')

        administrator = PickleUser.objects.create_superuser("PaddleTrafficCEO", "pickle.coin.ceo@paddletraffic.net", "picklers4life")
        
        organizer1 = PickleUser.objects.create_user("pickle_gym1", "organizer1@paddletraffic.net", "a1")
        organizer2 = PickleUser.objects.create_user("community_organizer39", "organizer2@paddletraffic.net", "a2")
        event_organizers.user_set.add(organizer1, organizer2)

        p1 = PickleUser.objects.create_user("jim4500", "p1@paddletraffic.net", "p1")
        p2 = PickleUser.objects.create_user("aaron9213", "p2@paddletraffic.net", "p2")
        p3 = PickleUser.objects.create_user("david2834", "p3@paddletraffic.net", "p3")
        players.user_set.add(p1, p2, p3)

        print(os.getcwd())
        with open("./paddle_traffic/management/commands/pickle-data.json", 'r') as file:
            data = json.load(file)
            locations = data['locations']
            for loc in locations:
                Location.objects.create(
                    name = loc['name'],
                    latitude = loc['latitude'],
                    longitude = loc['longitude'],
                    court_count = loc['court_count'],
                    courts_occupied = 0,
                    number_waiting = 0,
                    estimated_wait_time = timedelta(minutes=0),
                    calculated_time = datetime.now(timezone.utc),
                    city_state_country = loc['city_state_country']
                )

        """
         = Location.objects.create(
            name="",
            latitude=,
            longitude=,
            court_count=,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        """

        # match1 = Event.objects.create(
        #     name="Pickleball Scrimmage",
        #     description="A casual game between pickleball enthusiasts. All are welcome to join!",
        #     location=crescent_community,
        #     host=organizer1,
        #     date=timezone.now().date(),
        #     time=timezone.now().time(),
        #     isPublic=True
        # )
        # match1.players.add(organizer1, p3)
        # match2 = Event.objects.create(
        #     name="PaddleTraffic Charity Event",
        #     description="Raising money to fund the extended development of PaddleTraffic!",
        #     location=picklecoin_hq,
        #     host=administrator,
        #     date=timezone.now().date(),
        #     time=timezone.now().time(),
        #     isPublic=True
        # )
        # match2.players.add(p1, p2)


        '''
        match3 = Event.objects.create(
            name="Battle of the Picklers",
            description="An epic battle to determine the ultimate Pickler.",
            location=picklecoin_hq,
            host=organizer1,
            date=timezone.now().date(),
            time=timezone.now().time(),
            isPublic=True
        )
        match3.players.add(p1, p2)
        
        match4 = Event.objects.create(
            name="Moon Match",
            description="A chill game of pickleball on the moon.",
            location=the_moon,
            host=organizer2,
            date=timezone.now().date(),
            time=timezone.now().time(),
            isPublic=False
        )
        match4.players.add(p1, p2)

        '''

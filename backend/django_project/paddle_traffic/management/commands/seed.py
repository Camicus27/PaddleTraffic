from django.core.management.base import BaseCommand
from paddle_traffic.models import PickleUser, Group, Location, Event
import json
from datetime import datetime, timedelta, timezone
import os
import pathlib

class Command(BaseCommand):
    help = 'Creates map data in the database. Clears all existing data from the database.'

    def handle(self, *args, **kwargs):
        Location.objects.all().delete()
        PickleUser.objects.all().delete()
        Event.objects.all().delete()
        Group.objects.all().delete()

        # Predefined lists of names
        event_organizers, _ = Group.objects.get_or_create(name='Organizers')
        players, _ = Group.objects.get_or_create(name='Basic')

        administrator = PickleUser.objects.create_superuser(
            "PaddleTrafficCEO", "pickle.coin.ceo@paddletraffic.net", "picklers4life")
        adminEasyLogin = PickleUser.objects.create_superuser(
            "admin", "pickle.coin.ceo@paddletraffic.net", "password")

        organizer1 = PickleUser.objects.create_user(
            "pickle_gym1", "organizer1@paddletraffic.net", "a1")
        organizer2 = PickleUser.objects.create_user(
            "organizer39", "organizer2@paddletraffic.net", "a2")
        event_organizers.user_set.add(organizer1, organizer2)

        p1 = PickleUser.objects.create_user(
            "jim4500", "p1@paddletraffic.net", "p1")
        p2 = PickleUser.objects.create_superuser(
            "aaron", "p2@paddletraffic.net", "aaron")
        p3 = PickleUser.objects.create_user(
            "david2834", "p3@paddletraffic.net", "p3")
        players.user_set.add(p1, p2, p3)

        print(os.getcwd())
        with open(pathlib.Path(__file__).parent / 'pickle-data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            locations = data['locations']
            for loc in locations:
                Location.objects.create(
                    name=loc['name'],
                    latitude=loc['latitude'],
                    longitude=loc['longitude'],
                    court_count=loc['court_count'],
                    courts_occupied=0,
                    number_waiting=0,
                    estimated_wait_time=timedelta(minutes=0),
                    calculated_time=datetime.now(timezone.utc),
                    city_state_country=loc['city_state_country']
                )

        paddleTraffic = Location.objects.create(
            name="PaddleTraffic Demo Day",
            latitude=40.765993,
            longitude=-111.843702,
            court_count=12,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timedelta(minutes=0),
            calculated_time = datetime.now(timezone.utc),
            city_state_country = "Salt Lake City, UT, USA",
        )

        theMoon = Location.objects.create(
            name="The Moon (aaron's secret hideout)",
            latitude = 40.670454,
            longitude = -111.682705,
            court_count=20,
            number_waiting=0,
            estimated_wait_time=timedelta(minutes=0),
            calculated_time = datetime.now(timezone.utc),
            city_state_country = "Gobblers Knob, UT, USA"
        )

        """
         = Location.objects.create(
            name="",
            latitude=,
            longitude=,
            court_count=,
            courts_occupied=,
            number_waiting=,
            estimated_wait_time=timedelta(minutes=0),
            calculated_time=datetime.now(timezone.utc),
            city_state_country=,
        )
        """

        match1 = Event.objects.create(
            name="PaddleTraffic Charity Event",
            description="Raising money to fund the extended development of PaddleTraffic!",
            location=paddleTraffic,
            host=administrator,
            date=datetime.now().date(),
            time=datetime.now().time(),
            isPublic=True
        )

        match2 = Event.objects.create(
            name="Party with aaron",
            description="This is aaron's favorite location, so we're hosting a party here!",
            location=theMoon,
            host=administrator,
            date=datetime.now().date(),
            time=datetime.now().time(),
            isPublic=True
        )

        match2.players.add(p2)

        match1.players.add(p1, p2)
        p1.matches_attended = 1
        p1.matches_created = 0
        p2.matches_attended = 2
        p2.matches_created = 0
        administrator.matches_created = 2
        p1.save()
        p2.save()
        administrator.save()

from django.core.management.base import BaseCommand
from paddle_traffic.models import PickleUser, Group, Location, Event
from django.utils import timezone


class Command(BaseCommand):
    help = 'Creates dummy data in the database. Clears all existing data from the database.'

    def handle(self, *args, **kwargs):
        Location.objects.all().delete()
        PickleUser.objects.all().delete()
        Event.objects.all().delete()
        Group.objects.all().delete()

        # Predefined lists of names
        event_organizers, _ = Group.objects.get_or_create(name='Organizers')
        players, _ = Group.objects.get_or_create(name='Basic')

        administrator = PickleUser.objects.create_superuser("PaddleTrafficCEO", "pickle.coin.ceo@paddletraffic.net", "picklers4life")
        
        organizer1 = PickleUser.objects.create_user("pickle_gym1", "organizer1@paddletraffic.net", "a1")
        organizer2 = PickleUser.objects.create_user("community_organizer39", "organizer2@paddletraffic.net", "a2")
        event_organizers.user_set.add(organizer1, organizer2)

        p1 = PickleUser.objects.create_user("jim4500", "p1@paddletraffic.net", "p1")
        p2 = PickleUser.objects.create_user("aaron9213", "p2@paddletraffic.net", "p2")
        p3 = PickleUser.objects.create_user("david2834", "p3@paddletraffic.net", "p3")
        players.user_set.add(p1, p2, p3)
        

        picklecoin_hq = Location.objects.create(
            name="PaddleTraffic HQ",
            latitude=40.765955, 
            longitude=-111.843613,
            court_count=24,
            courts_occupied=5,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        hogan_park = Location.objects.create(
            name="Hogan Park",
            latitude=40.874055,
            longitude=-111.901010,
            court_count=6,
            courts_occupied=6,
            number_waiting=2,
            estimated_wait_time=timezone.timedelta(minutes=10),
            calculated_time = timezone.now()
        )
        avenue_park = Location.objects.create(
            name="11th Avenue Park",
            latitude=40.783488,
            longitude=-111.862134,
            court_count=6,
            courts_occupied=2,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        ave_and_c = Location.objects.create(
            name="5th Ave & C Street",
            latitude=40.774847,
            longitude=-111.880206,
            court_count=2,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        fairont = Location.objects.create(
            name="Fairont Park-West",
            latitude=40.720147,
            longitude=-111.862813,
            court_count=6,
            courts_occupied=6,
            number_waiting=10,
            estimated_wait_time=timezone.timedelta(minutes=25),
            calculated_time = timezone.now()
        )
        bickley = Location.objects.create(
            name="Bickley",
            latitude=40.716158,
            longitude=-111.877278,
            court_count=1,
            courts_occupied=1,
            number_waiting=4,
            estimated_wait_time=timezone.timedelta(minutes=20),
            calculated_time = timezone.now()
        )
        west_bountiful = Location.objects.create(
            name="West Bountiful",
            latitude=40.895123,
            longitude=-111.901440,
            court_count=4,
            courts_occupied=4,
            number_waiting=1,
            estimated_wait_time=timezone.timedelta(minutes=10),
            calculated_time = timezone.now()
        )
        twin_hollow = Location.objects.create(
            name="Twin Hollow",
            latitude=40.903635,
            longitude=-111.862690,
            court_count=6,
            courts_occupied=5,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        murray = Location.objects.create(
            name="Murray City Park",
            latitude=40.660899,
            longitude=-111.886080,
            court_count=6,
            courts_occupied=6,
            number_waiting=5,
            estimated_wait_time=timezone.timedelta(minutes=25),
            calculated_time = timezone.now()
        )
        cottonwood = Location.objects.create(
            name="Cottonwood",
            latitude=40.651424,
            longitude=-111.842278,
            court_count=3,
            courts_occupied=2,
            number_waiting=1,
            estimated_wait_time=timezone.timedelta(minutes=10),
            calculated_time = timezone.now()
        )
        butler = Location.objects.create(
            name="Butler Park",
            latitude=40.615042,
            longitude=-111.817880,
            court_count=6,
            courts_occupied=6,
            number_waiting=7,
            estimated_wait_time=timezone.timedelta(minutes=20),
            calculated_time = timezone.now()
        )
        centennial = Location.objects.create(
            name="Centennial Park",
            latitude=40.701042,
            longitude=-112.018665,
            court_count=12,
            courts_occupied=9,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        alta_canyon = Location.objects.create(
            name="Alta Canyon",
            latitude=40.576097,
            longitude=-111.834556,
            court_count=4,
            courts_occupied=4,
            number_waiting=13,
            estimated_wait_time=timezone.timedelta(hours=1),
            calculated_time = timezone.now()
        )
        flatiron_mesa = Location.objects.create(
            name="Flatiron Mesa Park",
            latitude=40.597158,
            longitude=-111.840582,
            court_count=5,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        crescent_community = Location.objects.create(
            name="Crescent Community Park",
            latitude=40.550329,
            longitude=-111.882503,
            court_count=4,
            courts_occupied=1,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        independence = Location.objects.create(
            name="Independence Courts",
            latitude=40.478724,
            longitude=-111.920607,
            court_count=4,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        highfield_park = Location.objects.create(
            name="Highfield Park",
            latitude=40.489465, 
            longitude=-112.004133,
            court_count=1,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        wardle_fields = Location.objects.create(
            name="Wardle Fields Regional Park",
            latitude=40.494282,
            longitude=-111.959244,
            court_count=16,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        sierra_newbold = Location.objects.create(
            name="Sierra Newbold Memorial Park",
            latitude=40.593987,
            longitude=-112.034921,
            court_count=6,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        south_jordan = Location.objects.create(
            name="South Jordan Courts",
            latitude=40.550959, 
            longitude=-111.940817,
            court_count=6,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        riverton_city = Location.objects.create(
            name="Riverton City Park",
            latitude=40.520899, 
            longitude=-111.931289,
            court_count=8,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        river_park = Location.objects.create(
            name="River Park",
            latitude=40.557689,
            longitude=-111.909769,
            court_count=2,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        suncrest_park = Location.objects.create(
            name="Suncrest Park",
            latitude=40.473242, 
            longitude=-111.836130,
            court_count=2,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        olympic_park = Location.objects.create(
            name="Olympic Park",
            latitude=40.408878, 
            longitude=-111.893737,
            court_count=3,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        exchange = Location.objects.create(
            name="Courts at The Exchange",
            latitude=40.406861, 
            longitude=-111.908760,
            court_count=4,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        harvest_moon = Location.objects.create(
            name="Harvest Moon Park",
            latitude=40.395414, 
            longitude=-111.926254,
            court_count=2,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        burgess = Location.objects.create(
            name="Burgess Park",
            latitude=40.452565, 
            longitude=-111.782882,
            court_count=4,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        watercress = Location.objects.create(
            name="Watercress Park",
            latitude=40.369987, 
            longitude=-111.847279,
            court_count=2,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        hollow_park = Location.objects.create(
            name="Hollow Park",
            latitude=40.344104, 
            longitude=-111.709021,
            court_count=4,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        easton_park = Location.objects.create(
            name="Easton Park",
            latitude=40.366366, 
            longitude=-111.779704,
            court_count=4,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        creek_side = Location.objects.create(
            name="Creekside Park",
            latitude=40.337107, 
            longitude=-111.729864,
            court_count=2,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        bonneville = Location.objects.create(
            name="Bonneville Park",
            latitude=40.324411, 
            longitude=-111.714777,
            court_count=4,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        sharon_park = Location.objects.create(
            name="Sharon Park",
            latitude=40.306703, 
            longitude=-111.689036,
            court_count=6,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
        )
        rotary = Location.objects.create(
            name="Rotary Park",
            latitude=40.254225, 
            longitude=-111.686344,
            court_count=8,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timezone.timedelta(minutes=0),
            calculated_time = timezone.now()
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

        match1 = Event.objects.create(
            name="Pickleball Scrimmage",
            description="A casual game between pickleball enthusiasts. All are welcome to join!",
            location=crescent_community,
            host=organizer1,
            date=timezone.now().date(),
            time=timezone.now().time(),
            isPublic=True
        )
        match1.players.add(organizer1, p3)
        match2 = Event.objects.create(
            name="PaddleTraffic Charity Event",
            description="Raising money to fund the extended development of PaddleTraffic!",
            location=picklecoin_hq,
            host=administrator,
            date=timezone.now().date(),
            time=timezone.now().time(),
            isPublic=True
        )
        match2.players.add(p1, p2)


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

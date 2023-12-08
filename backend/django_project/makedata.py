import os, django
import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()

from paddle_traffic.models import User, Group, Location, Event

def initial_data():
    
    eventOrganizers, _ = Group.objects.get_or_create(name='Event Organizers')
    players, _ = Group.objects.get_or_create(name='Players')

    administr = User.objects.create_superuser("PickleCoinCEO", "pickle.coin.ceo@paddletraffic.net", "picklers4life")
    organizer1 = User.objects.create_user("organizer1", "organizer1@paddletraffic.net", "a1")
    organizer2 = User.objects.create_user("organizer2", "organizer2@paddletraffic.net", "a2")
    eventOrganizers.user_set.add(organizer1, organizer2)

    p1 = User.objects.create_user("p1", "p1@paddletraffic.net", "p1")
    p2 = User.objects.create_user("p2", "p2@paddletraffic.net", "p2")
    p3 = User.objects.create_user("p3", "p3@paddletraffic.net", "p3")
    players.user_set.add(p1, p2, p3)
    
    
    thePark = Location.objects.create(
        name = "The Park",
        latitude = 40.745929,
        longitude = -111.873945,
        court_count = 4,
        courts_occupied = 2,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    picklecoinHQ = Location.objects.create(
        name = "Picklecoin HQ",
        latitude = 40.767807,
        longitude = -111.845182,
        court_count = 24,
        courts_occupied = 24,
        number_waiting = 15,
        estimated_wait_time = datetime.timedelta(hours=2)
    )
    theMoon = Location.objects.create(
        name = "The Moon",
        latitude = 40.673265,
        longitude = -111.683013,
        court_count = 2,
        courts_occupied = 2,
        number_waiting = 3,
        estimated_wait_time = datetime.timedelta(minutes=15)
    )
    hoganPark = Location.objects.create(
        name = "Hogan Park",
        latitude = 40.874055,
        longitude = -111.901010,
        court_count = 6,
        courts_occupied = 6,
        number_waiting = 2,
        estimated_wait_time = datetime.timedelta(minutes=10)
    )
    avenuePark = Location.objects.create(
        name = "11th Avenue Park",
        latitude = 40.783488,
        longitude = -111.862134,
        court_count = 6,
        courts_occupied = 2,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    aveAndC = Location.objects.create(
        name = "5th Ave & C Street",
        latitude = 40.774847,
        longitude = -111.880206,
        court_count = 2,
        courts_occupied = 0,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    fairont = Location.objects.create(
        name = "Fairont Park-West",
        latitude = 40.720147,
        longitude = -111.862813,
        court_count = 6,
        courts_occupied = 6,
        number_waiting = 10,
        estimated_wait_time = datetime.timedelta(minutes=25)
    )
    bickley = Location.objects.create(
        name = "Bickley",
        latitude = 40.716158,
        longitude = -111.877278,
        court_count = 1,
        courts_occupied = 1,
        number_waiting = 4,
        estimated_wait_time = datetime.timedelta(minutes=20)
    )
    westBountiful = Location.objects.create(
        name = "West Bountiful",
        latitude = 40.895123,
        longitude = -111.901440,
        court_count = 4,
        courts_occupied = 4,
        number_waiting = 1,
        estimated_wait_time = datetime.timedelta(minutes=10)
    )
    twinHollow = Location.objects.create(
        name = "Twin Hollow",
        latitude = 40.903635,
        longitude = -111.862690,
        court_count = 6,
        courts_occupied = 5,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    murray = Location.objects.create(
        name = "Murray City Park",
        latitude = 40.660899,
        longitude = -111.886080,
        court_count = 6,
        courts_occupied = 6,
        number_waiting = 5,
        estimated_wait_time = datetime.timedelta(minutes=25)
    )
    cottonwood = Location.objects.create(
        name = "Cottonwood",
        latitude = 40.651424,
        longitude = -111.842278,
        court_count = 3,
        courts_occupied = 2,
        number_waiting = 1,
        estimated_wait_time = datetime.timedelta(minutes=10)
    )
    butler = Location.objects.create(
        name = "Butler Park",
        latitude = 40.615042,
        longitude = -111.817880,
        court_count = 6,
        courts_occupied = 6,
        number_waiting = 7,
        estimated_wait_time = datetime.timedelta(minutes=20)
    )
    centennial = Location.objects.create(
        name = "Centennial Park",
        latitude = 40.701042,
        longitude = -112.018665,
        court_count = 12,
        courts_occupied = 9,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    altaCanyon = Location.objects.create(
        name = "Alta Canyon",
        latitude = 40.576097,
        longitude = -111.834556,
        court_count = 4,
        courts_occupied = 4,
        number_waiting = 13,
        estimated_wait_time = datetime.timedelta(hours=1)
    )
    flatironMesa = Location.objects.create(
        name = "Flatiron Mesa Park",
        latitude = 40.597158,
        longitude = -111.840582,
        court_count = 5,
        courts_occupied = 0,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    crescentCommunity = Location.objects.create(
        name = "Crescent Community Park",
        latitude = 40.550329,
        longitude = -111.882503,
        court_count = 4,
        courts_occupied = 1,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    
    
    match0 = Event.objects.create(
        name = "Battle of the Picklers",
        description = "An epic battle to determine the ultimate Pickler.",
        location = picklecoinHQ,
        host = organizer1,
        date = datetime.date(2023, 12, 22),
        time = datetime.time(12, 00, 00, 999999, datetime.timezone(datetime.timedelta(hours=-7), "MST"))
    )
    match0.players.add(p1, p2)
    match1 = Event.objects.create(
        name = "Pickleball Scrimmage",
        description = "A casual game between pickleball enthusiasts.",
        location = thePark,
        host = organizer2,
        date = datetime.date(2023, 12, 19),
        time = datetime.time(16, 00, 00, 999999, datetime.timezone(datetime.timedelta(hours=-7), "MST"))
    )
    match1.players.add(p2)
    match2 = Event.objects.create(
        name = "Picklecoin Charity Event",
        description = "Raising money to fund the Picklecoin CEO's new yacht.",
        location = picklecoinHQ,
        host = organizer1,
        date = datetime.date(2023, 12, 20),
        time = datetime.time(15, 30, 00, 999999, datetime.timezone(datetime.timedelta(hours=-7), "MST"))
    )
    match3 = Event.objects.create(
        name = "Moon Match",
        description = "A chill game of pickleball on the moon.",
        location = theMoon,
        host = organizer2,
        date = datetime.date(2023, 12, 24),
        time = datetime.time(20, 00, 00, 999999, datetime.timezone(datetime.timedelta(hours=-7), "MST"))
    )
    match3.players.add(p1, p2, p3)

if __name__ == "__main__":
    initial_data()

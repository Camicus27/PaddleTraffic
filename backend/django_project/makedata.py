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
        latitude = 1.0000,
        longitude = 1.0000,
        court_count = 4,
        courts_occupied = 2,
        number_waiting = 0,
        estimated_wait_time = datetime.timedelta(minutes=0)
    )
    picklecoinHQ = Location.objects.create(
        name = "Picklecoin HQ",
        latitude = 1.0000,
        longitude = 1.0000,
        court_count = 24,
        courts_occupied = 24,
        number_waiting = 15,
        estimated_wait_time = datetime.timedelta(hours=2)
    )
    theMoon = Location.objects.create(
        name = "The Moon",
        latitude = 1.0000,
        longitude = 1.0000,
        court_count = 2,
        courts_occupied = 2,
        number_waiting = 3,
        estimated_wait_time = datetime.timedelta(minutes=15)
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
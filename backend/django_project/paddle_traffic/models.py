from django.db import models
from django.contrib.auth.models import User, Group, AbstractUser
from django.utils import timezone


class PickleUser(AbstractUser):
    SKILL_LEVELS = (
        "Beginner",
        "Advanced Beginner",
        "Intermediate Beginner",
        "Intermediate",
        "Advanced Intermediate",
        "Expert",
        "Advanced Expert",
        "Professional",
    )

    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    matches_attended = models.IntegerField(default=0)
    matches_created = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0)
    loss_count = models.IntegerField(default=0)
    skill_level = models.CharField(
        max_length=21,
        choices=[(level, level) for level in SKILL_LEVELS],
        default="Beginner",
        help_text="Pickleball Skill Level",
    )
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    is_member = models.BooleanField(default=False)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )


"""
Represents a location on the map that has courts, like a park or rec center.
Identified by a lat/long coordinate, it has various information assigned.
How many courts here, how many are occupied, how many people waiting for courts,
and an estimated wait time. Additionally, it can access 'scheduled_events' for references
to all the Events being held at the location.
"""


class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6
    )  # max_digits can change but we can't not have them
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    court_count = models.IntegerField()
    courts_occupied = models.IntegerField()  # current courts occupied
    number_waiting = models.IntegerField()  # current number waiting
    estimated_wait_time = models.DurationField()
    # TODO: calculated_time = models.DateTimeField()


"""
Represents a match or larger scale event/tournament that can be held at a location.
Must have a location and host, and many players can sign up to attend.
Also has some identifying data such as a name (i.e. John Doe's Beginnner Match) and
a date and time to show up for the event.
"""


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="scheduled_events", null=False
    )
    host = models.ForeignKey(
        PickleUser, on_delete=models.CASCADE, related_name="hosted_events", null=False
    )
    players = models.ManyToManyField(
        PickleUser, related_name="attending_events", blank=True
    )
    date = models.DateField()
    time = models.TimeField()
    isPublic = models.BooleanField(default=True, null=False)


class Report(models.Model):
    submission_time = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    number_waiting = models.IntegerField()  # number_waiting at time of report
    courts_occupied = models.IntegerField()  # courts_occupied ^^


class FriendRequest(models.Model):
    requester = models.ForeignKey(
        PickleUser,
        on_delete=models.CASCADE,
        related_name="outgoing_requests",
        null=False,
    )
    receiver = models.ForeignKey(
        PickleUser,
        on_delete=models.CASCADE,
        related_name="incoming_requests",
        null=False,
    )
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ["requester", "receiver"]


# todo add a "proposal" model for people who are proposing to add a new court somewhere?

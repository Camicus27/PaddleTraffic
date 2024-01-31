from django.db import models
from django.contrib.auth.models import User, Group

'''
Represents a location on the map that has courts, like a park or rec center.
Identified by a lat/long coordinate, it has various information assigned.
How many courts here, how many are occupied, how many people waiting for courts,
and an estimated wait time. Additionally, it can access 'scheduled_events' for references
to all the Events being held at the location.
'''
class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # max_digits can change but we can't not have them
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    court_count = models.IntegerField()
    courts_occupied = models.IntegerField()  # current courts occupied
    number_waiting = models.IntegerField()  # current number waiting
    estimated_wait_time = models.DurationField()
    # TODO: calculated_time = models.DateTimeField()
'''
Represents a match or larger scale event/tournament that can be held at a location.
Must have a location and host, and many players can sign up to attend.
Also has some identifying data such as a name (i.e. John Doe's Beginnner Match) and
a date and time to show up for the event.
'''
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2047)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='scheduled_events', null=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events', null=False)
    players = models.ManyToManyField(User, related_name='attending_events', blank=True)
    date = models.DateField()
    time = models.TimeField()

class Report(models.Model):
    submission_time = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    number_waiting = models.IntegerField()  # number_waiting at time of report
    courts_occupied = models.IntegerField()  # courts_occupied ^^


# todo add a "proposal" model for people who are proposing to add a new court somewhere?

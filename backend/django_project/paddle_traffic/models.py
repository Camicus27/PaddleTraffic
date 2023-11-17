from django.db import models
from django.db.models import UniqueConstraint


# Create your models here.


class Location(models.Model):
    latitude = models.DecimalField(decimal_places=6)
    longitude = models.DecimalField(decimal_places=6)
    court_count = models.IntegerField()
    courts_occupied = models.IntegerField()
    number_waiting = models.IntegerField()
    estimated_wait_time = models.DurationField()


class Event(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    datetime = models.DateTimeField()


class Player(models.Model):
    pass


class PlaysIn(models.Model):
    UniqueConstraint(fields=["player, event"], name='unique_player_event')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class EventOrganizer(models.Model):
    pass

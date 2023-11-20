from .models import *
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'latitude',
            'longitude',
            'court_count',
            'courts_occupied',
            'number_waiting',
            'estimated_wait_time',
        ]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'location',
            'datetime',
        ]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'id',  # TODO finish from models
        ]


class PlaysInSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaysIn
        fields = [
            'id',
            'player',
            'event',
        ]


class EventOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOrganizer
        fields = [
            'id',  # TODO finish from models
        ]

from .models import *
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:  # Serializers just return a Meta class
        model = Location  # which hold the class as the type of the model
        fields = [  # and fields of said model
            'id',
            'name',
            'latitude',
            'longitude',
            'court_count',
            'courts_occupied',
            'number_waiting',
            'estimated_wait_time',
        ]

class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'name',
            'latitude',
            'longitude',
            'court_count',
            'courts_occupied',
            'number_waiting',
            'estimated_wait_time',
        ]
        # Make certain fields optional for updates
        extra_kwargs = {
            'name': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
            'court_count': {'required': False},
            'courts_occupied': {'required': False},
            'number_waiting': {'required': False},
            'estimated_wait_time': {'required': False}
        }

"""
    date = serializers.DateField(input_formats=['%Y-%m-%d'])
    time = serializers.TimeField(input_formats=['%H:%M:%S'])
"""
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'description',
            'location',
            'host',
            'players',
            'date',
            'time'
        ]


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'name',
            'description',
            'location',
            'host',
            'players',
            'date',
            'time'
        ]
        extra_kwargs = {
            'name': {'required': False},
            'description': {'required': False},
            'location': {'required': False},
            'host': {'required': False},
            'players': {'required': False},
            'date': {'required': False},
            'time': {'required': False}
        }

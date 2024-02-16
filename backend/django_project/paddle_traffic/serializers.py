from .models import *
from rest_framework import serializers
from time import strftime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickleUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined',
            'friends',
            'matches_attended',
            'matches_created',
            'win_count',
            'loss_count',
            'skill_level',
            'bio',
            'profile_picture',
            'is_member',
            'latitude',
            'longitude',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickleUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'groups',
            'user_permissions',
            'is_staff',
            'is_active',
            'is_superuser',
            'friends',
            'matches_attended',
            'matches_created',
            'win_count',
            'loss_count',
            'skill_level',
            'bio',
            'profile_picture',
            'is_member',
            'latitude',
            'longitude',
        ]
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'groups': {'required': False},
            'user_permissions': {'required': False},
            'is_staff': {'required': False},
            'is_active': {'required': False},
            'is_superuser': {'required': False},
            'friends': {'required': False},
            'matches_attended': {'required': False},
            'matches_created': {'required': False},
            'win_count': {'required': False},
            'loss_count': {'required': False},
            'skill_level': {'required': False},
            'bio': {'required': False},
            'profile_picture': {'required': False},
            'is_member': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
        }


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions'
        ]


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'name',
            'permissions'
        ]
        extra_kwargs = {
            'name': {'required': False},
            'permissions': {'required': False}
        }


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
    location = LocationSerializer()
    date = serializers.DateField(format='%A, %B %d, %Y', input_formats=['%A, %B %d, %Y'])   
    time = serializers.TimeField(format='%I:%M%p', input_formats=['%I:%M%p'])

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


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = [
            'requester',
            'receiver',
            'date_created',
            'accepted'
        ]
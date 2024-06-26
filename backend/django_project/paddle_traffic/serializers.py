from .models import *
from rest_framework import serializers
from time import strftime


class RestrictedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickleUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "matches_attended",
            "matches_created",
            "win_count",
            "loss_count",
            "skill_level",
            "bio",
        ]


class UserSerializer(serializers.ModelSerializer):
    friends = RestrictedUserSerializer(many=True, read_only=True)

    class Meta:
        model = PickleUser
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "user_permissions",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login",
            "date_joined",
            "friends",
            "matches_attended",
            "matches_created",
            "win_count",
            "loss_count",
            "skill_level",
            "bio",
            "is_member",
            "latitude",
            "longitude",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickleUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "user_permissions",
            "is_staff",
            "is_active",
            "is_superuser",
            "friends",
            "matches_attended",
            "matches_created",
            "win_count",
            "loss_count",
            "skill_level",
            "bio",
            "is_member",
            "latitude",
            "longitude",
        ]
        extra_kwargs = {
            "username": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
            "groups": {"required": False},
            "user_permissions": {"required": False},
            "is_staff": {"required": False},
            "is_active": {"required": False},
            "is_superuser": {"required": False},
            "friends": {"required": False},
            "matches_attended": {"required": False},
            "matches_created": {"required": False},
            "win_count": {"required": False},
            "loss_count": {"required": False},
            "skill_level": {"required": False},
            "bio": {"required": False},
            "is_member": {"required": False},
            "latitude": {"required": False},
            "longitude": {"required": False},
        }


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "permissions"]
        extra_kwargs = {"name": {"required": False}, "permissions": {"required": False}}


class LocationSerializer(serializers.ModelSerializer):
    class Meta:  # Serializers just return a Meta class
        model = Location
        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "court_count",
            "courts_occupied",
            "number_waiting",
            "estimated_wait_time",
            "calculated_time",
            "city_state_country"
        ]
        

class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "name",
            "latitude",
            "longitude",
            "court_count",
            "courts_occupied",
            "number_waiting",
            "estimated_wait_time",
            "calculated_time"
        ]
        extra_kwargs = {
            "name": {"required": True},
            "latitude": {"required": True},
            "longitude": {"required": True},
            "court_count": {"required": True},
            "courts_occupied": {"required": False},
            "number_waiting": {"required": False},
            "estimated_wait_time": {"required": False},
            "calculated_time": {"required": False},
        }
        
        
class LocationProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposedLocation
        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "court_count",
            "proposer",
        ]


class LocationProposalCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposedLocation
        fields = [
            "name",
            "latitude",
            "longitude",
            "court_count",
            "proposer",
        ]
        # Make certain fields optional for updates
        extra_kwargs = {
            "name": {"required": True},
            "latitude": {"required": True},
            "longitude": {"required": True},
            "court_count": {"required": True},
            "proposer": {"required": True},
        }
        
        



"""
    date = serializers.DateField(input_formats=['%Y-%m-%d'])
    time = serializers.TimeField(input_formats=['%H:%M:%S'])
"""


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    date = serializers.DateField(
        format="%A, %B %d, %Y", input_formats=["%A, %B %d, %Y"]
    )
    time = serializers.TimeField(format="%I:%M%p", input_formats=["%I:%M%p"])

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "location",
            "host",
            "players",
            "date",
            "time",
            "isPublic",
        ]


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["name", "description", "location", "host", "players", "date", "time", "isPublic"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": False, "allow_blank": True},
            "location": {"required": True},
            "host": {"required": True},
            "players": {"required": False},
            "date": {"required": True},
            "time": {"required": True},
            "isPublic": {"required": True},
        }


class FriendRequestSerializer(serializers.ModelSerializer):
    requester = RestrictedUserSerializer()
    receiver = RestrictedUserSerializer()

    class Meta:
        model = FriendRequest
        fields = ["id", "requester", "receiver", "date_created"]

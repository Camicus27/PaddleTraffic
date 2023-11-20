from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .serializers import *

# Create your views here.

# I figure we'll add more as we go, but here are some examples.

# GET /locations request
def AllLocations():
    # get all Locations
    locations = Location.objects.all()
    # serialize them
    serializer = LocationSerializer(locations, many=True)
    # return the json formatted as an HTTP response
    return JsonResponse(serializer.data)


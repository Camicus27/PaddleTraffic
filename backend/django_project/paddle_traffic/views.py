from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .serializers import *

# Create your views here.

'''
example API controller function
def dataToReturn(request, custom_url_number): # custom_url_number, represents the '1' in the url below. This is setup in urls.py
    if request.method == "POST"
        #  For anything passed through the uri as a query e.g. https://paddletraffic.net/1/dataOrSomething?username=billy&password=secure
        username = request.POST["username"]  # You can get that data here
        password = request.POST["password"]
    elif request.method == "GET"
        # MODEL -> SERIALIZE -> RESPOND
        stuff = StuffModel.objects.all()  # can do things like .where(...), .filter(...), etc.
        serializer = StuffModelSerializer(stuff, many=True)
        return JsonResponse(serializer.data)
    elif ...
        ...
'''


# I figure we'll add more as we go, but here are some examples.

# GET /locations request
def AllLocations(request):
    # get all Locations
    locations = Location.objects.all()
    # serialize them
    serializer = LocationSerializer(locations, many=True)
    # return the json formatted as an HTTP response
    return JsonResponse(serializer.data)


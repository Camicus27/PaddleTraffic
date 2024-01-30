from datetime import datetime

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from paddle_traffic import models as m
from django.contrib.auth.models import User
from django.db import models as django_model
from paddle_traffic import serializers as ser
from paddle_traffic.ApiHttpResponses import *
import json
# Create your views here.

# todo
# no negative people etc, add data checking
#   - clean() methods ... ? yeh... great
# add join event URI endpoint?


"""
example API controller function
def dataToReturn(request, custom_url_number): # custom_url_number, represents the "1" in the url below. This is setup in urls.py
    if request.method == "POST"
        #  For anything passed through the uri as a query e.g. https://paddletraffic.net/1/dataOrSomething?username=billy&password=secure
        username = request.POST["username"]  # You can get that data here
        password = request.POST["password"]
    elif request.method == "GET"
        # MODEL -> SERIALIZE -> RESPOND
        stuff = StuffModel.objects.all()  # can do things like .where(...), .filter(...), .get(...), etc.
        serializer = StuffModelSerializer(stuff, many=True)
        return JsonResponse(serializer.data)
    elif ...
        ...
"""


def index(request):
    return render(request, "index.html")


def index_redirect(request):
    return redirect("/")


def login(request):
    """
    /profile/login
    """
    if request.method == "POST":

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = authenticate(username=username, password=password)
        if user is not None:  # Success
            login(request, user)
            return redirect("/")
        else:  # Failure
            return render(request, "login.html", {"error": "Username and password do not match"})
    else:
        # GET the login page
        return render(request, "login.html")


@csrf_exempt
def users(request):
    """
    /users
    """
    def get():
        all_users = User.objects.all()
        serializer = ser.UserSerializer(all_users, many=True)
        return JsonResponse({"users": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def users_id(request, id):
    """
    /users/{id}
    """
    def get():
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return http_not_found(f"User with ID {id} ")

        serializer = ser.UserSerializer(user)
        return JsonResponse({"user": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def report(request, id):
    """
    /locations/<int:id>/report/
    """
    def post(all_data):
        data = all_data.get("report", None)
        if data is None:
            return http_bad_request_json()
        courts_occupied = data.get("courts_occupied", None)
        number_waiting = data.get("number_waiting", None)
        if courts_occupied is None or number_waiting is None:
            return http_bad_request_json()

        location: m.Location = try_get_instance(m.Location, id)

        if number_waiting > 10:
            return http_bad_argument("Reporting too many people waiting")

        if number_waiting < 0:
            return http_bad_argument("Cannot report negative number of groups waiting")

        if courts_occupied < 0:
            return http_bad_argument("Cannot report negative number of courts occupied")

        if courts_occupied > location.court_count:
            return http_bad_argument("Cannot report more courts occupied than there are courts")

        if courts_occupied < location.court_count and number_waiting > 0:
            return http_bad_argument("Cannot report groups waiting if there are courts unoccupied")

        report: m.Report = m.Report(
            submission_time=datetime.now(),
            location=location,
            number_waiting=number_waiting,
            courts_occupied=courts_occupied
        )
        report.save()

        # todo do calculations and set location occupied and waiting
        location.courts_occupied = courts_occupied  # todo replace
        location.number_waiting = number_waiting
        location.save()

        serializer = ser.LocationSerializer(location)
        return JsonResponse({"location": serializer.data})

    funs = {"POST": post}
    return get_response(request, funs)


@csrf_exempt
def locations(request):
    """
    /locations
    """
    def post(all_data):
        data = all_data.get("location", None)
        if data is None:
            return http_bad_request_json()
        serializer = ser.LocationSerializer(data=data)
        if not serializer.is_valid():
            return http_bad_request_json()
        new_location = serializer.save()
        return http_ok_request_json()

    def get():
        m_locations = m.Location.objects.all()
        serializer = ser.LocationSerializer(m_locations, many=True)
        return JsonResponse({"locations": serializer.data})

    funs = {"POST": post, "GET": get}
    return get_response(request, funs)


@csrf_exempt
def locations_id(request, id):
    """
    /locations/{id}
    """
    def patch(all_data):
        existing_location = try_get_instance(m.Location, id)
        if existing_location is None:
            return http_not_found(str(id))
        data = all_data.get("location", None)
        if data is None:
            return http_bad_request_json()

        serializer = ser.LocationUpdateSerializer(instance=existing_location, data=data)
        if serializer.is_valid():
            updated_location = serializer.save()
        else:
            return http_bad_request_json()
        return http_ok_request_json()

    def get():
        m_location = try_get_instance(m.Location, id)
        serializer = ser.LocationSerializer(m_location, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse({"location": serializer.data})

    def delete():
        location = try_get_instance(m.Location, id)
        if location is None:
            return http_not_found(str(id))
        location.delete()
        return http_ok(f"Location {id} deleted")

    funs = {"PATCH": patch, "GET": get, "DELETE": delete}
    return get_response(request, funs)


@csrf_exempt
def location_bounds(request):
    """
    /locations/bounds/
    """
    def get():
        lon_l = request.GET.get("lon_l", None)
        lon_r = request.GET.get("lon_r", None)
        lat_h = request.GET.get("lat_h", None)
        lat_l = request.GET.get("lat_l", None)

        if None in [lon_l, lon_r, lat_h, lat_l]:
            return http_bad_argument("OOGA BOOGA")

        m_location = m.Location.objects\
            .filter(latitude__lt=lat_h)\
            .filter(latitude__gt=lat_l)\
            .filter(longitude__lt=lon_r)\
            .filter(longitude__gt=lon_l)

        serializer = ser.LocationSerializer(m_location, many=True)
        # return the json formatted as an HTTP response
        return JsonResponse({"locations": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def events(request):
    """
    /events
    """
    def get():
        m_events = m.Event.objects.all()
        serializer = ser.EventSerializer(m_events, many=True)
        return JsonResponse({"events": serializer.data})
    
    def post(all_data):
        data = all_data.get("event", None)
        if data is None:
            return http_bad_request_json()
        serializer = ser.EventSerializer(data=data)
        if not serializer.is_valid():
            return http_bad_request_json()
        new_event = serializer.save()
        return http_ok_request_json()

    def patch(data):
        serializer = ser.EventSerializer(data=data)
        if not serializer.is_valid():
            return http_bad_request_json()

        new_event = serializer.save()
        return http_ok_request_json()

    funs = {"GET": get, "POST": post, "PATCH": patch}
    return get_response(request, funs)


@csrf_exempt
def events_id(request, id):
    def patch(data):
        existing_event = try_get_instance(m.Event, id)
        if existing_event is None:
            return http_not_found(str(id))

        serializer = ser.EventUpdateSerializer(instance=existing_event, data=data)
        if not serializer.is_valid():
            return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")  # Bad Request
        updated_location = serializer.save()
        return http_ok_request_json()

    def get():
        m_event = try_get_instance(m.Event, id)
        if m_event is None:
            return http_not_found(str(id))
        serializer = ser.EventSerializer(instance=m_event, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse({"event": serializer.data})

    def delete():
        m_event = try_get_instance(m.Event, id)
        if m_event is None:
            return http_not_found(str(id))
        m_event.delete()
        return http_ok(f"Event {id} deleted")

    funs = {"PATCH": patch, "GET": get, "DELETE": delete}
    return get_response(request, funs)


"""
--------------- Helper query functions ---------------------------------
"""


def get_response(request, funs) -> HttpResponse:
    if request.method not in funs.keys():
        return http_method_not_allowed()

    if request.method == "POST":
        if "application/json" not in request.content_type:
            return http_unsupported_media()

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return http_bad_request_json()
        return funs["POST"](data)

    elif request.method == "GET":
        return funs["GET"]()

    elif request.method == "PATCH":
        if "application/json" not in request.content_type:
            return http_unsupported_media()
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return http_bad_request_json()
        return funs["PATCH"](data)

    elif request.method == "DELETE":
        return funs["DELETE"]()

    else:
        return http_method_not_allowed()


def try_get_instance(model_class: django_model.Model, id):
    try:
        existing_location = model_class.objects.get(id=id)
        return existing_location
    except model_class.DoesNotExist:
        return None

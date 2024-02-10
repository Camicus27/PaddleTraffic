from datetime import datetime, timedelta, timezone
import math

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from paddle_traffic import models as m
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models as django_model
from paddle_traffic import serializers as ser
from paddle_traffic.ApiHttpResponses import *
import json
import re
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

EXPIRATION_THRESHOLD = timedelta(seconds=5)


def index(request):
    return render(request, "index.html")


def register_view(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname", None)
        lastname = request.POST.get("lastname", None)
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        email = request.POST.get("email", "")
        # Check if user entered valid username, email, password
        if not username:
            return render(request, "register.html", {"error": "Please enter a valid username"})
        if not password:
            return render(request, "register.html", {"error": "Please enter a valid password"})
        if not email or not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            return render(request, "register.html", {"error": "Please enter a valid"})
        # Check if the email is unique
        if email and User.objects.filter(email=email).exists():
            return render(request, "register.html", {"error": "A user with that email already exists"})

        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=firstname, last_name=lastname)
        login(request, user)
        return redirect("/")
    else:
        # GET the register page
        return render(request, "register.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if "" in [username, password]:
            return render(request, "login.html", {"error": "Invalid username and password"})

        user = authenticate(request, username=username, password=password)
        if user is not None:  # Success
            login(request, user)
            return redirect("/")
        else:  # Failure
            return render(request, "login.html", {"error": "Username and password do not match"})
    else:
        if request.user.is_authenticated:
            return redirect("/")

        # GET the login page
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("/")

# Authentication required


def current_user(request):
    def get():
        if not request.user.is_authenticated:
            return http_unauthorized()
        serializer = ser.UserSerializer(request.user)
        return JsonResponse({"user": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


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
            submission_time=datetime.now(timezone.utc),
            location=location,
            number_waiting=number_waiting,
            courts_occupied=courts_occupied
        )
        report.save()

        # TODO: do calculations and set location occupied and waiting
        location.courts_occupied = courts_occupied
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

        serializer = ser.LocationUpdateSerializer(
            instance=existing_location, data=data)
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

        try:
            lat = float(request.GET.get("lat", None))
            lon = float(request.GET.get("lon", None))
        except ValueError:
            return http_bad_argument("OOGA BOOOOOGA")

        if None in [lat, lon]:
            return http_bad_argument("OOGA BOOGA")

        lat_dif = 0.24
        lon_dif = 1.4

        lat_h = lat + (lat_dif / 2)
        lat_l = lat - (lat_dif / 2)
        lon_l = lon - (lon_dif / 2)
        lon_r = lon + (lon_dif / 2)

        m_location = m.Location.objects\
            .filter(latitude__lt=lat_h)\
            .filter(latitude__gt=lat_l)\
            .filter(longitude__lt=lon_r)\
            .filter(longitude__gt=lon_l)

        for loc in m_location:
            current_time = datetime.now(timezone.utc)
            time_passed = current_time - loc.calculated_time
            stay_time = 3600  # 1 hour in seconds, for equal groups waiting to number of courts, gg L + bozo + ratio + balding + malding + ur_mom

            # account for groups there - if busier stay less if empty stay longer => ratio between total groups there and number of courts
            total_groups = loc.number_waiting + loc.courts_occupied
            busyness_ratio = (total_groups / loc.court_count)
            SOFTEN_CONSTANT = 4
            softened_busyness_ratio = (busyness_ratio + SOFTEN_CONSTANT - 1) / SOFTEN_CONSTANT
            stay_time /= softened_busyness_ratio
            groups_leaving = math.floor(time_passed.seconds / stay_time)
            if groups_leaving <= 0:
                continue
            if loc.number_waiting > 0:
                loc.number_waiting = max(loc.number_waiting - groups_leaving, 0)
                loc.save()
                loc.calculated_time = current_time
            elif loc.courts_occupied > 0:
                loc.courts_occupied = max(loc.courts_occupied - groups_leaving, 0)
                loc.save()
                loc.calculated_time = current_time
            # if it's been a certain amount of time based on latest report
            # then update the location, save it, and then return it!

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

        serializer = ser.EventUpdateSerializer(
            instance=existing_event, data=data)
        if not serializer.is_valid():
            # Bad Request
            return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")
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

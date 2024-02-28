from datetime import datetime, timedelta, timezone

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from paddle_traffic import models as m
from django.contrib.auth import get_user_model
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


def index(request, username=None):
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
            return render(
                request, "register.html", {"error": "Please enter a valid username"}
            )
        if not re.search("[a-zA-Z]", username):
            return render(
                request,
                "register.html",
                {
                    "error": "Please enter a username with at least one alphabetic character"
                },
            )
        if not password:
            return render(
                request, "register.html", {"error": "Please enter a valid password"}
            )
        if not email or not re.fullmatch(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email
        ):
            return render(
                request, "register.html", {"error": "Please enter a valid email"}
            )
        # Check if the email is unique
        if email and get_user_model().objects.filter(email=email).exists():
            return render(
                request,
                "register.html",
                {"error": "A user with that email already exists"},
            )

        # Check if the username is unique
        if username and get_user_model().objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {"error": "A user with that username already exists"},
            )

        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname,
        )
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
            return render(
                request, "login.html", {"error": "Invalid username and password"}
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:  # Success
            login(request, user)
            return redirect("/")
        else:  # Failure
            return render(
                request, "login.html", {"error": "Username and password do not match"}
            )
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
        all_users = get_user_model().objects.all()
        serializer = ser.RestrictedUserSerializer(all_users, many=True)
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
            user = get_user_model().objects.get(pk=id)
        except get_user_model().DoesNotExist:
            return http_not_found(f"User with ID {id} ")

        serializer = ser.RestrictedUserSerializer(user)
        return JsonResponse({"user": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def users_username(request, username):
    """
    /users/{username}
    """

    def get():
        try:
            # Change from .get(pk=id) to .get(username=username)
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return http_not_found(f"User with username '{username}' not found.")

        serializer = ser.RestrictedUserSerializer(user)
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
            return http_bad_argument(
                "Cannot report more courts occupied than there are courts"
            )

        if courts_occupied < location.court_count and number_waiting > 0:
            return http_bad_argument(
                "Cannot report groups waiting if there are courts unoccupied"
            )

        report: m.Report = m.Report(
            submission_time=datetime.now(timezone.utc),
            location=location,
            number_waiting=number_waiting,
            courts_occupied=courts_occupied,
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

        m_location = (
            m.Location.objects.filter(latitude__lt=lat_h)
            .filter(latitude__gt=lat_l)
            .filter(longitude__lt=lon_r)
            .filter(longitude__gt=lon_l)
        )

        for loc in m_location:
            latest_report = (
                m.Report.objects.filter(location=loc)
                .order_by("-submission_time")
                .first()
            )
            if latest_report is None or latest_report.submission_time is None:
                continue
            # TODO: Make decay vary with how long since calculation stored in locations model
            if (
                datetime.now(timezone.utc) - latest_report.submission_time
                > EXPIRATION_THRESHOLD
            ):
                if loc.number_waiting > 0:
                    loc.number_waiting -= 1
                    loc.save()
                elif loc.courts_occupied > 0:
                    loc.courts_occupied -= 1
                    loc.save()
            # if it's been a certain amount of time based on latest report
            # then update the location, save it, and then return it!

        serializer = ser.LocationSerializer(m_location, many=True)
        # return the json formatted as an HTTP response
        return JsonResponse({"locations": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def friend_requests(request):
    """
    /friend-requests/
    These all require that the user is signed in, and are in the context of a user's friend requests.
    """

    def get():
        if not request.user.is_authenticated:
            return http_unauthorized()

        # Fetch incoming friend requests where the current user is the receiver
        incoming_requests = m.FriendRequest.objects.filter(
            receiver=request.user, accepted=False
        )
        incoming_serializer = ser.FriendRequestSerializer(incoming_requests, many=True)

        # Fetch outgoing friend requests where the current user is the requester
        outgoing_requests = m.FriendRequest.objects.filter(
            requester=request.user, accepted=False
        )
        outgoing_serializer = ser.FriendRequestSerializer(outgoing_requests, many=True)

        # Return both lists as JSON
        return JsonResponse(
            {
                "incoming_requests": incoming_serializer.data,
                "outgoing_requests": outgoing_serializer.data,
            }
        )

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def friend_request_id(request: HttpRequest, id):
    """
    /friend-requests/{id}
    These all require that the user is signed in, and are in the context of a user's friend requests.
    """

    """
    In this case, {id} represents the id of the friend request
    """

    def get():
        if not request.user.is_authenticated:
            return http_unauthorized()
        friend_request: m.FriendRequest = try_get_instance(m.FriendRequest, id)
        if not friend_request:
            return http_not_found(str(id))
        if not (
            friend_request.requester == request.user
            or friend_request.receiver == request.user
        ):  # A user should not be able to get a friend request that does not belong to them
            return http_unauthorized()
        serializer = ser.LocationSerializer(friend_request, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse({"friend_request": serializer.data})

    """
    In this case, {id} represents the id of the receiving user.
    This is the endpoint to create a new friend request.
    """

    def post(data):
        if not request.user.is_authenticated:
            return http_unauthorized()
        other_user = try_get_instance(m.PickleUser, id)
        if not other_user:
            return http_not_found(str(id))
        if other_user == request.user:
            return http_bad_argument(f"id: {id} cannot be the same as current user")
        m.FriendRequest(
            requester=request.user,
            receiver=other_user,
        ).save()
        return http_ok(
            f"Friend Request for users {request.user.id} and {id} was created."
        )

    """
    In this case, {id} represents the id of the friend request
    """

    def delete():
        if not request.user.is_authenticated:
            return http_unauthorized()
        friend_request: m.FriendRequest = try_get_instance(m.FriendRequest, id)
        if not friend_request:
            return http_not_found(str(id))
        if not (
            friend_request.requester == request.user
            or friend_request.receiver == request.user
        ):  # A user should not be able to get a friend request that does not belong to them
            return http_unauthorized()
        friend_request.delete()
        return http_ok(f"Friend Request {id} deleted")

    funs = {"GET": get, "POST": post, "DELETE": delete}
    return get_response(request, funs)


@csrf_exempt
def accept_friend_request(request, id):
    """
    /friend-requests/accept/{id}
    """

    """
    In this case, {id} represents the id of the friend request
    """

    def post(data):
        if not request.user.is_authenticated:
            return http_unauthorized()
        friend_request: m.FriendRequest = try_get_instance(m.FriendRequest, id)
        if not friend_request:
            return http_not_found(str(id))
        if (
            friend_request.receiver != request.user
        ):  # A user should not be able to accept a friend request if they are not the receiver
            return http_unauthorized()
        friend_request.accepted = True
        friend_request.save()
        friend_request.receiver.friends.add(
            friend_request.requester
        )  # Since this field is symmetric, this also adds the receiver as a friend of the requester
        return http_ok(
            f"Friends {friend_request.receiver} and {friend_request.requester} are now friends"
        )

    funs = {"POST": post}
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
        print(data)
        serializer = ser.EventUpdateSerializer(data=data)
        if not serializer.is_valid():
            return http_bad_request_json()
        serializer.save()
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
            return HttpResponse(
                "Invalid JSON data", status=400, content_type="text/plain"
            )  # Bad Request
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

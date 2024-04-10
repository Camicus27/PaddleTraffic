from datetime import datetime, timedelta, timezone
import requests
import math
import json
import re

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from paddle_traffic import models as m
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import models as django_model
from paddle_traffic import serializers as ser
from paddle_traffic.ApiHttpResponses import *
from django.db.models import ExpressionWrapper, FloatField, F
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
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


"""
User login tests to verify a user's group.

@user_passes_test(is_basic_user)   -->  is_event_organizer    is_admin
@login_required
"""


def is_basic_user(user):
    return user.groups.filter(name="Basic").exists()


def is_event_organizer(user):
    return user.groups.filter(name="Organizers").exists()


def is_admin(user):
    return user.is_superuser


"""
Google Maps Geocoding API
"""
def get_address(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key=AIzaSyBjqdNRs9JW2yfvq8Lbnp-tgr12PR_RCPw"

    try:
        response = requests.get(url)
        data = response.json()
        
        # Extract city, state, and country from the response
        if data["status"] == "OK":
            address_components = data["results"][0]["address_components"]
            city = next((component["long_name"] for component in address_components if "locality" in component["types"]), None)
            state = next((component["short_name"] for component in address_components if "administrative_area_level_1" in component["types"]), None)
            country = next((component["short_name"] for component in address_components if "country" in component["types"]), None)
        
            formatted_city_state_country = ""
            if city:
                formatted_city_state_country += ", " + city
            if state:
                formatted_city_state_country += ", " + state
            if country:
                formatted_city_state_country += ", " + country
            
            if len(formatted_city_state_country) == 0:
                return "No Info"
            else:
                return formatted_city_state_country.strip(", ")
        else:
            return "No Info"
        
    except Exception as e:
        print("Error:", e)
        return None


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
                request, "register.html", {
                    "error": "Please enter a valid username"}
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
                request, "register.html", {
                    "error": "Please enter a valid password"}
            )
        if not email or not re.fullmatch(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email
        ):
            return render(
                request, "register.html", {
                    "error": "Please enter a valid email"}
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
                request, "login.html", {
                    "error": "Invalid username and password"}
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:  # Success
            login(request, user)
            return redirect("/")
        else:  # Failure
            return render(
                request, "login.html", {
                    "error": "Username and password do not match"}
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


@csrf_exempt
def current_user(request):
    def get():
        if not request.user.is_authenticated:
            return http_unauthorized()
        serializer = ser.UserSerializer(request.user)
        return JsonResponse({"user": serializer.data})

    def patch(all_data):
        if not request.user.is_authenticated:
            return http_unauthorized()
        data = all_data.get("user", None)
        if data is None:
            return http_bad_request_json()
        if data.get("id") != request.user.id:
            return http_unauthorized()
        serializer = ser.UserUpdateSerializer(
            instance=request.user, data=data)
        if serializer.is_valid():
            updated_user = serializer.save()
        else:
            return http_bad_request_json()
        return http_ok_request_json()

    funs = {"GET": get, "PATCH": patch}
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


def calculate_exponential(reports, percentage, time_passed):
    # Calculate weights using exponential decay
    values = [r.number_waiting + r.courts_occupied for r in reports]
    times = [((datetime.now(timezone.utc) -
              r.submission_time).total_seconds() / 3600) for r in reports]

    # Decay rate for 0.1=e^lambda*6 ln(0.1)/6 = lambda
    lambda_value = -math.log(percentage) / time_passed
    weights_exp = [math.exp(-lambda_value * t) for t in times]

    weighted_values_exp = [w * v for w, v in zip(weights_exp, values)]

    weighted_average_exp = sum(weighted_values_exp) / sum(weights_exp)
    return round(weighted_average_exp)


def verify_distance(lat, lon, location):
    court_lat = location.latitude
    court_lon = location.longitude
    distance_to_location = math.sqrt(
        (lat - float(court_lat)) ** 2 + (lon - float(court_lon)) ** 2)
    # 0.00725 is 0.5 miles in lat/lon coords (at equator)
    VERIFICATION_DISTANCE = 0.00725 * 10  # TODO: Decrease dist to realistic value
    return distance_to_location < VERIFICATION_DISTANCE


@csrf_exempt
def report(request, id):
    """
    /locations/<int:id>/report/
    """
    cookie_key = 'TIME_LIMIT'

    def post(all_data):
        data = all_data.get("report", None)
        report_data = data.get("reportData", None)
        if report_data is None:
            return http_bad_request_json()
        courts_occupied = report_data.get("courts_occupied", None)
        number_waiting = report_data.get("number_waiting", None)
        lat = data.get("lat", None)
        lon = data.get("lon", None)

        if courts_occupied is None or number_waiting is None:
            return http_bad_request_json()

        location: m.Location = try_get_instance(m.Location, id)
        if not verify_distance(lat, lon, location):
            return http_unauthorized()

        cookie = request.COOKIES.get(cookie_key, None)
        if cookie:
            time_of_last_request = datetime.strptime(
                cookie, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - time_of_last_request < timedelta(seconds=20):
                return http_too_many_requests()

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
        four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=4)
        reports_for_calculation = m.Report.objects.filter(
            location=location).filter(submission_time__gt=four_hours_ago)

        percentage = 0.25
        time_passed = 4  # IN HOURS
        new_total_groups = calculate_exponential(
            reports_for_calculation, percentage, time_passed)

        if new_total_groups <= location.court_count:
            location.courts_occupied = new_total_groups
            location.number_waiting = 0
        else:
            location.courts_occupied = location.court_count
            location.number_waiting = new_total_groups - location.court_count
        location.calculated_time = datetime.now(timezone.utc)
        calculate_wait_time(location)
        location.save()

        serializer = ser.LocationSerializer(location)

        response = JsonResponse({"location": serializer.data})

        report_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        response.set_cookie(cookie_key, report_time)
        return response

    funs = {"POST": post}
    return get_response(request, funs)


@csrf_exempt
def locations(request):
    """
    /locations
    """

    def get():
        m_locations = m.Location.objects.all()
        serializer = ser.LocationSerializer(m_locations, many=True)
        return JsonResponse({"locations": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def location_list(request):
    def post(data):
        locIds = data.get("locationIds", None)
        if not locIds:
            return JsonResponse({"locations": []})
        locations = m.Location.objects.filter(id__in=locIds)
        locations = lazy_decay(locations)
        serializer = ser.LocationSerializer(locations, many=True)
        return JsonResponse({"locations": serializer.data})

    funs = {"POST": post}
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


def get_locations_by_lat_lon(lat, lon):
    LAT_DIF = 1
    LON_DIF = 1

    lat_h = lat + (LAT_DIF / 2)
    lat_l = lat - (LAT_DIF / 2)
    lon_l = lon - (LON_DIF / 2)
    lon_r = lon + (LON_DIF / 2)

    m_locations = m.Location.objects\
        .filter(latitude__lt=lat_h)\
        .filter(latitude__gt=lat_l)\
        .filter(longitude__lt=lon_r)\
        .filter(longitude__gt=lon_l)
    return m_locations


def get_locations_by_boundary(lat1, lon1, lat2, lon2):
    lat_h = lat2 if lat2 > lat1 else lat1
    lat_l = lat2 if lat2 < lat1 else lat1
    lon_l = lon2 if lon2 < lon1 else lon1
    lon_r = lon2 if lon2 > lon1 else lon1

    m_locations = m.Location.objects\
        .filter(latitude__lt=lat_h)\
        .filter(latitude__gt=lat_l)\
        .filter(longitude__lt=lon_r)\
        .filter(longitude__gt=lon_l)
    return m_locations


def lazy_decay(locations):
    for loc in locations:
        if (loc.court_count == 0):
            loc.delete()
            continue
        current_time = datetime.now(timezone.utc)
        time_passed = current_time - loc.calculated_time
        stay_time = 3600  # 1 hour in seconds, for equal groups waiting to number of courts

        # account for groups there - if busier stay less if empty stay longer => ratio between total groups there and number of courts
        total_groups = loc.number_waiting + loc.courts_occupied
        busyness_ratio = (total_groups / loc.court_count)
        SOFTEN_CONSTANT = 4
        softened_busyness_ratio = (
            busyness_ratio + SOFTEN_CONSTANT - 1) / SOFTEN_CONSTANT
        stay_time /= softened_busyness_ratio

        groups_leaving = math.floor(time_passed.seconds / stay_time)
        if groups_leaving <= 0:
            continue

        if loc.number_waiting > 0:
            leftover = groups_leaving - loc.number_waiting

            loc.number_waiting = max(loc.number_waiting - groups_leaving, 0)

            if (leftover > 0):
                loc.courts_occupied = max(loc.courts_occupied - leftover, 0)
            loc = calculate_wait_time(loc)
            loc.calculated_time = current_time
            loc.save()
        elif loc.courts_occupied > 0:
            loc.courts_occupied = max(loc.courts_occupied - groups_leaving, 0)
            loc = calculate_wait_time(loc)
            loc.calculated_time = current_time
            loc.save()
    return locations


def calculate_wait_time(location: m.Location):
    # (AVG_GAME_TIME / court_count) * (number_waiting + 1)
    if (location.number_waiting + location.courts_occupied < location.court_count):
        location.estimated_wait_time = timedelta(minutes=0)
        return location

    AVG_GAME_TIME = 20
    est_wait_time = (AVG_GAME_TIME / location.court_count) * \
        (location.number_waiting + 1)
    t_delta = timedelta(minutes=est_wait_time)
    location.estimated_wait_time = t_delta
    return location


@csrf_exempt
def location_latlon(request):
    def get():

        try:
            lat = float(request.GET.get("lat", None))
            lon = float(request.GET.get("lon", None))
        except ValueError:
            return http_bad_argument("Malformed Latlon")

        if None in [lat, lon]:
            return http_bad_argument("Malformed Latlon")

        m_locations = get_locations_by_lat_lon(lat, lon)
        m_locations = lazy_decay(m_locations)
        m_location = m_locations.annotate(
            distance=ExpressionWrapper(
                (F('latitude') - lat) ** 2 +
                (F('longitude') - lon) ** 2,
                output_field=FloatField()
            )
        ) \
            .order_by('distance').first()

        serializer = ser.LocationSerializer(m_location, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse({"location": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


def cluster(m_locations, NUM_CLUSTERS):
    # Example data (replace this with your data)
    locations = list(m_locations)
    coordinates = [(loc.latitude, loc.longitude) for loc in locations]
    coordinates_array = np.array(coordinates)

    kmeans = KMeans(n_clusters=NUM_CLUSTERS)

    kmeans.fit(coordinates_array)
    clusters = kmeans.predict(coordinates_array)

    cluster_centers = kmeans.cluster_centers_
    closest_points_indices, _ = pairwise_distances_argmin_min(
        cluster_centers, coordinates_array)
    closest_objects = [locations[index] for index in closest_points_indices]
    return closest_objects


@csrf_exempt
def location_bounds(request):
    """
    /locations/bounds/
    """

    def get():

        try:
            lat1 = float(request.GET.get("lat1", None))
            lon1 = float(request.GET.get("lon1", None))
            lat2 = float(request.GET.get("lat2", None))
            lon2 = float(request.GET.get("lon2", None))
        except ValueError:
            return http_bad_argument("Malformed Latlon")

        if None in [lat1, lon1, lat2, lon2]:
            return http_bad_argument("Malformed Latlon")

        m_locations = get_locations_by_boundary(lat1, lon1, lat2, lon2)
        m_locations = lazy_decay(m_locations)

        NUM_CLUSTERS = 20
        if (len(m_locations) >= NUM_CLUSTERS):
            m_locations = cluster(m_locations, NUM_CLUSTERS)

        serializer = ser.LocationSerializer(m_locations, many=True)
        # return the json formatted as an HTTP response
        return JsonResponse({"locations": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def location_proposal(request):
    """
    /location/new
    """

    def get():
        if not request.user.is_authenticated or not is_admin(request.user):
            return http_unauthorized()

        m_locations = m.ProposedLocation.objects.all()

        serializer = ser.LocationProposalSerializer(m_locations, many=True)
        return JsonResponse({"new_locations": serializer.data})

    def post(all_data):

        if not request.user.is_authenticated:
            return http_unauthorized()

        data = all_data.get("location", None)
        if data is None:
            return http_bad_request_json()

        # Cleanse data
        lat = data.get("latitude", None)
        long = data.get("longitude", None)
        court_count = data.get("court_count", None)

        if lat is None or long is None or court_count is None:
            return http_bad_request_json()
        
        try:
            lat = float(lat)
            long = float(long)
        except ValueError:
            return http_bad_request_json()

        if lat < -90 or lat > 90:
            return http_bad_argument("Invalid latitude")

        if long < -180 or long > 180:
            return http_bad_argument("Invalid longitude")

        if court_count < 1:
            return http_bad_argument("Cannot have zero or negative courts at a location")
        
        data["latitude"] = lat
        data["longitude"] = long
        
        serializer = ser.LocationProposalCreationSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            return http_bad_request_json()
        new_location = serializer.save()

        return http_ok_request_json()

    funs = {"GET": get, "POST": post}
    return get_response(request, funs)


@user_passes_test(is_admin)
@csrf_exempt
def location_proposal_id(request, id):
    """
    /location/new/{id}
    """

    def post(all_data):
        proposal: m.ProposedLocation = try_get_instance(m.ProposedLocation, id)
        if proposal is None:
            return http_not_found("Proposal does not exist.")

        # Get and serialize data from admin
        data = all_data.get("location", None)
        if data is None:
            return http_bad_request_json()
        serializer = ser.LocationProposalSerializer(data=data)
        if not serializer.is_valid():
            return http_bad_request_json()

        # Retrieve information from proposal
        name = serializer.data.get('name')
        latitude = serializer.data.get('latitude')
        longitude = serializer.data.get('longitude')
        court_count = serializer.data.get('court_count')
        
        formatted_address = get_address(latitude,longitude)
        if formatted_address is None:
            http_bad_argument("Latitude/Longitude geocoordinate not found")

        # Create a new location
        m.Location(
            name=name,
            latitude=latitude,
            longitude=longitude,
            court_count=court_count,
            courts_occupied=0,
            number_waiting=0,
            estimated_wait_time=timedelta(minutes=0),
            calculated_time=datetime.now(timezone.utc),
            city_state_country=formatted_address
        ).save()

        # Remove the proposal
        proposal.delete()
        return http_ok_request_json()

    def delete():
        # Find the proposal
        proposal: m.ProposedLocation = try_get_instance(m.ProposedLocation, id)
        if proposal is None:
            return http_not_found(f"Proposal ${id}")

        # Remove the proposal
        proposal.delete()
        return http_ok(f"Request successfully deleted")

    funs = {"POST": post, "DELETE": delete}
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
            receiver=request.user)
        incoming_serializer = ser.FriendRequestSerializer(
            incoming_requests, many=True)

        # Fetch outgoing friend requests where the current user is the requester
        outgoing_requests = m.FriendRequest.objects.filter(
            requester=request.user
        )
        outgoing_serializer = ser.FriendRequestSerializer(
            outgoing_requests, many=True)

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
        if id in [f.id for f in request.user.friends.all()]:
            return http_bad_argument(f"Cannot Send a friend request to a user that you are already friends with")
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
        friend_request.delete()
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
        m_events = None

        # Public events & private events the user is participating in
        if request.user.is_authenticated:
            user_events = m.Event.objects.filter(django_model.Q(
                host=request.user) | django_model.Q(players=request.user))
            m_events = m.Event.objects.filter(django_model.Q(
                isPublic=True) | django_model.Q(id__in=user_events))

        # No logged in user, only public events
        else:
            m_events = m.Event.objects.filter(isPublic=True)

        serializer = ser.EventSerializer(m_events, many=True)
        return JsonResponse({"events": serializer.data})

    def post(all_data):
        if not request.user.is_authenticated:
            return http_unauthorized()

        data = all_data.get("event", None)
        if data is None:
            return http_bad_request_json()

        serializer = ser.EventUpdateSerializer(data=data)
        if not serializer.is_valid():
            return http_bad_request_json()
        serializer.save()

        request.user.matches_created += 1
        if request.user.id in data.get("players"):
            request.user.matches_attended += 1
        request.user.save()

        return http_ok_request_json()

    def patch(data):
        if not request.user.is_authenticated:
            return http_unauthorized()

        serializer = ser.EventSerializer(data=data)
        if not serializer.is_valid():
            return http_bad_request_json()

        new_event = serializer.save()
        return http_ok_request_json()

    funs = {"GET": get, "POST": post, "PATCH": patch}
    return get_response(request, funs)


@csrf_exempt
def events_id(request, id):
    def get():
        m_event = try_get_instance(m.Event, id)
        if m_event is None:
            return http_not_found(str(id))
        serializer = ser.EventSerializer(instance=m_event, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse({"event": serializer.data})

    """
    This is the endpoint to create a new join event request.
    """

    def post(data):
        if not request.user.is_authenticated:
            return http_unauthorized()

        # Get the event and verify it exists
        m_event = try_get_instance(m.Event, id)
        if m_event is None:
            return http_not_found(f"Event was not found ({str(id)}).")

        isJoining = data.get("joining")
        if isJoining is None:
            return http_bad_request_json()

        # Joining an event
        if isJoining:
            # Verify the user is not already in the event
            if m_event.players.filter(id=request.user.id).exists():
                return http_bad_argument(f"User already is participating in event ({str(id)}).")

            # Add player to event and save
            try:
                m_event.players.add(request.user)
                m_event.save()
                request.user.matches_attended += 1
                request.user.save()
                return http_ok(f"User added to event ({str(id)}) successfully.")
            except:
                return http_bad_argument(f"Error adding user to event ({str(id)}).")
        # Leaving an event
        else:
            # Verify the user is not already not in the event
            if not m_event.players.filter(id=request.user.id).exists():
                return http_bad_argument(f"User is already not participating in event ({str(id)}).")

            # Remove player from event and save
            try:
                m_event.players.remove(request.user)
                m_event.save()
                request.user.matches_attended -= 1
                request.user.save()
                return http_ok(f"User removed from event ({str(id)}) successfully.")
            except:
                return http_bad_argument(f"Error removing user from event ({str(id)}).")

    def patch(data):
        existing_event = try_get_instance(m.Event, id)
        if existing_event is None:
            return http_not_found(str(id))

        serializer = ser.EventUpdateSerializer(
            instance=existing_event, data=data)
        if not serializer.is_valid():
            return HttpResponse(
                "Invalid JSON data", status=400, content_type="text/plain"
            )  # Bad Request
        updated_event = serializer.save()
        return http_ok_request_json()

    def delete():
        m_event = try_get_instance(m.Event, id)
        if m_event is None:
            return http_not_found(str(id))
        m_event.delete()
        return http_ok(f"Event {id} deleted")

    funs = {"GET": get, "POST": post, "PATCH": patch, "DELETE": delete}
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

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from paddle_traffic import models as m
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models as django_model
from paddle_traffic import serializers as ser
import json
import re
# Create your views here.

# todo
# no negative people etc, add data checking
#   - clean() methods ... ? yeh... great
# add join event URI endpoint?
# where id is None potentially return something that is "none"?


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

        user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
        login(request, user)
        return redirect("/")
    else:
        #GET the register page
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
            return HttpUnauthorized()
        serializer = ser.UserSerializer(request.user)
        return JsonResponse({"user": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)

@csrf_exempt
def users(request):
    """
    GET /users
    POST /users

    :param request:
    :return: JsonResponse
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
    GET /users/{id}
    :param request:
    :param id: id of the user
    :return: JsonResponse
    """
    def get():
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return HttpNotFound(f"User with ID {id} ")

        serializer = ser.UserSerializer(user)
        return JsonResponse({"user": serializer.data})

    funs = {"GET": get}
    return get_response(request, funs)


@csrf_exempt
def report(request, id):
    def post(all_data):
        location: m.Location = try_get_instance(m.Location, id)
        data = all_data.get("report", None)
        if data is None:
            return HttpBadRequestJson()
        courts_occupied = data.get("courts_occupied", None)
        number_waiting = data.get("number_waiting", None)
        if courts_occupied is None or number_waiting is None:
            return HttpBadRequestJson()
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
    GET /locations
    POST /locations

    :param request:
    :return: JsonResponse
    """
    def post(all_data):
        data = all_data.get("location", None)
        if data is None:
            return HttpBadRequestJson()
        serializer = ser.LocationSerializer(data=data)
        if not serializer.is_valid():
            return HttpBadRequestJson()
        new_location = serializer.save()
        return HttpOKRequestJson()

    def get():
        m_locations = m.Location.objects.all()
        serializer = ser.LocationSerializer(m_locations, many=True)
        return JsonResponse({"locations": serializer.data})

    funs = {"POST": post, "GET": get}
    return get_response(request, funs)


@csrf_exempt
def locations_id(request, id):
    """
    GET /locations/{id}
    :param request:
    :param id: id of location
    :return: JsonResponse
    """
    def patch(all_data):
        existing_location = try_get_instance(m.Location, id)
        if existing_location is None:
            return HttpNotFound(str(id))
        data = all_data.get("location", None)
        if data is None:
            return HttpBadRequestJson()

        serializer = ser.LocationUpdateSerializer(instance=existing_location, data=data)
        if serializer.is_valid():
            updated_location = serializer.save()
        else:
            return HttpBadRequestJson()
        return HttpOKRequestJson()

    def get():
        m_location = try_get_instance(m.Location, id)
        serializer = ser.LocationSerializer(m_location, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse({"location": serializer.data})

    def delete():
        location = try_get_instance(m.Location, id)
        if location is None:
            return HttpNotFound(str(id))
        location.delete()
        return HttpOK(f"Location {id} deleted")

    funs = {"PATCH": patch, "GET": get, "DELETE": delete}
    return get_response(request, funs)


@csrf_exempt
def events(request):
    def get():
        m_events = m.Event.objects.all()
        serializer = ser.EventSerializer(m_events, many=True)
        return JsonResponse({"events": serializer.data})
    
    def post(all_data):
        data = all_data.get("event", None)
        if data is None:
            return HttpBadRequestJson()
        serializer = ser.EventSerializer(data=data)
        if not serializer.is_valid():
            return HttpBadRequestJson()
        new_event = serializer.save()
        return HttpOKRequestJson()

    def patch(data):
        serializer = ser.EventSerializer(data=data)
        if not serializer.is_valid():
            return HttpBadRequestJson()

        new_event = serializer.save()
        return HttpOKRequestJson()

    funs = {"GET": get, "POST": post, "PATCH": patch}
    return get_response(request, funs)


@csrf_exempt
def events_id(request, id):
    def patch(data):
        existing_event = try_get_instance(m.Event, id)
        if existing_event is None:
            return HttpNotFound(str(id))

        serializer = ser.EventUpdateSerializer(instance=existing_event, data=data)
        if not serializer.is_valid():
            return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")  # Bad Request
        updated_location = serializer.save()
        return HttpOKRequestJson()

    def get():
        m_event = try_get_instance(m.Event, id)
        if m_event is None:
            return HttpNotFound(str(id))
        serializer = ser.EventSerializer(instance=m_event, many=False)
        # return the json formatted as an HTTP response
        return JsonResponse({"event": serializer.data})

    def delete():
        m_event = try_get_instance(m.Event, id)
        if m_event is None:
            return HttpNotFound(str(id))
        m_event.delete()
        return HttpOK(f"Event {id} deleted")

    funs = {"PATCH": patch, "GET": get, "DELETE": delete}
    return get_response(request, funs)


def get_response(request, funs) -> HttpResponse:
    if request.method not in funs.keys():
        return HttpMethodNotAllowed()

    if request.method == "POST":
        if "application/json" not in request.content_type:
            return HttpUnsupportedMedia()

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return HttpBadRequestJson()
        return funs["POST"](data)

    elif request.method == "GET":
        return funs["GET"]()

    elif request.method == "PATCH":
        if not "application/json" in request.content_type:
            return HttpUnsupportedMedia()
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return HttpBadRequestJson()
        return funs["PATCH"](data)

    elif request.method == "DELETE":
        return funs["DELETE"]()

    else:  # shouldn't ever get called...
        return HttpMethodNotAllowed()


"""
Helper query stuff
"""


def try_get_instance(model_class: django_model.Model, id):
    try:
        existing_location = model_class.objects.get(id=id)
        return existing_location
    except model_class.DoesNotExist:
        return None


"""
Status Codes
200 OK: Successful request and processing of JSON data.
400 Bad Request: Invalid JSON data.
405 Method Not Allowed: Request method other than POST is not allowed.
404 Not Found
415 Unsupported Media Type: Requested content type (JSON) is not supported.
"""
def HttpOK(msg):
    return HttpResponse(msg, status=200, content_type="text/plain")  # OK

def HttpBadRequestJson():
    return HttpResponse("Invalid JSON data", status=400, content_type="text/plain")  # Bad Request

def HttpOKRequestJson():
    return HttpResponse("Received and processed JSON data", status=200, content_type="text/plain")  # OK

def HttpUnsupportedMedia():
    return HttpResponse("Unsupported Media Type", status=415, content_type="text/plain")  # Unsupported Media Type

def HttpMethodNotAllowed():
    return HttpResponse("Method Not Allowed", status=405, content_type="text/plain")  # Method Not Allowed

def HttpNotFound(msg):
    return HttpResponse(msg + "Not Found", status=404, content_type="text/plain")

def HttpUnauthorized():
    return HttpResponse("Unathorized", status=401, content_type="text/plain") # If requires authentication
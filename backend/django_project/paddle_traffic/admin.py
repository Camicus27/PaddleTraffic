from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Event, Location, PickleUser

admin.site.register(Event)
admin.site.register(Location)
admin.site.register(PickleUser, UserAdmin)


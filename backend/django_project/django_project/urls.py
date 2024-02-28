"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from paddle_traffic import views

#  Add custom numbered, lettered, named, urls using the following
#  path('<int:custom_url_number>/locations/')
urlpatterns = [
    # Routes from Vue router
    path('', views.index),
    # Redirect these for now bc of Vue static file weirdness
    # todo remove??
    path('map/', views.index),
    path('matchmaking/', views.index),
    path('about/', views.index),
    path('profile/', views.index),
    path('profile/<str:username>', views.index),

    path('admin/', admin.site.urls),
    path('users/', views.users),
    path('users/<int:id>/', views.users_id),
    path('users/<str:username>', views.users_username),
    path('locations/', views.locations),
    path('locations/<int:id>/', views.locations_id),
    path('locations/<int:id>/report/', views.report),
    path('locations/bounds/', views.location_bounds),
    path('location/latlon/', views.location_latlon),
    path('events/', views.events),
    path('events/<int:id>/', views.events_id),

    path('login/', views.login_view),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('current-user/', views.current_user),

    # Friend Requests
    path('friend-requests/', views.friend_requests, name='friend_requests'),  # List all friend requests for the logged-in user
    path('friend-requests/<int:id>/', views.friend_request_id, name='friend_request_detail'),  # Get, delete a specific friend request, or create a new one with the receiver's ID
    path('friend-requests/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),  # Accept a friend request
    #  Add custom numbered, lettered, named, urls using the following
    #  path('<int:custom_url_number>/locations/')
]

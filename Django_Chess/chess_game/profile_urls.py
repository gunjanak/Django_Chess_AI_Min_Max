from django.urls import path
from .profile_views import profile_view

urlpatterns = [
    path('', profile_view, name='profile'),
]

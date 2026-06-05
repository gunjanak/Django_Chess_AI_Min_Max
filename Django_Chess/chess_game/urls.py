from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_home, name='game_home'),
    path('play/', views.play_view, name='play'),
    path('save/', views.save_game, name='save_game'),
]

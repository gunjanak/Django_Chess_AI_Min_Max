from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('game/', include('chess_game.urls')),
    path('profile/', include('chess_game.profile_urls')),
    path('', RedirectView.as_view(url='/game/', permanent=False)),
]

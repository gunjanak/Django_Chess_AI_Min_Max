from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ChessUser

@admin.register(ChessUser)
class ChessUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'elo', 'wins', 'losses', 'draws', 'games_played')
    fieldsets = UserAdmin.fieldsets + (
        ('Chess Stats', {'fields': ('elo', 'wins', 'losses', 'draws', 'games_played')}),
    )

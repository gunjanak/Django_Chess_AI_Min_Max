from django.contrib import admin
from .models import GameRecord

@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'result', 'ai_depth', 'elo_before', 'elo_after', 'played_at', 'duration_s')
    list_filter = ('result', 'ai_depth')
    search_fields = ('user__username',)
    readonly_fields = ('played_at',)

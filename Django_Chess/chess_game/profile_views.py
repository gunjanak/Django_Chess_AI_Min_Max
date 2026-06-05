from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import GameRecord
from .elo import AI_ELO_BY_DEPTH
import json

User = get_user_model()

@login_required
def profile_view(request):
    user = request.user
    recent_games = GameRecord.objects.filter(user=user)[:20]

    # ELO trend (last 20 games reversed)
    elo_history = list(reversed([
        {'date': g.played_at.strftime('%m/%d'), 'elo': g.elo_after, 'result': g.result}
        for g in recent_games
    ]))

    # Stats by depth
    depth_stats = {}
    for depth in range(1, 6):
        games = GameRecord.objects.filter(user=user, ai_depth=depth)
        depth_stats[depth] = {
            'ai_elo': AI_ELO_BY_DEPTH[depth],
            'games': games.count(),
            'wins': games.filter(result='win').count(),
            'losses': games.filter(result='loss').count(),
            'draws': games.filter(result='draw').count(),
        }

    return render(request, 'chess_game/profile.html', {
        'player': user,
        'recent_games': recent_games,
        'elo_history_json': json.dumps(elo_history),
        'depth_stats': depth_stats,
    })

import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import GameRecord
from .elo import new_elo, AI_ELO_BY_DEPTH


def game_home(request):
    depths = list(AI_ELO_BY_DEPTH.items())
    return render(request, 'chess_game/home.html', {'depths': depths})


@login_required
def play_view(request):
    depth = int(request.GET.get('depth', 2))
    depth = max(1, min(5, depth))
    ai_elo = AI_ELO_BY_DEPTH.get(depth, 1000)
    depths = list(AI_ELO_BY_DEPTH.items())
    return render(request, 'chess_game/play.html', {
        'depth': depth,
        'ai_elo': ai_elo,
        'player_elo': request.user.elo,
        'depths': depths,
    })


@login_required
@require_POST
def save_game(request):
    try:
        data = json.loads(request.body)
        result = data.get('result')
        ai_depth = int(data.get('ai_depth', 2))
        pgn = data.get('pgn', '')
        duration_s = int(data.get('duration_s', 0))

        if result not in ('win', 'loss', 'draw'):
            return JsonResponse({'error': 'Invalid result'}, status=400)

        user = request.user
        ai_elo = AI_ELO_BY_DEPTH.get(ai_depth, 1000)
        elo_before = user.elo
        updated_elo, _ = new_elo(elo_before, ai_elo, result)

        GameRecord.objects.create(
            user=user,
            result=result,
            ai_depth=ai_depth,
            elo_before=elo_before,
            elo_after=updated_elo,
            pgn=pgn,
            duration_s=duration_s,
        )

        user.elo = updated_elo
        user.games_played += 1
        if result == 'win':
            user.wins += 1
        elif result == 'loss':
            user.losses += 1
        else:
            user.draws += 1
        user.save()

        return JsonResponse({
            'status': 'ok',
            'elo_before': elo_before,
            'elo_after': updated_elo,
            'elo_change': updated_elo - elo_before,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

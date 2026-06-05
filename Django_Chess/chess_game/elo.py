"""ELO calculation utilities."""

AI_ELO_BY_DEPTH = {1: 800, 2: 1000, 3: 1200, 4: 1400, 5: 1600}
K_FACTOR = 32

def expected_score(player_elo, opponent_elo):
    return 1 / (1 + 10 ** ((opponent_elo - player_elo) / 400))

def new_elo(player_elo, opponent_elo, result):
    """result: 'win'=1, 'loss'=0, 'draw'=0.5"""
    score_map = {'win': 1.0, 'loss': 0.0, 'draw': 0.5}
    score = score_map[result]
    exp = expected_score(player_elo, opponent_elo)
    change = round(K_FACTOR * (score - exp))
    return max(100, player_elo + change), change

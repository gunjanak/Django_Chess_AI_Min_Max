# Chess Arena — Django Chess Platform

A full Django web application wrapping the chess minimax AI with user accounts,
ELO tracking, game history, and a profile dashboard.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. (Optional) Create superuser for admin
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Then open http://127.0.0.1:8000/

## Project Structure

```
chess_platform/          ← Django project root
├── chess_platform/      ← settings, root urls, wsgi
├── accounts/            ← ChessUser model, register/login/logout
│   ├── models.py        ← ChessUser(AbstractUser) + elo/wins/losses/draws
│   ├── forms.py
│   ├── views.py
│   └── urls.py
├── chess_game/          ← Game logic, save endpoint, profile
│   ├── models.py        ← GameRecord
│   ├── elo.py           ← ELO calculation (K=32, AI ELOs by depth)
│   ├── views.py         ← game_home, play_view, save_game
│   ├── profile_views.py ← profile dashboard
│   ├── urls.py
│   └── profile_urls.py
├── templates/
│   ├── base.html        ← shared nav/layout
│   ├── accounts/        ← register.html, login.html
│   └── chess_game/      ← home.html, play.html, profile.html
├── static/
├── db.sqlite3           ← created after migrate
└── requirements.txt
```

## URL Map

| URL | View |
|-----|------|
| `/` | → `/game/` redirect |
| `/game/` | Depth selector home |
| `/game/play/?depth=N` | Play chess vs AI (depth 1–5) |
| `/game/save/` | POST endpoint — saves game result |
| `/profile/` | Player dashboard |
| `/accounts/register/` | Registration |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/admin/` | Django admin |

## ELO System

- AI ELO by depth: 1→800, 2→1000, 3→1200, 4→1400, 5→1600
- K-factor: 32
- Player starting ELO: 1200
- Formula: `new_elo = old_elo + K * (score - expected_score)`

## Chess Engine

The chess game uses:
- **chess.js** — move generation, game state, PGN
- **chessboard.js** — drag-and-drop board UI
- **Minimax with alpha-beta pruning** — built-in JS, depth-configurable
- **Piece-square tables** — positional bonuses for pawns/knights

After game over, JavaScript POSTs to `/game/save/` with:
```json
{ "result": "win|loss|draw", "ai_depth": 2, "pgn": "...", "duration_s": 120 }
```

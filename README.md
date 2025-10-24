# Connect 4

A simple Connect 4 game with a React frontend and a Django backend (with AI opponent).

## Rules

- Board: 7 columns × 6 rows.
- Players drop one piece per turn in any non-full column.
- First to connect four in a row (horizontal, vertical, or diagonal) wins.
- If the board fills with no 4-in-a-row, it’s a draw.
- In this UI: Player = Yellow (1), AI = Red (2).

## How to Run

Prerequisites:
- Python 3.10+ and Node.js 18+

Backend (Django):
- From project root:
  ```bash
  cd backend
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  # Start server on 8000
  python manage.py runserver 0.0.0.0:8000
  ```
- API base URL: http://localhost:8000

Frontend (React + Vite):
- From project root:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```
- Open the app at the URL (e.g., http://localhost:5173).

## Endpoints (JSON)

- GET `/api/new-game/` → `{ board }`
- POST `/api/apply-move/` with `{ board, column, piece }` → `{ board, game_over, winner }`
- POST `/api/ai-move/` with `{ board, depth }` → `{ board, game_over, winner }`

## How the AI Works

- Search: Minimax with alpha–beta pruning to a fixed depth (e.g., 4–5 plies).
- Evaluation: Scores 4-cell “windows” across rows, columns, and diagonals.
  - Rewards: 4-in-a-row (win), 3-in-a-row with an empty, 2-in-a-row.
  - Penalties: Opponent 3-in-a-row with an empty (block threats).
  - Center bias: Prefers playing the center column (more potential connections).
- Move choice: Picks the column with the highest evaluated outcome; falls back to a random legal move if needed.
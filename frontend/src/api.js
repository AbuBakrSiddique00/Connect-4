const API_BASE = import.meta.env.VITE_API_BASE || '' // empty uses Vite proxy

export async function newGame() {
  const res = await fetch(`${API_BASE}/api/new-game/`)
  if (!res.ok) throw new Error('Failed to start new game')
  return res.json()
}

export async function applyMove(board, column, piece = 1) {
  const res = await fetch(`${API_BASE}/api/apply-move/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ board, column, piece }),
  })
  if (!res.ok) throw new Error('Invalid move')
  return res.json()
}

export async function aiMove(board, depth = 5) {
  const res = await fetch(`${API_BASE}/api/ai-move/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ board, depth }),
  })
  if (!res.ok) throw new Error('AI move failed')
  return res.json()
}

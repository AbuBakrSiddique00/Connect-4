import React, { useEffect, useState } from 'react'
import Board from './components/Board.jsx'
import { newGame, applyMove, aiMove } from './api.js'

export default function App() {
  const [board, setBoard] = useState(null)
  const [status, setStatus] = useState('Loading...')
  const [gameOver, setGameOver] = useState(false)
  const [winner, setWinner] = useState(null)
  const [loading, setLoading] = useState(false)

  async function startNewGame() {
    setLoading(true)
    try {
      const data = await newGame()
      setBoard(data.board)
      setGameOver(false)
      setWinner(null)
      setStatus('Your turn')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    startNewGame()
  }, [])

  async function onColumnClick(col) {
    if (!board || loading || gameOver) return
    setLoading(true)

    try {
      // Player move
      const moveRes = await applyMove(board, col, 1)
      setBoard(moveRes.board)

      if (moveRes.game_over) {
        setGameOver(true)
        setWinner(moveRes.winner)
        setStatus(moveRes.winner ? `${moveRes.winner} wins!` : 'Draw!')
        return
      }

      setStatus('AI is thinking...')

      // AI move
      const aiRes = await aiMove(moveRes.board, 5)
      setBoard(aiRes.board)
      if (aiRes.game_over) {
        setGameOver(true)
        setWinner(aiRes.winner)
        setStatus(aiRes.winner ? `${aiRes.winner} wins!` : 'Draw!')
        return
      }

      setStatus('Your turn')
    } catch (e) {
      console.error(e)
      alert('Move failed. Try another column.')
      setStatus('Your turn')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="header">
        <h1>Connect 4</h1>
      </div>

      <div className="legend">
        <span><span className="swatch" style={{ background: '#ffeb3b' }} /> You</span>
        <span><span className="swatch" style={{ background: '#ff5252' }} /> AI</span>
      </div>

      <div className="status">{status}</div>

      <div className="controls">
        <button onClick={startNewGame} disabled={loading}>New Game</button>
      </div>

      {board && (
        <Board
          board={board}
          onColumnClick={onColumnClick}
          disabled={loading || gameOver}
        />
      )}
    </div>
  )
}

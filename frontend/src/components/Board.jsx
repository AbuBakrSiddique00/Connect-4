import React from 'react'

export default function Board({ board, onColumnClick, disabled }) {

  const displayRows = [...board].slice().reverse()

  return (
    <div className="board">
      <div className="grid">
        {displayRows.map((row, rIdx) =>
          row.map((cell, cIdx) => {
            const piece = cell === 1 ? 'player' : cell === 2 ? 'ai' : ''
            const key = `${rIdx}-${cIdx}`
            // For click target, we put a column overlay only on the top visual row
            const isTopVisualRow = rIdx === 0
            return (
              <div className="cell" key={key}>
                {isTopVisualRow ? (
                  <div
                    className="column-overlay"
                    role="button"
                    aria-label={`Drop in column ${cIdx + 1}`}
                    onClick={() => !disabled && onColumnClick(cIdx)}
                  >
                    <div className={`disc ${piece}`} />
                  </div>
                ) : (
                  <div className={`disc ${piece}`} />
                )}
              </div>
            )
          })
        )}
      </div>
    </div>
  )
}

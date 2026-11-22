// frontend/src/App.jsx
import { useState, useEffect, useRef } from 'react';
import './index.css';

const GRID_SIZE = 15;
const TICK_MS = 150;

//Helper to convert coordinates to a Map key.
const toKey = (x, y) => `${x},${y}`;

//Generate random food not currently on the snake.
const spawnFood = (snakeMap) => {
  while (true) {
    const x = Math.floor(Math.random() * GRID_SIZE);
    const y = Math.floor(Math.random() * GRID_SIZE);
    const key = toKey(x, y);
    if (!snakeMap.has(key)) return { x, y, key };
  }
};

//Initial 3-cell snake.
const createInitialSnake = () => {
  const map = new Map();
  map.set(toKey(5, 7), { x: 5, y: 7 }); // Tail
  map.set(toKey(6, 7), { x: 6, y: 7 });
  map.set(toKey(7, 7), { x: 7, y: 7 }); // Head
  return map;
};

export default function App() {
  //Grab the logged-in Django username from <div id="snake-root" data-username="...">.
  const loggedInUser =
    document.getElementById('snake-root')?.dataset.username || '';

  const [snake, setSnake] = useState(createInitialSnake);
  const [food, setFood] = useState(() => spawnFood(createInitialSnake()));
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  //Special variable to hold the logged-in user's score for export.
  const [exportedScore, setExportedScore] = useState(null);

  //Refs keep direction updates instant without waiting for React re-renders.
  const directionRef = useRef({ dx: 1, dy: 0 }); //Moving right initially.
  const headRef = useRef({ x: 7, y: 7 });

  //Arrow Key Controls.
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
        e.preventDefault(); // Stop page from scrolling
      }

      const { dx, dy } = directionRef.current;
      if (e.key === 'ArrowUp' && dy !== 1) directionRef.current = { dx: 0, dy: -1 };
      if (e.key === 'ArrowDown' && dy !== -1) directionRef.current = { dx: 0, dy: 1 };
      if (e.key === 'ArrowLeft' && dx !== 1) directionRef.current = { dx: -1, dy: 0 };
      if (e.key === 'ArrowRight' && dx !== -1) directionRef.current = { dx: 1, dy: 0 };
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  //Game Looooooooooop.
  useEffect(() => {
    if (gameOver) return;

    const interval = setInterval(() => {
      setSnake((prevSnake) => {
        const nextX = headRef.current.x + directionRef.current.dx;
        const nextY = headRef.current.y + directionRef.current.dy;
        const nextKey = toKey(nextX, nextY);

        //Wall collision check (out of range).
        const hitWall =
          nextX < 0 || nextX >= GRID_SIZE || nextY < 0 || nextY >= GRID_SIZE;

        //Body collision check (key already exists in Map).
        const hitBody = prevSnake.has(nextKey);

        if (hitWall || hitBody) {
          setGameOver(true);
          return prevSnake;
        }

        //Clone the Map so React detects the state update.
        const nextSnake = new Map(prevSnake);
        nextSnake.set(nextKey, { x: nextX, y: nextY });
        headRef.current = { x: nextX, y: nextY };

        //Food check: if eaten, keep the tail (grows by 1) and add score.
        if (nextKey === food.key) {
          setScore((s) => s + 10);
          setFood(spawnFood(nextSnake));
        } else {
          //Normal move: remove the oldest key (the tail).
          const tailKey = nextSnake.keys().next().value;
          nextSnake.delete(tailKey);
        }

        return nextSnake;
      });
    }, TICK_MS);

    return () => clearInterval(interval);
  }, [gameOver, food]);

  //Save / Export Score for Logged-In User on Game Over.
  useEffect(() => {
    if (gameOver && loggedInUser) {
      const scoreData = {
        username: loggedInUser,
        game: 'snake',
        score: score,
      };

      setExportedScore(scoreData);

      // Easy for your teammate to read or replace with a Django POST request later
      window.latestSnakeScore = scoreData;
      console.log('Ready to export to High Scores:', scoreData);
    }
  }, [gameOver, loggedInUser, score]);

  const resetGame = () => {
    const freshSnake = createInitialSnake();
    headRef.current = { x: 7, y: 7 };
    directionRef.current = { dx: 1, dy: 0 };
    setSnake(freshSnake);
    setFood(spawnFood(freshSnake));
    setScore(0);
    setGameOver(false);
    setExportedScore(null);
  };

  const headKey = toKey(headRef.current.x, headRef.current.y);

  return (
    <div className="snake-wrapper">
      <div className="snake-hud">
        <span>Score: {score}</span>
        {gameOver && <span className="game-over-text">GAME OVER</span>}
      </div>

      {/* Render the Map as an HTML Table */}
      <table className="snake-table">
        <tbody>
          {Array.from({ length: GRID_SIZE }).map((_, y) => (
            <tr key={y}>
              {Array.from({ length: GRID_SIZE }).map((_, x) => {
                const cellKey = toKey(x, y);
                let cellClass = 'cell';

                if (cellKey === headKey) cellClass += ' snake-head';
                else if (snake.has(cellKey)) cellClass += ' snake-body';
                else if (cellKey === food.key) cellClass += ' food';

                return <td key={cellKey} className={cellClass} />;
              })}
            </tr>
          ))}
        </tbody>
      </table>

      {gameOver && (
        <div className="game-over-panel">
          <button onClick={resetGame} className="restart-btn">
            Play Again
          </button>
          {exportedScore && (
            <p className="score-saved-msg">
              Saved score ({exportedScore.score}) for {exportedScore.username}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
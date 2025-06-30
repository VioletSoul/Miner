# Miner

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/VioletSoul/Miner)
![Repo Size](https://img.shields.io/github/repo-size/VioletSoul/Miner)
![Size](https://img.shields.io/github/languages/code-size/VioletSoul/Miner)
![Issues](https://img.shields.io/github/issues/VioletSoul/Miner)
![Stars](https://img.shields.io/github/stars/VioletSoul/Miner)
![Forks](https://img.shields.io/github/forks/VioletSoul/Miner)

## Description

**Miner** is a Python implementation of the classic "Minesweeper" game. The gameplay fully replicates the original Windows Minesweeper: mines are randomly placed on the board, and the player's goal is to open all safe cells without detonating a mine. The number in each cell shows how many mines are adjacent to it, allowing logical deduction of mine locations.

## How to play

- **Left mouse button** — open a cell.
- **Right mouse button** — place or remove a flag (mark a suspected mine).
- The goal: open all non-mine cells. If you open a mine — the game is over.
- The numbers in the cells show how many mines are in the neighboring cells (horizontally, vertically, and diagonally).

## Features

- Classic Minesweeper mechanics
- Random mine placement on the board
- Counting the number of mines around each cell
- Ability to place and remove flags
- The game ends with a win (all safe cells opened) or a loss (mine opened)
- All logic is implemented in a single file with no external dependencies

## Launch

1. Make sure you have Python 3 installed.
2. Download the `miner.py` file.
3. Run the game with:
```
python miner.py
```

## License

MIT

## Author

[VioletSoul](https://github.com/VioletSoul)

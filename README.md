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

**Miner** is a modern implementation of the classic Minesweeper game in Python, featuring a visual style adapted for Windows, macOS, and Linux. The gameplay faithfully reproduces the original Windows Minesweeper: mines are randomly placed on the board, and your goal is to open all safe cells without triggering a mine. The number on each cell indicates how many mines are adjacent to it, helping you logically deduce the locations of mines.

## How to Play

- **Left mouse button** — open a cell.
- **Right mouse button** — place or remove a flag (mark a suspected mine).
- **On Mac**: you can also use **Ctrl + left mouse button** to place or remove a flag.
- The goal is to open all cells without mines. If you open a mine, the game is over.
- Numbers on the cells show how many mines are adjacent (horizontally, vertically, and diagonally).

## Features

- Classic Minesweeper mechanics
- Modern, cross-platform appearance: opened and closed cells are always visually distinct, even on Mac
- Defeat visualization: when you lose, all mines are revealed, cells get a reddish tint, incorrect flags are marked with a cross, and the exploded cell is highlighted in bright red
- Readable interface: mine counter and timer are displayed in a dark font for better readability
- Random mine placement
- Automatic counting of adjacent mines
- Flag placement and removal
- Victory and defeat detection
- Single-file, dependency-free implementation

## Installation & Launch

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

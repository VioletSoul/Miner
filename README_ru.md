# Miner

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Last Commit](https://img.shields.io/github/last-commit/VioletSoul/Miner)
![Repo Size](https://img.shields.io/github/repo-size/VioletSoul/Miner)
![Size](https://img.shields.io/github/languages/code-size/VioletSoul/Miner)
![Issues](https://img.shields.io/github/issues/VioletSoul/Miner)
![Stars](https://img.shields.io/github/stars/VioletSoul/Miner)
![Forks](https://img.shields.io/github/forks/VioletSoul/Miner)

## Описание

**Miner** — это реализация классической игры "Сапёр" (Minesweeper) на Python. Игра полностью повторяет механику оригинального Windows-сапёра: на игровом поле случайным образом размещаются мины, а задача игрока — открыть все безопасные клетки, не подорвавшись на мине. Количество мин вокруг каждой клетки отображается числом, что позволяет логически вычислять расположение мин.

## Как играть

- **Левая кнопка мыши** — открыть клетку.
- **Правая кнопка мыши** — поставить или убрать флаг (отметить предполагаемую мину).
- Цель игры: открыть все клетки без мин. Если вы открыли мину — игра окончена.
- Числа на клетках показывают, сколько мин находится в соседних клетках по горизонтали, вертикали и диагонали.

## Особенности

- Классическая механика "Сапёра"
- Случайная генерация мин на поле
- Подсчёт количества мин вокруг каждой клетки
- Возможность ставить и убирать флаги
- Игра завершается победой (все безопасные клетки открыты) или поражением (открыта мина)
- Вся логика реализована в одном файле без сторонних зависимостей

## Запуск

1. Убедитесь, что у вас установлен Python 3.
2. Скачайте файл `miner.py`.
3. Запустите игру командой:
```
python miner.py
```
## Лицензия

MIT

## Автор

[VioletSoul](https://github.com/VioletSoul)
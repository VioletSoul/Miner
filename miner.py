import tkinter as tk
import random
import time

class StartDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Параметры игры")
        self.resizable(False, False)  # Запрет изменения размера окна
        tk.Label(self, text="Размер поля (минимум 5):").grid(row=0, column=0, sticky="w")
        tk.Label(self, text="Количество мин:").grid(row=1, column=0, sticky="w")
        self.size_var = tk.IntVar(value=9)
        self.mines_var = tk.IntVar(value=10)
        tk.Entry(self, textvariable=self.size_var, width=5).grid(row=0, column=1)
        tk.Entry(self, textvariable=self.mines_var, width=5).grid(row=1, column=1)
        tk.Button(self, text="Начать игру", command=self.ok).grid(row=2, column=0, columnspan=2, pady=5)
        self.result = None

    def ok(self):
        size = max(5, self.size_var.get())
        mines = max(1, self.mines_var.get())
        if mines >= size * size:
            mines = size * size - 1
        self.result = (size, mines)
        self.destroy()

class Cell:
    colors = {
        1: 'blue',
        2: 'green',
        3: 'red',
        4: 'darkblue',
        5: 'brown',
        6: 'cyan',
        7: 'black',
        8: 'gray'
    }

    def __init__(self, master, x, y, callback):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_open = False
        self.is_flag = False
        self.button = tk.Button(master, width=2, height=1, font=('Arial', 14),
                                command=self.open_cell)
        self.button.bind('<Button-3>', self.toggle_flag)  # Правая кнопка мыши
        self.button.bind('<Control-Button-1>', self.toggle_flag)  # Control+левый клик (Mac)
        self.callback = callback

    def open_cell(self):
        if self.is_open or self.is_flag:
            return
        self.is_open = True
        self.button.config(relief=tk.SUNKEN)
        self.callback(self)

    def toggle_flag(self, event):
        if self.is_open:
            return
        self.is_flag = not self.is_flag
        self.button.config(text='🚩' if self.is_flag else '')

    def show_mine(self):
        self.button.config(text='💣', bg='red')

    def show_number(self, n):
        if n > 0:
            color = self.colors.get(n, 'black')
            self.button.config(text=str(n), disabledforeground=color)
        self.button.config(state=tk.DISABLED)

    def disable(self):
        self.button.config(state=tk.DISABLED)

    def reset(self):
        self.is_mine = False
        self.is_open = False
        self.is_flag = False
        self.button.config(text='', bg='SystemButtonFace', relief=tk.RAISED, state=tk.NORMAL)

class Minesweeper:
    def __init__(self, root, size, mines):
        self.root = root
        self.size = size
        self.mines_count = mines
        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=0, sticky='nw')
        self.cells = []
        self.mines = set()
        self.game_over = False
        self.start_time = None
        self.timer_id = None

        self.create_widgets()
        self.place_mines()
        self.counts = self.calculate_counts()
        self.start_timer()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.resizable(False, False)  # Запрет изменения размера главного окна

    def create_widgets(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = Cell(self.frame, i, j, self.cell_callback)
                cell.button.grid(row=i, column=j)
                row.append(cell)
            self.cells.append(row)
        # Надписи и кнопка — сверху, слева
        self.status = tk.Label(self.root, text="Игра началась!", font=("Arial", 13))
        self.status.grid(row=0, column=0, sticky='w', padx=5, pady=(5,0))
        self.timer_label = tk.Label(self.root, text="Время: 0", font=("Arial", 13))
        self.timer_label.grid(row=0, column=1, sticky='w', padx=5, pady=(5,0))
        self.new_game_btn = tk.Button(self.root, text="Новая игра", font=("Arial", 12), command=self.new_game_dialog)
        self.new_game_btn.grid(row=0, column=2, sticky='w', padx=5, pady=(5,0))

    def place_mines(self):
        self.mines = set()
        positions = random.sample(range(self.size * self.size), self.mines_count)
        for pos in positions:
            x, y = divmod(pos, self.size)
            self.cells[x][y].is_mine = True
            self.mines.add((x, y))

    def calculate_counts(self):
        counts = [[0]*self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j].is_mine:
                    continue
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = i+dx, j+dy
                        if 0 <= ni < self.size and 0 <= nj < self.size:
                            if self.cells[ni][nj].is_mine:
                                counts[i][j] += 1
        return counts

    def cell_callback(self, cell):
        if self.game_over:
            return
        if cell.is_mine:
            cell.show_mine()
            self.end_game(False)
        else:
            n = self.counts[cell.x][cell.y]
            cell.show_number(n)
            if n == 0:
                self.open_neighbors(cell.x, cell.y)
            if self.check_win():
                self.end_game(True)

    def open_neighbors(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    neighbor = self.cells[nx][ny]
                    if not neighbor.is_open and not neighbor.is_mine and not neighbor.is_flag:
                        neighbor.open_cell()

    def end_game(self, win):
        self.game_over = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        for i in range(self.size):
            for j in range(self.size):
                cell = self.cells[i][j]
                if cell.is_mine:
                    cell.show_mine()
                cell.disable()
        if win:
            self.status.config(text="Поздравляем! Вы выиграли!")
        else:
            self.status.config(text="Игра окончена! Вы проиграли.")

    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                cell = self.cells[i][j]
                if not cell.is_mine and not cell.is_open:
                    return False
        return True

    def new_game_dialog(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.frame.destroy()
        self.status.destroy()
        self.timer_label.destroy()
        self.new_game_btn.destroy()
        dialog = StartDialog(self.root)
        self.root.wait_window(dialog)
        if dialog.result:
            size, mines = dialog.result
            Minesweeper(self.root, size, mines)

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.game_over or not self.timer_label.winfo_exists():
            return
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Время: {elapsed}")
        self.timer_id = self.root.after(1000, self.update_timer)

    def on_close(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Сапёр")
    root.resizable(False, False)  # Запрет изменения размера главного окна
    dialog = StartDialog(root)
    root.wait_window(dialog)
    if dialog.result:
        size, mines = dialog.result
        Minesweeper(root, size, mines)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import random
import time

CELL_SIZE = 32
FONT = ("Segoe UI", 13, "bold")
BG_COLOR = "#e0e0e0"
BTN_COLOR = "#bdbdbd"
FLAG_COLOR = "#ff4444"
MINE_COLOR = "#222"
OPEN_COLOR = "#f5f5f5"
NUMBER_COLORS = {
    1: "#1976d2", 2: "#388e3c", 3: "#d32f2f", 4: "#7b1fa2",
    5: "#ff8f00", 6: "#00838f", 7: "#c2185b", 8: "#455a64"
}

DIFFICULTIES = {
    "Новичок": (9, 9, 10),
    "Любитель": (16, 16, 40),
    "Эксперт": (30, 16, 99)
}

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.is_mine = False
        self.is_open = False
        self.is_flag = False
        self.adjacent = 0

class Minesweeper(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Сапёр")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_menu()
        self.setup_game("Новичок")

    def create_menu(self):
        menubar = tk.Menu(self)
        game_menu = tk.Menu(menubar, tearoff=0)
        for diff in DIFFICULTIES:
            game_menu.add_command(label=diff, command=lambda d=diff: self.setup_game(d))
        game_menu.add_separator()
        game_menu.add_command(label="Выход", command=self.on_close)
        menubar.add_cascade(label="Игра", menu=game_menu)
        self.config(menu=menubar)

    def setup_game(self, difficulty):
        self.difficulty = difficulty
        self.width, self.height, self.mines = DIFFICULTIES[difficulty]
        self.first_click = True
        self.start_time = None
        self.timer_id = None
        self.flag_count = self.mines
        self.game_over = False

        for widget in self.winfo_children():
            widget.destroy()

        # Верхняя панель
        top = tk.Frame(self, bg=BG_COLOR)
        top.pack(fill="x")
        self.mine_label = tk.Label(top, text=f"💣 {self.flag_count}", font=FONT, bg=BG_COLOR)
        self.mine_label.pack(side="left", padx=10, pady=5)
        self.restart_btn = tk.Button(top, text="😃", font=("Segoe UI", 16), width=2,
                                     command=lambda: self.setup_game(self.difficulty))
        self.restart_btn.pack(side="left", padx=10)
        self.timer_label = tk.Label(top, text="⏱ 0", font=FONT, bg=BG_COLOR)
        self.timer_label.pack(side="right", padx=10, pady=5)

        # Игровое поле
        self.board = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        self.buttons = [[None for _ in range(self.width)] for _ in range(self.height)]
        field = tk.Frame(self, bg=BG_COLOR)
        field.pack()

        for y in range(self.height):
            field.grid_rowconfigure(y, minsize=CELL_SIZE)
            for x in range(self.width):
                field.grid_columnconfigure(x, minsize=CELL_SIZE)
                btn = tk.Button(field, width=2, height=1, font=FONT, bg=BTN_COLOR,
                                relief="raised", command=lambda x=x, y=y: self.on_left_click(x, y))
                btn.bind("<Button-3>", lambda e, x=x, y=y: self.on_right_click(x, y))
                btn.grid(row=y, column=x, padx=0, pady=0, sticky="nsew")
                self.buttons[y][x] = btn

        # Автоматически подгоняем размер окна под поле и панель
        self.update_idletasks()
        total_width = field.winfo_reqwidth()
        total_height = top.winfo_reqheight() + field.winfo_reqheight()
        self.minsize(total_width, total_height)
        self.geometry(f"{total_width}x{total_height}")

    def on_left_click(self, x, y):
        if self.game_over or self.board[y][x].is_flag:
            return
        if self.first_click:
            self.place_mines(x, y)
            self.start_time = time.time()
            self.update_timer()
            self.first_click = False
        self.reveal_cell(x, y)
        self.update_buttons()
        self.check_win()

    def on_right_click(self, x, y):
        if self.game_over or self.board[y][x].is_open:
            return
        cell = self.board[y][x]
        btn = self.buttons[y][x]
        if not cell.is_flag and self.flag_count == 0:
            return
        cell.is_flag = not cell.is_flag
        if cell.is_flag:
            btn.config(text="🚩", fg=FLAG_COLOR, relief="raised")
            self.flag_count -= 1
        else:
            btn.config(text="", fg="black", relief="raised")
            self.flag_count += 1
        self.mine_label.config(text=f"💣 {self.flag_count}")

    def place_mines(self, safe_x, safe_y):
        positions = [(x, y) for y in range(self.height) for x in range(self.width)
                     if abs(x-safe_x) > 1 or abs(y-safe_y) > 1]
        random.shuffle(positions)
        for i in range(self.mines):
            x, y = positions[i]
            self.board[y][x].is_mine = True
        for y in range(self.height):
            for x in range(self.width):
                if not self.board[y][x].is_mine:
                    self.board[y][x].adjacent = self.count_adjacent(x, y)

    def count_adjacent(self, x, y):
        cnt = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.board[ny][nx].is_mine:
                        cnt += 1
        return cnt

    def reveal_cell(self, x, y):
        cell = self.board[y][x]
        btn = self.buttons[y][x]
        if cell.is_open or cell.is_flag:
            return
        cell.is_open = True
        btn.config(relief="sunken", bg=OPEN_COLOR)
        if cell.is_mine:
            btn.config(text="💣", bg=MINE_COLOR, fg="white")
            self.lose_game(x, y)
            return
        if cell.adjacent > 0:
            btn.config(text=str(cell.adjacent), fg=NUMBER_COLORS[cell.adjacent])
        else:
            btn.config(text="")
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x+dx, y+dy
                    if (dx != 0 or dy != 0) and 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal_cell(nx, ny)

    def update_buttons(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                btn = self.buttons[y][x]
                if cell.is_open:
                    btn.config(relief="sunken", bg=OPEN_COLOR)
                    if cell.is_mine:
                        btn.config(text="💣", bg=MINE_COLOR, fg="white")
                    elif cell.adjacent > 0:
                        btn.config(text=str(cell.adjacent), fg=NUMBER_COLORS[cell.adjacent])
                    else:
                        btn.config(text="")
                elif cell.is_flag:
                    btn.config(text="🚩", fg=FLAG_COLOR, relief="raised")
                else:
                    btn.config(text="", fg="black", bg=BTN_COLOR, relief="raised")

    def lose_game(self, x, y):
        self.game_over = True
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
        for row in self.board:
            for cell in row:
                btn = self.buttons[cell.y][cell.x]
                if cell.is_mine:
                    btn.config(text="💣", bg=MINE_COLOR, fg="white")
                elif cell.is_flag and not cell.is_mine:
                    btn.config(text="❌", fg="red")
        self.buttons[y][x].config(bg="#ff4444")
        self.restart_btn.config(text="😵")
        messagebox.showinfo("Поражение", "Вы подорвались на мине!")

    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine and not cell.is_open:
                    return
        self.game_over = True
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
        for row in self.board:
            for cell in row:
                btn = self.buttons[cell.y][cell.x]
                if cell.is_mine:
                    btn.config(text="🚩", fg=FLAG_COLOR)
        self.restart_btn.config(text="😎")
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        messagebox.showinfo("Победа", f"Вы выиграли! Время: {elapsed} сек.")

    def update_timer(self):
        if self.game_over or self.first_click:
            return
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"⏱ {elapsed}")
        self.timer_id = self.after(1000, self.update_timer)

    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    Minesweeper().mainloop()

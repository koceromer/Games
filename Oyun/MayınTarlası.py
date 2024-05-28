import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper(tk.Tk):
    def __init__(self, size=15, mines=10):
        super().__init__()
        self.title('Mayın Tarlası')
        self.size = size
        self.mines = mines
        self.buttons = {}
        self.mines_positions = set()
        self.first_click = True
        self.hint_used = False
        self.create_widgets()

    def create_widgets(self):
        for row in range(self.size):
            for col in range(self.size):
                button = tk.Button(self, width=2, height=1, font=('Arial', 12), command=lambda r=row, c=col: self.click(r, c), bg='#d9d9d9', fg='black')
                button.bind("<Button-3>", lambda e, r=row, c=col: self.right_click(r, c))
                button.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[(row, col)] = button
        
        self.reset_button = tk.Button(self, text='Yeniden Başlat', command=self.reset, font=('Arial', 14), bg='white', fg='black')
        self.reset_button.grid(row=self.size, column=0, columnspan=self.size//2, sticky="we")

        self.menu_button = tk.Button(self, text='Menüye Dön', command=self.return_to_menu, font=('Arial', 14), bg='white', fg='black')
        self.menu_button.grid(row=self.size, column=self.size//2, columnspan=self.size//2, sticky="we")
        
        self.hint_button = tk.Button(self, text='💡 İpucu', command=self.use_hint, font=('Arial', 14), bg='yellow', fg='black')
        self.hint_button.grid(row=self.size+1, column=0, columnspan=self.size, sticky="we")

    def place_mines(self, start_row, start_col):
        self.mines_positions = set(random.sample(self.buttons.keys(), self.mines))
        safe_zone = {(start_row + r, start_col + c) for r in range(-1, 2) for c in range(-1, 2)}
        self.mines_positions.difference_update(safe_zone)
        additional_mines = self.mines - len(self.mines_positions)
        while additional_mines > 0:
            new_mine = random.choice(list(self.buttons.keys()))
            if new_mine not in self.mines_positions and new_mine not in safe_zone:
                self.mines_positions.add(new_mine)
                additional_mines -= 1

        self.counts = {pos: 0 for pos in self.buttons}
        for (row, col) in self.mines_positions:
            self.counts[(row, col)] = -1
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if (r, c) in self.counts and self.counts[(r, c)] != -1:
                        self.counts[(r, c)] += 1

    def update_counts(self):
        for (row, col) in self.buttons:
            if self.counts[(row, col)] == -1:
                continue
            self.buttons[(row, col)].config(text='', state='normal', relief=tk.RAISED, bg='#d9d9d9', fg='black')

    def click(self, row, col):
        if self.first_click:
            self.place_mines(row, col)
            self.update_counts()
            self.first_click = False
            self.reveal(row, col, True)
        else:
            if (row, col) in self.mines_positions:
                self.game_over(False)
                return
            self.reveal(row, col, False)
            if self.check_win():
                self.game_over(True)

    def right_click(self, row, col):
        current_text = self.buttons[(row, col)].cget('text')
        if current_text == '':
            self.buttons[(row, col)].config(text='F', fg='red', bg='white')
        elif current_text == 'F':
            self.buttons[(row, col)].config(text='?', fg='orange', bg='white')
        elif current_text == '?':
            self.buttons[(row, col)].config(text='', bg='#d9d9d9')

    def reveal(self, row, col, is_first_click):
        if self.buttons[(row, col)].cget('text') in ['F', '?']:
            return
        self.buttons[(row, col)].config(text=self.counts[(row, col)] if self.counts[(row, col)] != 0 else '', state='disabled', relief=tk.SUNKEN, bg='white')
        if is_first_click:
            self.reveal_neighbors(row, col)
        elif self.counts[(row, col)] == 0:
            self.reveal_neighbors(row, col)

    def reveal_neighbors(self, row, col):
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if (r, c) in self.buttons and self.buttons[(r, c)].cget('state') == 'normal':
                    self.reveal(r, c, False)

    def use_hint(self):
        if not self.hint_used:
            self.hint_used = True
            if self.mines_positions:
                mine = random.choice(list(self.mines_positions))
                self.buttons[mine].config(bg='yellow')
                self.hint_button.config(state='disabled')

    def game_over(self, won):
        for (row, col) in self.buttons:
            if (row, col) in self.mines_positions:
                self.buttons[(row, col)].config(text='M', fg='black', bg='red')
            self.buttons[(row, col)].config(state='disabled')
        if won:
            messagebox.showinfo("Oyun Bitti", "Kazandınız! Tebrikler!")
        else:
            messagebox.showinfo("Oyun Bitti", "Kaybettiniz! Tekrar Deneyin!")
        self.reset_button.config(text='Yeniden Başlat')

    def check_win(self):
        for (row, col) in self.buttons:
            if self.counts[(row, col)] != -1 and self.buttons[(row, col)].cget('state') == 'normal':
                return False
        return True

    def reset(self):
        self.first_click = True
        self.hint_used = False
        for button in self.buttons.values():
            button.config(text='', state='normal', relief=tk.RAISED, bg='#d9d9d9', fg='black')
        self.reset_button.config(text='Yeniden Başlat')
        self.hint_button.config(state='normal', bg='yellow')
        self.mines_positions = set()

    def return_to_menu(self):
        self.destroy()
        start_menu = StartMenu()
        start_menu.mainloop()

class StartMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Mayın Tarlası - Başlangıç Menüsü')
        self.geometry('400x500')
        self.configure(bg='#add8e6')
        
        tk.Label(self, text='Mayın Tarlası', font=('Arial', 24, 'bold'), bg='#add8e6').pack(pady=20)
        
        tk.Label(self, text='Boyut Seçin:', font=('Arial', 14), bg='#add8e6').pack()
        self.size_var = tk.IntVar(value=15)
        tk.Radiobutton(self, text='Küçük (15x15)', variable=self.size_var, value=15, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        tk.Radiobutton(self, text='Orta (25x25)', variable=self.size_var, value=25, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        tk.Radiobutton(self, text='Büyük (40x40)', variable=self.size_var, value=40, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        
        tk.Label(self, text='Zorluk Seçin:', font=('Arial', 14), bg='#add8e6').pack()
        self.difficulty_var = tk.IntVar(value=10)
        tk.Radiobutton(self, text='Kolay', variable=self.difficulty_var, value=10, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        tk.Radiobutton(self, text='Orta', variable=self.difficulty_var, value=20, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        tk.Radiobutton(self, text='Zor', variable=self.difficulty_var, value=25, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        
        tk.Button(self, text='Başlat', command=self.start_game, font=('Arial', 14), bg='white', fg='black').pack(pady=20)

    def start_game(self):
        size = self.size_var.get()
        difficulty = self.difficulty_var.get()
        if size == 15:
            mines = difficulty
        elif size == 25:
            mines = difficulty * 2
        elif size == 40:
            mines = difficulty * 4
        self.destroy()
        game = Minesweeper(size=size, mines=mines)
        game.mainloop()

if __name__ == '__main__':
    start_menu = StartMenu()
    start_menu.mainloop()

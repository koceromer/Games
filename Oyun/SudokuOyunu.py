import tkinter as tk
from tkinter import messagebox
import random

class Sudoku(tk.Tk):
    def __init__(self, difficulty=40):
        super().__init__()
        self.title('Sudoku')
        self.geometry('550x650')
        self.cells = {}
        self.difficulty = difficulty
        self.create_board()
        self.generate_puzzle()
        
    def create_board(self):
        self.board_frame = tk.Frame(self)
        self.board_frame.pack()

        self.canvas = tk.Canvas(self.board_frame, width=550, height=550)
        self.canvas.grid(row=0, column=0, columnspan=9, rowspan=9)
        self.create_grid_lines()

        for row in range(9):
            for col in range(9):
                if (row // 3 + col // 3) % 2 == 0:
                    bg_color = '#ffffff'
                else:
                    bg_color = '#f0f0f0'
                cell = tk.Entry(self.board_frame, width=3, font=('Arial', 18), justify='center', bg=bg_color, relief='ridge')
                cell.grid(row=row, column=col, padx=1, pady=1)
                self.cells[(row, col)] = cell

        self.check_button = tk.Button(self, text='Çözümü Kontrol Et', command=self.check_solution, font=('Arial', 14), bg='lightblue', fg='black')
        self.check_button.pack(pady=10)
        
        self.reset_button = tk.Button(self, text='Yeni Oyun', command=self.reset_board, font=('Arial', 14), bg='lightblue', fg='black')
        self.reset_button.pack(pady=10)

        self.menu_button = tk.Button(self, text='Menüye Dön', command=self.return_to_menu, font=('Arial', 14), bg='lightblue', fg='black')
        self.menu_button.pack(pady=10)

    def create_grid_lines(self):
        for i in range(10):
            width = 2 if i % 3 == 0 else 1
            self.canvas.create_line(0, i * 60, 540, i * 60, fill='black', width=width)
            self.canvas.create_line(i * 60, 0, i * 60, 540, fill='black', width=width)

    def generate_puzzle(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_puzzle()
        self.remove_numbers_from_board()
        self.display_board()

    def solve_puzzle(self):
        empty = self.find_empty_cell()
        if not empty:
            return True
        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                if self.solve_puzzle():
                    return True
                self.board[row][col] = 0
        return False

    def find_empty_cell(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return (row, col)
        return None

    def is_valid_move(self, row, col, num):
        if num in self.board[row]:
            return False
        if num in [self.board[i][col] for i in range(9)]:
            return False
        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[box_start_row + i][box_start_col + j] == num:
                    return False
        return True

    def remove_numbers_from_board(self):
        for _ in range(self.difficulty):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0

    def display_board(self):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].config(state='normal')
                self.cells[(row, col)].delete(0, 'end')
                if self.board[row][col] != 0:
                    self.cells[(row, col)].insert(0, self.board[row][col])
                    self.cells[(row, col)].config(state='disabled', disabledforeground='black')
                else:
                    self.cells[(row, col)].config(state='normal', fg='blue')

    def check_solution(self):
        for row in range(9):
            for col in range(9):
                if self.cells[(row, col)].get() == '':
                    messagebox.showwarning('Geçersiz Çözüm', 'Tüm hücreler doldurulmamış.')
                    return
                if not self.cells[(row, col)].get().isdigit() or int(self.cells[(row, col)].get()) not in range(1, 10):
                    messagebox.showwarning('Geçersiz Giriş', 'Hücrelerde geçersiz sayı var.')
                    return
                if not self.is_valid_move(row, col, int(self.cells[(row, col)].get())):
                    messagebox.showwarning('Yanlış Çözüm', 'Çözüm yanlış.')
                    return
        messagebox.showinfo('Doğru Çözüm', 'Tebrikler! Çözüm doğru.')

    def reset_board(self):
        self.generate_puzzle()

    def return_to_menu(self):
        self.destroy()
        start_menu = StartMenu()
        start_menu.mainloop()

class StartMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sudoku - Başlangıç Menüsü')
        self.geometry('400x400')
        self.configure(bg='#add8e6')
        
        tk.Label(self, text='Sudoku', font=('Arial', 24, 'bold'), bg='#add8e6').pack(pady=20)
        
        tk.Label(self, text='Zorluk Seçin:', font=('Arial', 14), bg='#add8e6').pack()
        self.difficulty_var = tk.IntVar(value=40)
        tk.Radiobutton(self, text='Kolay', variable=self.difficulty_var, value=40, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        tk.Radiobutton(self, text='Orta', variable=self.difficulty_var, value=50, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        tk.Radiobutton(self, text='Zor', variable=self.difficulty_var, value=60, font=('Arial', 12), bg='#add8e6').pack(anchor='w')
        
        tk.Button(self, text='Başlat', command=self.start_game, font=('Arial', 14), bg='white', fg='black').pack(pady=20)

    def start_game(self):
        difficulty = self.difficulty_var.get()
        self.destroy()
        game = Sudoku(difficulty=difficulty)
        game.mainloop()

if __name__ == '__main__':
    start_menu = StartMenu()
    start_menu.mainloop()

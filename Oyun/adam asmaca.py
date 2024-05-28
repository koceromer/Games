import tkinter as tk
import random

# Kelime listesi
word_list = ['python', 'java', 'kotlin', 'javascript', 'hangman', 'programming', 'development', 'algorithm']

def get_word():
    return random.choice(word_list)

def display_hangman(tries):
    stages = [
        '''
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        ---------
        ''',
        '''
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        ---------
        ''',
        '''
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        ---------
        ''',
        '''
           -----
           |   |
           O   |
          /|   |
               |
               |
        ---------
        ''',
        '''
           -----
           |   |
           O   |
           |   |
               |
               |
        ---------
        ''',
        '''
           -----
           |   |
           O   |
               |
               |
               |
        ---------
        ''',
        '''
           -----
           |   |
               |
               |
               |
               |
        ---------
        '''
    ]
    return stages[tries]

def update_display():
    word_display = ' '.join([letter if letter in guessed_letters else '_' for letter in word])
    display_label.config(text=word_display)
    tries_label.config(text=f'Kalan tahmin hakkınız: {tries}')
    guessed_label.config(text=f'Tahmin edilen harfler: {" ".join(sorted(guessed_letters))}')
    hangman_label.config(text=display_hangman(tries))

def guess_letter():
    global tries
    guess = entry.get().lower()
    entry.delete(0, tk.END)
    
    if len(guess) != 1 or not guess.isalpha():
        result_label.config(text='Lütfen geçerli bir harf girin.')
        return
    
    if guess in guessed_letters:
        result_label.config(text='Bu harfi zaten tahmin ettiniz.')
    elif guess in word:
        guessed_letters.add(guess)
        result_label.config(text='Doğru tahmin!')
    else:
        guessed_letters.add(guess)
        tries -= 1
        result_label.config(text='Yanlış tahmin!')

    update_display()

    if '_' not in [letter if letter in guessed_letters else '_' for letter in word]:
        result_label.config(text='Tebrikler! Kelimeyi buldunuz: ' + word)
        guess_button.config(state='disabled')
    elif tries == 0:
        result_label.config(text='Kaybettiniz! Kelime: ' + word)
        guess_button.config(state='disabled')

def restart_game():
    global word, guessed_letters, tries
    word = get_word()
    guessed_letters = set()
    tries = 6
    result_label.config(text='')
    guess_button.config(state='normal')
    update_display()

# Initialize the game
word = get_word()
guessed_letters = set()
tries = 6

# Create the main window
root = tk.Tk()
root.title('Adam Asmaca Oyunu')

# Create the widgets
display_label = tk.Label(root, text='', font=('Courier', 24, 'bold'))
tries_label = tk.Label(root, text='', font=('Courier', 14))
guessed_label = tk.Label(root, text='', font=('Courier', 14))
hangman_label = tk.Label(root, text='', font=('Courier', 14))
entry = tk.Entry(root, font=('Courier', 14))
guess_button = tk.Button(root, text='Tahmin Et', command=guess_letter, font=('Courier', 14))
result_label = tk.Label(root, text='', font=('Courier', 14))
restart_button = tk.Button(root, text='Yeniden Başlat', command=restart_game, font=('Courier', 14))

# Place the widgets
display_label.pack(pady=20)
tries_label.pack()
guessed_label.pack()
hangman_label.pack(pady=20)
entry.pack(pady=10)
guess_button.pack(pady=10)
result_label.pack(pady=10)
restart_button.pack(pady=20)

# Initial display update
update_display()

# Start the main loop
root.mainloop()

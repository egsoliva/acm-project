from rich.console import Console
from rich.prompt import Prompt
from random import choice

console = Console()

class Wordle:
    def __init__(self):
        self._is_game_over: bool = False
        self._tries: int = 5
        self._word_bank: list[str] = self.generate_word_bank()
        self._word: str = choice(self._word_bank)

        self._board = [["     " for _ in range(5)] for _ in range(5)]

    def generate_word_bank(self):
        arr: list[str] = []
        with open("words.txt", "r") as words:
            for word in words:
                word = word.strip().upper()
                if len(word) == 5:
                    arr.append(word)
        return arr

    def display_board(self):
        for row in self._board:
            for cell in row:
                console.print(cell, end="")
            console.print()

    def get_guess(self) -> str:
        while True:
            guess = Prompt.ask("[green3]Enter guess").upper()
            if len(guess) == 5:
                return guess
            console.print("[red]Invalid word. Try again.")

    def check_word(self, guess: str, row: int):
        word = self._word

        for i in range(5):
            if guess[i] == word[i]:
                self._board[row][i] = f"[white on green3] {guess[i]} "
            elif guess[i] in word:
                self._board[row][i] = f"[white on gold3] {guess[i]} "
            else:
                self._board[row][i] = f"[white on bright_black] {guess[i]} "

    def run(self):
        console.print("[bold cyan]Welcome to Wordle!")

        for attempt in range(self._tries):
            self.display_board()
            guess = self.get_guess()

            self.check_word(guess, attempt)

            if guess == self._word:
                self.display_board()
                console.print("[bold green]You win!")
                return

        self.display_board()
        console.print(f"[bold red]Game over! The word was {self._word}")
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

class View:
        
    def display_main_menu(self):
        ...

class WordleView:
    def get_guess(self) -> str:
        len_guess: int = 0
        guess:str = ""

        while len_guess != 5:
            guess = Prompt.ask("[green3]Enter guess").upper()
            len_guess: int = len(guess)
        
        return guess

    def display_board(self, board: list[str]):
        for i in board:
            ...

    def play_again(self) -> bool:
        response = Prompt.ask("[green3]Would you like to play again?").upper()
        
        return True if response == "Y" else False
    
    def display_outcome(self, guess: str, word: str):
        for i in range(5):
            if guess[i] == word[i]:
                Console.print(f"[white on green3]{guess[i]}", end="")
            elif guess[i] != word[i] and guess[i] in word:
                Console.print(f"[white on gold3]{guess[i]}", end="")
            elif guess[i] not in word:
                Console.print(f"[white on bright_black]{guess[i]}", end="")
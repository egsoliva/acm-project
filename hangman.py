from collections.abc import Sequence
from random import randint
import os
from time import sleep


DELAY = 0.8

'''
To Do:
+ Add word bank
'''

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Hangman:
    def __init__(self) -> None:
        self.set_game()


    def set_game(self) -> None:
        self.word: str = self.pick_word()
        self.guesses: list[str] = ['_' for _ in range(len(self.word))] # to be displayed as game goes on
        self.deconstructed_word: dict[str, list[int]] = {letter: [] for letter in self.word}
        
        for i in range(len(self.word)):
            self.deconstructed_word[self.word[i]].append(i)

        self.attempts_left: int = 7
        self.letters_found: int = 0

        self.guesses_made: set[str] = set()


    def pick_word(self) -> str:
        arr: list[str] = []
        with open("words.txt", "r") as words:
            for word in words:
                word = word.strip().upper()
                arr.append(word)

        return arr[randint(0, len(arr) - 1)]


    def make_guess(self, guess: str) -> bool:
        if len(guess) != 1:
            raise ValueError

        if guess in self.guesses_made:
            raise IndexError

        self.guesses_made.add(guess)

        if guess in self.deconstructed_word:
            for index in self.deconstructed_word[guess]:
                self.guesses[index] = guess.upper()
                self.letters_found += 1

            return True

        return False


    @property
    def is_game_over(self) -> bool:
        return self.letters_found == len(self.word) or self.attempts_left == 0

    @property
    def is_game_won(self) -> bool:
        return self.letters_found == len(self.word)


    def hangman_display(self) -> None:
        if self.is_game_won:
            return f"""
  |
  |
  |
  |         O
 _|_       /T\\
/   \\      / \\
"""

        match self.attempts_left:
            case 7:
                return f"""

  |
  |                    
  |
  |
 _|_
/   \\
"""
            case 6:
                return f"""
   ____
  |    |
  |    
  |
  |
 _|_
/   \\
"""
            case 5:
                return f"""
   ____
  |    |
  |    O
  |
  |
 _|_
/   \\
"""
            case 4: 
                return f"""
   ____
  |    |
  |    O
  |    T
  |
 _|_
/   \\
"""
            case 3:
                return f"""
   ____
  |    |
  |    O
  |   /T
  |
 _|_
/   \\
"""
            case 2:
                return f"""
   ____
  |    |
  |    O
  |   /T\\
  |
 _|_
/   \\
"""

            case 1:
                return f"""
   ____
  |    |
  |    O
  |   /T\\
  |   /
 _|_
/   \\
"""
            case 0: 
                return f"""
   ____
  |    |
  |    O
  |   /T\\
  |   / \\
 _|_
/   \\
"""


    def guesses_display(self) -> None:
        return " ".join(self.guesses)


    def play(self) -> bool: # returns True or False if game was won
        self.set_game()

        while not self.is_game_over:
            clear_screen()
            print(self.hangman_display())
            print(self.guesses_display())
            print(f"Guesses Left: {self.attempts_left}")

            guess: str = input("Make Your Guess: ").upper()
            
            try:
                if not self.make_guess(guess):

                    self.attempts_left -= 1
                    print(f"There is 0 {guess}'s in the word!")
                    sleep(DELAY)
                else:
                    print(f"There are {len(self.deconstructed_word[guess])} {guess}'s in the word!" if len(self.deconstructed_word[guess]) > 1 else f"There is 1 {guess} in the word!")
                    sleep(DELAY)

            except ValueError:
                print(f"Please only enter single characters!")
                sleep(DELAY)
                continue

            except IndexError:
                print(f"You have already guessed {guess}")
                sleep(DELAY)
                continue


        print(f"Game Over. The word was {self.word.upper()}" if not self.is_game_won else f"You Won! The word is {self.word.upper()}!")
        print(self.hangman_display())
        while True:
            replay: str = input("Play Again? (y/n) ")
            if replay.lower() not in "yn":
                print("Please select y or n")
                sleep(DELAY)
                continue
            else:
                break

        if replay == 'y':
            self.play()

        else:
            return


if __name__ == '__main__':
    game: Hangman = Hangman()
    game.play()
import os
from time import sleep
from random import choice

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from blackjack import Blackjack
from hangman import Hangman
from wordle import Wordle

console = Console()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# =========================
# 🎮 STYLE / VISUALS
# =========================

FLAVOR_TEXTS = [
    "Luck favors the bold.",
    "Will you beat the house?",
    "Welcome, legend...",
    "Every guess matters.",
    "Fortune or failure?",
    "Choose your challenge.",
]

def show_title():
    title = Text("""
 █████╗ ██████╗  ██████╗ █████╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝
███████║██████╔╝██║     ███████║██║  ██║█████╗  
██╔══██║██╔══██╗██║     ██╔══██║██║  ██║██╔══╝  
██║  ██║██║  ██║╚██████╗██║  ██║██████║ ███████╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝  ╚═════╝
""", style="bold cyan")

    console.print(Align.center(title))
    console.print(Align.center("[bold magenta]🎮 Arcade Hub[/bold magenta]\n"))
    console.print(Align.center(f"[italic dim]{choice(FLAVOR_TEXTS)}[/italic dim]\n"))

def show_menu(coins, name):
    table = Table.grid(padding=1)
    table.add_column(justify="center")

    table.add_row("[bold bright_white on dark_green] 1. 🃏 Blackjack [/bold bright_white on dark_green]")
    table.add_row("[bold bright_white on dark_blue] 2. 🎯 Hangman   [/bold bright_white on dark_blue]")
    table.add_row("[bold bright_white on dark_magenta] 3. 🔤 Wordle   [/bold bright_white on dark_magenta]")
    table.add_row("[bold bright_white on red] 4. 🚪 Exit       [/bold bright_white on red]")

    header = f"[bold yellow]Player:[/bold yellow] {name}    [bold green]Coins:[/bold green] {coins}"

    console.print(Panel(
        Align.center(table),
        title="[bold cyan]Select Your Game[/bold cyan]",
        subtitle=header,
        border_style="bright_magenta",
        padding=(1, 4)
    ))


def loading(text):
    for i in range(3):
        console.print(f"[bold cyan]{text}{'.' * (i+1)}[/bold cyan]", end="\r")
        sleep(0.3)
    console.print(" " * 30, end="\r")


# =========================
# 🎮 GAME WRAPPERS
# =========================

def play_blackjack(coins):
    game = Blackjack()
    game.balance = coins
    game.play()
    return game.balance


def play_hangman(coins):
    game = Hangman()
    game.play()

    if game.is_game_won:
        console.print("[bold green]💰 +20 coins![/bold green]")
        coins += 20
    else:
        console.print("[bold red]💸 -10 coins[/bold red]")
        coins = max(0, coins - 10)

    sleep(1.5)
    return coins


def play_wordle(coins):
    game = Wordle()
    game.play()

    console.print("[bold green]💰 +15 coins![/bold green]")
    coins += 15

    sleep(1.5)
    return coins


# =========================
# 🚀 MAIN LOOP
# =========================

def main():
    clear_screen()
    show_title()

    name = Prompt.ask("Enter your name", default="Player")
    coins = 100

    while True:
        clear_screen()
        show_title()
        show_menu(coins, name)

        choice = Prompt.ask("\n[bold cyan]Select option[/bold cyan]", choices=["1", "2", "3", "4"])

        if choice == "1":
            clear_screen()
            loading("Shuffling cards")
            coins = play_blackjack(coins)

        elif choice == "2":
            clear_screen()
            loading("Building gallows")
            coins = play_hangman(coins)

        elif choice == "3":
            clear_screen()
            loading("Choosing word")
            coins = play_wordle(coins)

        elif choice == "4":
            console.print("\n[bold magenta]Goodbye, legend. 🎮[/bold magenta]")
            sleep(1)
            break

        console.print("\n[dim]Press Enter to return...[/dim]")
        input()


if __name__ == "__main__":
    main()
import random
import os
from time import sleep

DELAY = 0.6

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Blackjack:
    def __init__(self) -> None:
        self.balance: int = 100
        self.set_round()

    def set_round(self) -> None:
        self.deck = self.create_deck()
        self.player = [self.deck.pop(), self.deck.pop()]
        self.dealer = [self.deck.pop(), self.deck.pop()]
        self.bet: int = 0
        self.player_bust: bool = False

    # === main logic ===

    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        deck = [(r, s) for r in ranks for s in suits]
        random.shuffle(deck)
        return deck

    def card_value(self, card):
        rank = card[0]
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        return int(rank)

    def hand_value(self, hand):
        total = sum(self.card_value(c) for c in hand)
        aces = sum(1 for c in hand if c[0] == 'A')

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    # === displays ===

    def section(self, title):
        print(f"\n--- {title} ---\n")

    def show_hand(self, name, hand, hide_first=False):
        if hide_first:
            visible = hand[1]
            print(f"{name}: [Hidden], {visible[0]} of {visible[1]} (Showing: {self.card_value(visible)})")
        else:
            cards = ", ".join(f"{r} of {s}" for r, s in hand)
            print(f"{name}: {cards} (Value: {self.hand_value(hand)})")

    # === actions ===

    def get_bet(self):
        while True:
            try:
                bet = int(input("Enter bet: "))
                if 0 < bet <= self.balance:
                    self.bet = bet
                    self.balance -= bet
                    return
                print("Invalid bet.")
            except ValueError:
                print("Enter a number.")

    def player_turn(self):
        self.section("PLAYER'S TURN")

        while True:
            self.show_hand("You", self.player)
            self.show_hand("Dealer", self.dealer, hide_first=True)

            if self.hand_value(self.player) > 21:
                self.player_bust = True
                sleep(DELAY)
                return

            move = input("Hit (h) or Stand (s): ").lower()

            if move == 'h':
                self.player.append(self.deck.pop())
            elif move == 's':
                return
            else:
                print("Invalid input!")

    def dealer_turn(self):
        if self.player_bust:
            return

        self.section("DEALER'S TURN")

        print("Dealer reveals:")
        self.show_hand("Dealer", self.dealer)

        while self.hand_value(self.dealer) < 17:
            print("Dealer hits...")
            self.dealer.append(self.deck.pop())
            self.show_hand("Dealer", self.dealer)
            sleep(DELAY)

    def show_result(self):
        self.section("RESULT")

        p = self.hand_value(self.player)
        d = self.hand_value(self.dealer)

        print(f"You: {p} | Dealer: {d}")

        if self.player_bust:
            print("You busted! Dealer wins!")
        elif d > 21 or p > d:
            print("You win!")
            self.balance += self.bet * 2
        elif p < d:
            print("Dealer wins!")
        else:
            print("Push!")
            self.balance += self.bet

    # === main loop ===

    def play(self):
        while self.balance > 0:
            clear_screen()
            self.set_round()

            self.section("NEW ROUND")
            print(f"Balance: {self.balance}")

            self.get_bet()

            self.section("DEALING CARDS")

            self.player_turn()
            self.dealer_turn()
            self.show_result()

            if self.balance <= 0:
                print("\nYou're out of money!")
                break

            replay = input("\nPlay again? (y/n): ").lower()
            if replay != 'y':
                break

        print("\n")
        print(f"Final balance: {self.balance}")
        print("\nThanks for playing!")

# === run game ===

if __name__ == "__main__":
    game = Blackjack()
    game.play()
import random


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.suit} {self.rank}: {BlackJack.values[self.rank]}"


class Hand:
    def __init__(self):
        self.cards = []  # start with empty list
        self.value = 0
        self.aces = 0

    def adjust_for_ace(self):
        self.value -= 10

    def add_card(self, card):
        self.cards.append(card)
        self.value += BlackJack.values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
            if self.value > 21:
                self.adjust_for_ace()

    def __str__(self):
        return f"Current Hand:{self.cards}\nCurrent Value:{self.value}\nCurrent Aces:{self.aces}\n"


class Deck:
    game = None

    def __init__(self, card_game):

        self.game = card_game

        # create deck with all 52 cards
        self.cards = list()
        for suit in self.game.suits:
            for rank in self.game.ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        return f"{[x for x in self.cards]}"


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += (self.bet*2)
        self.bet = 0

    def lose_bet(self):
        self.total -= self.bet
        self.bet = 0

    def make_bet(self, bet):
        if bet <= self.total:
            self.bet = bet
        else:
            raise ValueError(f"{bet} exceeds available chips")

    def __str__(self):
        return f"Total: {self.total}\nCurrent Bet:{self.bet}\n"


class Player:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.lost_games = 0
        self.chips = Chips()

    def __str__(self):
        return f"{self.name}:\n{self.wins} wins\n{self.lost_games} losses\nChips:{self.chips}\n"


class BlackJack:

    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
    values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
              'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

    def __init__(self, player):
        self.player = player
        self.deck = Deck(self)
        self.playing = False

    def status(self, dealer, player_name, player):
        print(f"Dealer: {dealer.value} - {player_name}: {player.value}")

    def play(self):
        """
        # 1. Create a deck of 52 cards
        # 2. Shuffle the deck
        # 3. Ask the Player for their bet
        # 4. Make sure that the Player's bet does not exceed their available chips
        # 5. Deal two cards to the Dealer and two cards to the Player
        # 6. Show only one of the Dealer's cards, the other remains hidden
        # 7. Show both of the Player's cards
        # 8. Ask the Player if they wish to Hit, and take another card
        # 9. If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
        # 10. If a Player Stands, play the Dealer's hand.
        #     The dealer will always Hit until the Dealer's value meets or exceeds 17
        # 11. Determine the winner and adjust the Player's chips accordingly
        # 12. Ask the Player if they'd like to play again
        """

        self.playing = True
        self.deck.shuffle()
        while self.playing:
            while True:
                try:
                    # Ask the Player for their bet
                    bet = int(input("Please put your bet: "))

                    # Make sure that the Player's bet does not exceed their available chips
                    self.player.chips.make_bet(bet)

                    break
                except TypeError:
                    print("Invalid input. Please try again")
                except ValueError as exc:
                    print(f"{exc} Please try again")

            # Deal two cards to the Dealer and two cards to the Player
            dealer = Hand()
            p = Hand()
            p.add_card(self.deck.deal_card())
            dealer.add_card(self.deck.deal_card())
            p.add_card(self.deck.deal_card())
            dealer.add_card(self.deck.deal_card())

            # Show only one of the Dealer's cards, the other remains hidden
            print(f"Dealer's card (one hidden): {dealer.cards[0]}")

            # Show both of the Player's cards
            print(f"{self.player.name}'s Cards: {p.cards[0]}, {p.cards[1]}")

            # Ask the Player if they wish to Hit, and take another card
            # If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
            action = 'h'
            while action == 'h' and p.value < 21:
                print(f"{self.player.name}: current {p.value}")
                action = input("Do you wish to 'Hit' ('h') or 'Stay' ('s')? ")
                if action == 's':
                    print(f"{self.player.name} (Hand {p.value}): STAY\n")
                    break  # dealers turn
                else:
                    print(f"{self.player.name} (Hand {p.value}): HIT\n")
                    cd = self.deck.deal_card()
                    print(f"Deal Card: {cd}")
                    p.add_card(cd)

            if p.value > 21:
                # player busts -  lost his bet
                print(f"\n{'='*80}")
                self.status(dealer, self.player.name, p)
                print(f"{self.player.name} (Hand: {p.value}): BUST")
                self.player.chips.lose_bet()
                self.player.lost_games += 1
                self.playing = False
                break
            else:
                # If a Player Stands, play the Dealer's hand.
                #    The dealer will always Hit until the Dealer's value meets or exceeds 17
                while dealer.value < 17:
                    print(f"Dealer (Hand: {dealer.value}): ADD CARD")
                    dealer.add_card(self.deck.deal_card())

                self.status(dealer, self.player.name, p)
                if dealer.value > 21:
                    print(f"Dealer BUSTS, {self.player.name} WINS")
                    self.player.chips.win_bet()
                    self.player.wins += 1
                    self.playing = False
                    break

            # Determine the winner and adjust the Player's chips accordingly
            if p.value > dealer.value:
                print(f"{self.player.name} WINS: {p.value} > {dealer.value}")
                self.player.chips.win_bet()
                self.player.wins += 1
            elif p.value < dealer.value:
                print(f"Dealer WINS: {p.value} < {dealer.value}")
                self.player.chips.lose_bet()
                self.player.lost_games += 1
            else:
                print(f"Dealer == {self.player.name}: {p.value} == {dealer.value}")
            self.playing = False


if __name__ == "__main__":

    playing = True

    # Play a new game of BlackJack with Player Daniela
    playr = Player('Daniela')

    while playing:
        game = BlackJack(playr)
        game.play()
        print(f"GAME DONE. Game Stats:\n {playr}")

        # Ask the Player if they'd like to play again
        if input("Would you like another game? y/n: ") != 'y':
            playing = False

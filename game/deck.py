from random import shuffle
from utils import Suit, Rank


class Card:
    def __init__(self, suit: Suit, rank: Rank) -> None:
        self.suit = suit
        self.rank: Rank = rank
        self.effect = None

        self._init_effect()

    def _init_effect(self) -> None:
        pass

    def __repr__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    CARD_COUNT = len(Suit) * 8

    def __init__(self) -> None:
        self.reset_deck()
        self.next_player_effect = None

    def reset_deck(self) -> None:
        self.playing_pile = []
        self._init_drawpile()

    def _init_drawpile(self) -> None:
        self.drawpile = []
        for suit in Suit:
            for rank in Rank:
                self.drawpile.append(Card(suit, rank))

        shuffle(self.drawpile)

    def emmit_effect(self) -> ...:
        return self.next_player_effect

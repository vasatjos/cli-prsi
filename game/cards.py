from random import shuffle
from card_utils import Suit, Rank, CardEffect


class Card:
    def __init__(self, suit: Suit, rank: Rank) -> None:
        self.suit = suit
        self.rank: Rank = rank

        self.effect: CardEffect | None
        self._init_effect(rank)

    def _init_effect(self, rank) -> None:
        if rank is Rank.SEVEN:
            self.effect = CardEffect.DRAW_TWO
        elif rank is Rank.OBER:
            self.effect = CardEffect.CHANGE_SUIT
        elif rank is Rank.ACE:
            self.effect = CardEffect.SKIP_TURN
        else:
            self.effect = None

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

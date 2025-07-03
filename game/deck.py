from random import shuffle

from game.card_utils import Suit, Rank, CardEffect
from game.card import Card


class Deck:
    CARD_COUNT = len(Suit) * 8

    def __init__(self) -> None:
        self.playing_pile: list[Card]
        self.drawpile: list[Card]
        self.next_player_effect: CardEffect | None

        self.reset_deck()

    def reset_deck(self) -> None:
        self.playing_pile: list[Card] = []
        self._init_drawpile()
        self.next_player_effect: CardEffect | None = None

    def _init_drawpile(self) -> None:
        self.drawpile: list[Card] = []
        for suit in Suit:
            for rank in Rank:
                self.drawpile.append(Card(suit, rank))

        shuffle(self.drawpile)

    def draw_card(self) -> Card:
        return self.drawpile.pop()

    def play_card(self, card: Card) -> None:
        self.playing_pile.append(card)
        self.next_player_effect = card.effect

    def emmit_effect(self) -> CardEffect | None:
        return self.next_player_effect

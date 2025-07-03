from random import shuffle

from game.card_utils import Suit, Rank, CardEffect
from game.card import Card


class Deck:
    CARD_COUNT = len(Suit) * 8

    def __init__(self) -> None:
        self.discard_pile: list[Card]
        self.drawing_pile: list[Card]

        self.reset_deck()

    def reset_deck(self) -> None:
        self.discard_pile: list[Card] = []
        self.drawing_pile = [Card(suit, rank) for suit in Suit for rank in Rank]
        shuffle(self.drawing_pile)

    @staticmethod
    def generate_suit(suit: Suit) -> list[Card]:
        return [Card(suit, rank) for rank in Rank]

    @staticmethod
    def generate_rank(rank: Rank) -> list[Card]:
        return [Card(suit, rank) for suit in Suit]

    def draw_card(self) -> Card:
        """
        Draw a card from the drawing pile.

        If the drawing pile is empty, the discard pile gets flipped over
        and becomes the drawing pile.
        """

        if len(self.drawing_pile) > 0:
            return self.drawing_pile.pop()

        # Flip over playing pile
        playing_pile_top_card = self.discard_pile.pop()
        self.drawing_pile = list(reversed(self.discard_pile))
        self.discard_pile = []
        self.discard_pile.append(playing_pile_top_card)

        return self.drawing_pile.pop()

    def play_card(self, card: Card) -> CardEffect | None:
        """
        Take a card and put it on top of the discard pile.

        Returns:
          The effect of the played card if it has one, None otherwise.
        """

        self.discard_pile.append(card)
        return card.effect

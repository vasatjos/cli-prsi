from functools import total_ordering

from game.card_utils import Suit, Rank, CardEffect


@total_ordering
class Card:
    def __init__(self, suit: Suit, rank: Rank) -> None:
        self.suit = suit
        self.rank = rank

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

    def __lt__(self, other) -> bool:
        return (
            self.rank < other.rank or self.rank == other.rank and self.suit < other.suit
        )

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.suit, self.rank))

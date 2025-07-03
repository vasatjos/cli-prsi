import pytest
from game.card import Card
from game.deck import Deck
from game.card_utils import Suit, Rank, CardEffect


def test_card_effects():
    assert Card(Suit.HEARTS, Rank.SEVEN).effect == CardEffect.DRAW_TWO
    assert Card(Suit.ACORNS, Rank.OBER).effect == CardEffect.CHANGE_SUIT
    assert Card(Suit.BELLS, Rank.ACE).effect == CardEffect.SKIP_TURN
    assert Card(Suit.LEAVES, Rank.KING).effect is None
    assert Card(Suit.HEARTS, Rank.EIGHT).effect is None
    assert Card(Suit.LEAVES, Rank.TEN).effect is None


def test_card_ordering():
    low = Card(Suit.HEARTS, Rank.SEVEN)
    high = Card(Suit.HEARTS, Rank.ACE)
    assert low < high
    assert not high < low
    assert high >= low

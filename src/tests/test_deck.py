import pytest

from game.card import Card
from game.card_utils import Suit, Rank, CardEffect
from game.deck import Deck


def test_deck_initialization():
    deck = Deck()
    # Check total number of cards
    assert len(deck.drawpile) == Deck.CARD_COUNT
    assert len(deck.playing_pile) == 0
    assert deck.next_player_effect is None


def test_draw_card_reduces_drawpile():
    deck = Deck()
    count_before = len(deck.drawpile)
    card = deck.draw_card()
    count_after = len(deck.drawpile)

    assert isinstance(card, Card)
    assert count_after == count_before - 1


def test_play_card_sets_effect():
    raise NotImplementedError
    deck = Deck()
    card = Card(Suit.HEARTS, Rank.SEVEN)
    deck.play_card(card)

    assert deck.playing_pile[-1] == card
    assert deck.emmit_effect() == CardEffect.DRAW_TWO

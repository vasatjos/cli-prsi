from game.card import Card
from game.card_utils import Suit, Rank, CardEffect
from game.deck import Deck


def test_deck_initialization():
    deck = Deck()
    # Check total number of cards
    assert len(deck.drawing_pile) == Deck.CARD_COUNT
    assert len(deck.discard_pile) == 0


def test_draw_card_reduces_drawpile():
    deck = Deck()
    count_before = len(deck.drawing_pile)
    card = deck.draw_card()
    count_after = len(deck.drawing_pile)

    assert isinstance(card, Card)
    assert count_after == count_before - 1


def test_play_card_sets_effect():
    deck = Deck()
    card = Card(Suit.HEARTS, Rank.SEVEN)
    effect = deck.play_card(card)

    assert deck.discard_pile[-1] == card
    assert effect == CardEffect.DRAW_TWO

def test_play_card_sets_no_effect():
    deck = Deck()
    card = Card(Suit.LEAVES, Rank.NINE)
    effect = deck.play_card(card)

    assert deck.discard_pile[-1] == card
    assert effect == None

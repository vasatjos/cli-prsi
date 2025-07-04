from game.card import Card
from game.deck import Deck
from game.state_manager import GameStateManager
from game.card_utils import CardEffect, Rank, Suit


def test_get_suit_choice_success(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "h")
    selected = GameStateManager.get_suit_choice()
    assert selected is Suit.HEARTS

    monkeypatch.setattr("builtins.input", lambda _: "a")
    selected = GameStateManager.get_suit_choice()
    assert selected is Suit.ACORNS

    monkeypatch.setattr("builtins.input", lambda _: "B")
    selected = GameStateManager.get_suit_choice()
    assert selected is Suit.BELLS

    monkeypatch.setattr("builtins.input", lambda _: "L")
    selected = GameStateManager.get_suit_choice()
    assert selected is Suit.LEAVES


def test_get_suit_choice_retry(monkeypatch):
    inputs = iter(["", "xyz", "1", "a"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    selected = GameStateManager.get_suit_choice()
    assert selected is Suit.ACORNS


def test_find_allowed_sevens():
    manager = GameStateManager()
    manager._actual_suit = Suit.BELLS
    manager.top_card = Card(Suit.BELLS, Rank.SEVEN)
    manager.current_effect = CardEffect.DRAW_TWO
    manager.effect_strength = 1

    should_be_allowed = Deck.generate_rank(Rank.SEVEN)
    allowed = manager.find_allowed_cards()
    assert should_be_allowed == allowed


def test_find_allowed_aces():
    manager = GameStateManager()
    manager._actual_suit = Suit.HEARTS
    manager.top_card = Card(Suit.HEARTS, Rank.ACE)
    manager.current_effect = CardEffect.SKIP_TURN
    manager.effect_strength = 1

    should_be_allowed = Deck.generate_rank(Rank.ACE)
    allowed = manager.find_allowed_cards()
    assert should_be_allowed == allowed


def test_find_allowed_actual_is_different_from_top():
    manager = GameStateManager()
    manager._actual_suit = Suit.LEAVES
    manager.top_card = Card(Suit.HEARTS, Rank.OBER)
    manager.current_effect = None
    manager.effect_strength = 0

    should_be_allowed = Deck.generate_suit(Suit.LEAVES) | Deck.generate_rank(Rank.OBER)
    allowed = manager.find_allowed_cards()
    assert should_be_allowed == allowed

from game.state_manager import GameStateManager
from game.card_utils import Suit


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

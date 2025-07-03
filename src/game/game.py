from game.deck import Deck
from game.player import Player
from game.state_manager import GameStateManager

class Prsi:
    STARTING_HAND = 4
    MAX_PLAYER_COUNT = 6  # 32 - 7 * 4 is not enough for everyone to draw

    def __init__(self) -> None:
        self._player_count: int = 0
        self._players: list[Player] = []
        self._deck: Deck = Deck()
        self._effect_manager: GameStateManager = GameStateManager()

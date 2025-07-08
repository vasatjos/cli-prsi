import os

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

    @staticmethod
    def _print_menu() -> int:
        """
        Print the menu.

        Returns:
          The number of players who will be playing. 0 is returned if the user
          wishes to exit.
        """
        while True:
            user_input = input(
                "Please select the number of players (2-6). Enter 0 to exit: "
            )
            try:
                num_players = int(user_input)
                if num_players > Prsi.MAX_PLAYER_COUNT:
                    raise ValueError
                if num_players < 2:
                    return 0
                return num_players
            except ValueError:
                os.system("clear")
                print("Please insert a valid number of players.")

    def _deal(self) -> None:
        for _ in range(Prsi.STARTING_HAND):
            for player in self._players:
                player.take_drawn_cards([self._deck.draw_card()])

    def start_game(self) -> None:
        self._player_count = self._print_menu()
        if not self._player_count:
            return
        self._players = [Player() for _ in range(self._player_count)]
        self._deal()

        self._game_loop()

    def _game_loop(self) -> None:
        while True:
            pass

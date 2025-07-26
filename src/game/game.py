import os

from game.card_utils import CardEffect
from game.deck import Deck
from game.card import Card
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
        self._last_winner: Player | None = None

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

    def _reset_screen(self) -> None:
        os.system("clear")
        input("Press enter to start your turn.")
        os.system("clear")

        print(f"Current top card: {self._deck.discard_pile[-1]}\n")

    def start_game(self) -> None:
        while True:
            self._player_count = Prsi._print_menu()
            if not self._player_count:
                return
            self._deck.reset()
            self._players = [Player(i) for i in range(self._player_count)]
            self._effect_manager.update(self._deck.discard_pile[0], first_card=True)
            self._deal()
            self._game_loop()

    def _game_loop(self) -> None:
        if not 2 <= self._player_count <= Prsi.MAX_PLAYER_COUNT:
            raise RuntimeError("Player count not valid.")

        while True:
            for player in self._players:
                # TODO: Update last winner for changing player counts
                if self._last_winner is not None and player != self._last_winner:
                    continue  # start with last winner
                self._last_winner = None

                self._reset_screen()
                print("Current cards on hand:")
                player.print_hand()
                allowed = self._effect_manager.find_allowed_cards()
                print("\nPlayable cards:")
                player_choice = player.select_card_to_play(allowed)
                print()

                if player_choice is not None:
                    self._deck.play_card(player_choice)
                else:
                    # TODO: Draw multiple on 7s
                    # TODO: Improve turn skipping logic
                    drawn = [self._deck.draw_card()]
                    if self._effect_manager.current_effect is CardEffect.SKIP_TURN:
                        drawn: list[Card] = []
                    player.take_drawn_cards(drawn)

                self._effect_manager.update(player_choice)

            if self._last_winner is not None:
                break

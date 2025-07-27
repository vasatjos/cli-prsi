import os

from game.card_utils import CardEffect, COLOR_RESET
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
        self._last_player_count: int = 0

    @staticmethod
    def _print_menu() -> int:
        """
        Print the menu.

        Returns:
          The number of players who will be playing. 0 is returned if the user
          wishes to exit.
        """
        os.system("clear")
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
                print("Please insert a valid number of players.")

    def _deal(self) -> None:
        for _ in range(Prsi.STARTING_HAND):
            for player in self._players:
                player.take_drawn_cards([self._deck.draw_card()])

    def _reset_screen(self, player_id: int) -> None:
        player_id += 1  # one based index
        os.system("clear")
        input(f"Press enter to start player #{player_id} turn.")
        os.system("clear")

        print(f"Player #{player_id} currently playing.\n")
        print(f"Current top card: {self._effect_manager.top_card}")

        assert self._effect_manager.actual_suit
        assert self._effect_manager.top_card

        if self._effect_manager.actual_suit != self._effect_manager.top_card.suit:
            print(
                f"Current suit: {self._effect_manager.actual_suit.value}"
                + f"{self._effect_manager.actual_suit.name}{COLOR_RESET}"
            )

        print()

    def start_game(self) -> None:
        while True:
            self._player_count = Prsi._print_menu()
            if not self._player_count:
                return
            self._deck.reset()
            self._players = [Player(i) for i in range(self._player_count)]
            if self._last_winner and self._last_player_count != self._players:
                self._last_winner = None
            self._effect_manager.update(self._deck.discard_pile[0], first_card=True)
            self._deal()
            self._game_loop()

    def _draw_cards(self) -> list[Card]:
        drawn: list[Card] = []

        match self._effect_manager.current_effect:
            case CardEffect.DRAW_TWO:
                for _ in range(self._effect_manager.effect_strength):
                    drawn.append(self._deck.draw_card())
                    drawn.append(self._deck.draw_card())
            case CardEffect.SKIP_TURN:
                pass
            case _:
                drawn.append(self._deck.draw_card())

        return drawn

    def _game_loop(self) -> None:
        if not 2 <= self._player_count <= Prsi.MAX_PLAYER_COUNT:
            raise RuntimeError("Player count not valid.")

        while True:
            for player in self._players:
                if self._last_winner is not None and player != self._last_winner:
                    continue  # start with last winner
                self._last_winner = None

                self._reset_screen(player.id)
                print("Current cards on hand:")
                player.print_hand()
                allowed = self._effect_manager.find_allowed_cards()
                print("\nPlayable cards:")
                player_choice = player.select_card_to_play(allowed)
                print()

                if player_choice is not None:
                    self._deck.play_card(player_choice)

                    if not len(player._hand_set):
                        self._last_winner = player
                        input("Congratulations, you win! Press enter to continue.")
                        break

                else:
                    drawn: list[Card] = self._draw_cards()
                    player.take_drawn_cards(drawn)

                self._effect_manager.update(player_choice)

            if self._last_winner is not None:
                break

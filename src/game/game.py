import os

from game.card_utils import CardEffect, COLOR_RESET, Rank, Suit
from game.deck import Deck
from game.card import Card
from game.player import Player
from game.state_manager import GameStateManager


class Prsi:
    STARTING_HAND_SIZE = 4
    MAX_PLAYER_COUNT = 6  # 32 - 7 * 4 is not enough for everyone to draw

    def __init__(self) -> None:
        self._player_count: int = 0
        self._players: list[Player] = []
        self._deck: Deck = Deck()
        self._effect_manager: GameStateManager = GameStateManager()
        self._last_winner: Player | None = None
        self._last_player_count: int = 0
        self._done_playing: list[Player] = []

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
                if 2 <= num_players <= Prsi.MAX_PLAYER_COUNT or num_players == 0:
                    return num_players
                raise ValueError
            except ValueError:
                print("Please insert a valid number of players.")

    def _deal(self) -> None:
        for _ in range(Prsi.STARTING_HAND_SIZE):
            for player in self._players:
                player.take_drawn_cards([self._deck.draw_card()])

    def _print_game_state(self, player: Player) -> None:
        player_id = player.id + 1  # print with one based index
        os.system("clear")
        input(f"Press enter to start player #{player_id} turn.")
        os.system("clear")

        for p in self._players:
            if p == player:
                print(f"Player #{player_id} currently playing.")
            else:
                print(f"Player #{p.id + 1} has {p.card_count()} cards")
        print(f"\nTop card: {self._effect_manager.top_card}")

        if (
            self._effect_manager.actual_suit is None
            or self._effect_manager.top_card is None
        ):
            raise RuntimeError("Manager not initialized.")

        if self._effect_manager.top_card.rank is Rank.OBER:
            print(
                f"Current suit: {self._effect_manager.actual_suit.value}"
                + f"{self._effect_manager.actual_suit.name}{COLOR_RESET}"
            )

        print("\nCards on hand:")
        player.print_hand()

    def _get_player_card_choice(self, player: Player) -> Card | None:
        self._print_game_state(player)
        allowed = self._effect_manager.find_allowed_cards()
        print("\nPlayable cards:")
        player_choice = player.select_card_to_play(allowed)
        print()

        return player_choice

    def start_game(self) -> None:
        while True:
            self._player_count = Prsi._print_menu()
            if not self._player_count:
                return
            self._deck.reset()
            self._players = [Player(i) for i in range(self._player_count)]
            if self._last_winner and self._last_player_count != self._player_count:
                self._last_winner = None
            self._effect_manager.update(self._deck.discard_pile[0], first_card=True)
            self._done_playing = []
            self._deal()
            self._game_loop()

    def _draw_cards(self) -> list[Card]:
        match self._effect_manager.current_effect:
            case CardEffect.DRAW_TWO:
                drawn = []
                for _ in range(self._effect_manager.effect_strength):
                    drawn.append(self._deck.draw_card())
                    drawn.append(self._deck.draw_card())
                return drawn
            case CardEffect.SKIP_TURN:
                return []
            case _:
                return [self._deck.draw_card()]

    def _print_order(self) -> None:
        os.system("clear")
        print("---GAME OVER---\n\nResults:\n")

        if self._last_winner is None:
            raise RuntimeError
        print(f"Winner: Player #{self._last_winner.id + 1}")
        for position, player in enumerate(self._done_playing[1:], start=2):
            print(f"Finished at position {position}: Player #{player.id + 1}")

        input("\nPress Enter to continue.")

    def _end_game(self) -> None:
        if not self._done_playing:
            raise RuntimeError("Game ended without any players finishing.")
        self._last_winner = self._done_playing[0]
        self._print_order()

    def _take_turn(self, player: Player) -> None:

        if not player.card_count():
            seven_hearts = Card(Suit.HEARTS, Rank.SEVEN)
            if (
                self._effect_manager.top_card == seven_hearts
                and self._effect_manager.current_effect is not None
            ):
                pass
            else:
                self._done_playing.append(player)
                self._effect_manager.update()
                return
        player_choice = self._get_player_card_choice(player)

        if player_choice is not None:
            self._deck.play_card(player_choice)
        else:
            drawn = self._draw_cards()
            player.take_drawn_cards(drawn)

        self._effect_manager.update(player_choice)

    def _game_loop(self) -> None:
        if not 2 <= self._player_count <= Prsi.MAX_PLAYER_COUNT:
            raise RuntimeError("Player count not valid.")

        while len(self._done_playing) + 1 < self._player_count:
            for player in self._players:
                if len(self._done_playing) + 1 >= self._player_count:
                    break
                if player in self._done_playing:
                    continue
                if self._last_winner is not None and player != self._last_winner:
                    continue  # start with last winner
                self._last_winner = None

                self._take_turn(player)

        for player in self._players:  # add last player for displaying purposes
            if player not in self._done_playing:
                self._done_playing.append(player)

        self._end_game()

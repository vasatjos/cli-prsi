from game.card import Card


class Player:
    def __init__(self, id: int) -> None:
        self._hand_set: set[Card] = set()
        self._id = id

    @property
    def id(self):
        return self._id

    def __eq__(self, other) -> bool:
        return self._id == other._id

    def print_hand(self, cards: list[Card] | None = None) -> None:
        """
        Print given cards in a sorted order.
        """

        if cards is None:
            cards = list(self._hand_set)
        cards.sort()
        for i, card in enumerate(cards, start=1):
            print(f"{i}. {card}")

    def select_card_to_play(self, allowed: set[Card]) -> Card | None:
        """
        Select a card from the players hand which he will play.

        Parameters:
          allowed: A set of cards which can be played based on the state of the game
            and active effects.

        Returns:
          None if player chose to draw a card. Drawing logic handled by separate method,
          handling of this behaviour falls on the caller.
          Otherwise simply the card the player chose to play.
        """

        playable = list(self._hand_set & allowed)
        if len(playable) == 0:
            input("No cards available, press enter to draw.")
            return None
        self.print_hand(playable)

        while True:
            # TODO: Change "0 to draw" to "empty input to draw"
            choice_input = input(
                "Enter the number of the card you want to play, "
                + "enter 0 to draw a card: "
            )
            try:
                choice = int(choice_input)
                if not 0 <= choice <= len(playable):
                    print("Inserted number too high.")
                    continue
                break  # valid input
            except ValueError:
                print("Please insert a number.")

        card_index = choice - 1  # type: ignore
        if card_index >= 0:
            chosen_card = playable[card_index]
            self._hand_set.remove(chosen_card)
            return chosen_card
        else:
            return None  # draw a card

    def take_drawn_cards(self, drawn_cards: list[Card]) -> None:
        self._hand_set.update(drawn_cards)

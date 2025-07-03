from game.card import Card


class Player:
    def __init__(self) -> None:
        self._hand_set: set[Card] = set()

    def print_hand(self, cards: list[Card] | None) -> None:
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
          None if player chose to draw a card. Drawing logic handled by separate function.
          Otherwise simply the card the player chose to play.
        """

        playable = list(self._hand_set.intersection(allowed))
        if len(playable) == 0:
            input("No cards available, press enter to draw.")
            return None
        self.print_hand(playable)

        valid_choice = False
        while not valid_choice:
            choice = input(
                "Enter the number of the card you want to play, "
                + "enter 0 to draw a card: "
            )
            try:
                choice = int(choice)
                if not -1 < choice <= len(playable):  # <= since 1 based indexing
                    raise IndexError
                else:
                    valid_choice = True
            except ValueError:
                print("Please insert a number.")
            except IndexError:
                print("Inserted number too high.")

        card_index = choice - 1  # type: ignore
        if card_index >= 0:
            chosen_card = playable[card_index]
            self._hand_set.remove(chosen_card)
            return chosen_card
        else:
            return None  # draw a card

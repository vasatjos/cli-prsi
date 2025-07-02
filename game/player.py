from cards import Card


class Player:
    def __init__(self) -> None:
        self.hand: list[Card] = []

    def print_hand(self, hand: list[Card] | None = None) -> None:
        if hand is None:
            hand = self.hand
        hand.sort()
        for i, card in enumerate(hand, start=1):
            print(f"{i}. {card}")

    def select_card_to_play(self, allowed: set[Card]) -> Card | None:
        """Select a card from the players hand which he will play.

        Parameters:
          allowed: A set of cards which can be played based on the state of the game
            and active effects.

        Returns:
          None if player chose to draw a card. Drawing logic handled by separate function.
          Otherwise simply the card the player chose to play.
        """

        player_cards = set(self.hand)
        playable = list(player_cards.intersection(allowed))
        self.print_hand(playable)

        valid_choice = False
        while not valid_choice:
            choice = input(
                "Enter the number of the card you want to play, "
                + "enter 0 to draw a card: "
            )
            try:
                choice = int(choice)
                if not -1 < choice < len(playable):
                    raise ValueError
                else:
                    valid_choice = True
            except ValueError:
                print("Please insert a valid card number")

        card_index = choice - 1  # type: ignore
        if card_index >= 0:
            chosen_card = playable[card_index]
            self.hand.remove(chosen_card)
            return chosen_card
        else:
            # TODO: Draw a card.
            #
            # Can be done via passing the effects as a parameter,
            # by passing the entire effect manager instead of allowed cards,
            # or by pulling the functionality out (prefered).
            ...
            return None

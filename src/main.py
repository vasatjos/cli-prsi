import os
from game.game import Prsi


def main() -> None:
    game = Prsi()
    game.start_game()
    os.system("clear")


if __name__ == "__main__":
    main()

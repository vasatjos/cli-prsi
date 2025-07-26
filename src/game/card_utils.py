from enum import Enum, StrEnum, IntEnum

COLOR_RESET = "\033[0m"


class Suit(StrEnum):
    HEARTS = "\033[31m"
    LEAVES = "\033[32m"
    BELLS = "\033[34m"
    ACORNS = "\033[33m"


class Rank(IntEnum):
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    UNTER = 11
    JACK = 11  # alias, doesn't affect __len__
    OBER = 12
    QUEEN = 12  # alias, doesn't affect __len__
    KING = 13
    ACE = 14


class CardEffect(Enum):
    SKIP_TURN = 0
    DRAW_TWO = 2

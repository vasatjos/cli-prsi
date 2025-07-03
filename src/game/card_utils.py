from enum import Enum, StrEnum, IntEnum


class Suit(StrEnum):
    HEARTS = "hearts"
    LEAVES = "leaves"
    BELLS = "bells"
    ACORNS = "acorns"


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

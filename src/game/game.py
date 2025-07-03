class Prsi:
    STARTING_HAND = 4
    MAX_PLAYER_COUNT = 6  # 32 - 7 * 4 is not enough for everyone to draw

    def __init__(self) -> None:
        self._player_count: int | None = None

from enum import Enum


class AdjacentPosition(Enum):
    UP = (1, 0)
    DOWN = (-1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (1, -1)
    UP_RIGHT = (-1, 1)
    UP_LEFT = (-1, -1)

    def helper(self):
        return self.value


ADJACENT_4 = list(
    map(
        AdjacentPosition.helper,
        [
            AdjacentPosition.UP,
            AdjacentPosition.DOWN,
            AdjacentPosition.RIGHT,
            AdjacentPosition.LEFT,
        ],
    )
)
ADJACENT_RIGHT = list(
    map(
        AdjacentPosition.helper,
        [
            AdjacentPosition.RIGHT,
            AdjacentPosition.DOWN_RIGHT,
            AdjacentPosition.UP_RIGHT,
            AdjacentPosition.UP,
            AdjacentPosition.DOWN,
        ],
    )
)
ADJACENT_ALL = list(
    map(
        AdjacentPosition.helper,
        [
            AdjacentPosition.UP,
            AdjacentPosition.DOWN,
            AdjacentPosition.RIGHT,
            AdjacentPosition.LEFT,
            AdjacentPosition.DOWN_RIGHT,
            AdjacentPosition.DOWN_LEFT,
            AdjacentPosition.UP_RIGHT,
            AdjacentPosition.UP_LEFT,
        ],
    )
)

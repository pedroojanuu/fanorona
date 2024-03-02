class TypeOfMove(enum.Enum):
    APPROACH = 1
    WITHDRAWAL = 2
    FREE = 3

class Move:
    def __init__(self, x_origin, y_origin, x_destination, y_destination, type):
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.x_destination = x_destination
        self.y_destination = y_destination
        self.type = type
from enum import Enum

class TypeOfMove(Enum):
    APPROACH = 1
    WITHDRAWAL = 2
    FREE = 3

class Move:
    def __init__(self, row_origin, col_origin, row_destination, col_destination, type):
        self.row_origin = row_origin
        self.col_origin = col_origin
        self.row_destination = row_destination
        self.col_destination = col_destination
        self.type = type

    def __str__(self):
        return f"({self.row_origin}, {self.col_origin}) -> ({self.row_destination}, {self.col_destination}, {self.type})"
    
    def __repr__(self):
        return f"({self.row_origin}, {self.col_origin}) -> ({self.row_destination}, {self.col_destination}, {self.type})"
    
    def get_destination(self):
        return (self.row_destination, self.col_destination)
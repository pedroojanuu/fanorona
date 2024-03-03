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
        return f"({self.row_origin}, {self.col_origin}) -> ({self.row_destination}, {self.col_destination}) {self.type}"
    
    def __repr__(self):
        return f"({self.row_origin}, {self.col_origin}) -> ({self.row_destination}, {self.col_destination}) {self.type}"
    
    def __eq__(self, __value: object) -> bool:
        return self.row_origin == __value.row_origin and self.col_origin == __value.col_origin and self.row_destination == __value.row_destination and self.col_destination == __value.col_destination and self.type == __value.type
    
    def get_destination(self):
        return (self.row_destination, self.col_destination)
    
    def get_origin(self):
        return (self.row_origin, self.col_origin)
import state

class Game:
    def __init__(self):
        self.board = Board()
        self.player = PlayerEnum.BLACK
    
    def change_player(self):
        self.player = opponent_player(self.player)

    def play(self):
        pass

def opponent_player(player):
    if player == PlayerEnum.BLACK:
        return PlayerEnum.WHITE
    return PlayerEnum.BLACK


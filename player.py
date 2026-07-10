from voice import VoiceController

class Player:
    def __init__(self, name, piece):

        self.name = name
        self.piece = piece
        self.voice = VoiceController()

    def get_move(self, board):
        while True:
            column = self.voice.listen()

            if column in board.valid_moves():
                return column

            else:
                print("Invalid column, try again")
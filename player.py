from voice import VoiceController

class Player:
    def __init__(self, name, piece):
        # Set human player with name, piece, and voice microphone controller
        self.name = name
        self.piece = piece
        self.voice = VoiceController() #Linked microphone helper to listen for speech

    def get_move(self, board):
        # Listen to user until you hear a valid column number
        while True:
            # Convert the speech into a number.
            column = self.voice.listen()

            # Check if chosen column is open and allowed.
            if column in board.valid_moves():
                return column # Get back valid column choice.

            else:
                # if column filled up
                print("Invalid column, try again")
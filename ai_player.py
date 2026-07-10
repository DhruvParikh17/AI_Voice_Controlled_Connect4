import random


class AIPlayer:

    def __init__(self, name, piece):

        self.name = name
        self.piece = piece


    def get_move(self, board):

        opponent_piece = "X"

        #Scenario A: Can I win right now?
        for move in board.valid_moves():
            test_board = board.copy()
            test_board.drop_piece(
                move,
                self.piece
            )

            if test_board.check_win(self.piece):
                return move

        #Scenario B: Can the player win next turn?
        for move in board.valid_moves():
            test_board = board.copy()
            test_board.drop_piece(
                move,
                opponent_piece
            )

            if test_board.check_win(opponent_piece):
                return move

        #Scenario C: Take center if possible
        if 3 in board.valid_moves():
            return 3

        #Scenario D: Otherwise random
        return random.choice(
            board.valid_moves()
        )
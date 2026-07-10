from board import Board
from player import Player
from ai_player import AIPlayer

board = Board()

player1 = Player("Player", "X")
player2 = AIPlayer("Computer", "O")

while True:
    board.print_board()
    move = player1.get_move(board)
    board.drop_piece(
        move,
        player1.piece
    )

    if board.check_win(player1.piece):
        board.print_board()
        print("You win!")
        break

    move = player2.get_move(board)

    board.drop_piece(
        move,
        player2.piece
    )

    print("Computer played.")

    if board.check_win(player2.piece):
        board.print_board()
        print("Computer wins!")
        break
from board import Board
from player import Player
from ai_player import AIPlayer


def print_colored_board(board):
    # This function draws the game board on the screen using blue circles (You) and yellow circles (AI).
    print("\n" + "=" * 29)
    print("      CONNECT 4 (VOICE)")
    print("=" * 29)

    for row in board.grid:
        print("|", end="")
        for cell in row:
            if cell == "X":
                print(" 🔵 |", end="")  # Blue for Player X
            elif cell == "O":
                print(" 🟡 |", end="")  # Yellow for Computer O
            else:
                print("    |", end="")
        print()

    # Formating board.
    print("-" * 29)
    print("   1   2   3   4   5   6   7")
    print("=" * 29 + "\n")


def main():
    board = Board()
    player1 = Player("Player", "X")
    player2 = AIPlayer("Computer", "O")

    print("Game started! Speak your column numbers (1 to 7) when prompted.")

    while True:
        #Render current board
        print_colored_board(board)

        # Player Turn
        print("🎙️  Listening for your move... (Say 'one' through 'seven')")
        move = player1.get_move(board)

        # Validate players move
        if move not in board.valid_moves():
            print("❌ Invalid or unclear column. Try speaking again.")
            continue

        # Drop piece
        board.drop_piece(move, player1.piece)

        # Check if they won
        if board.check_win(player1.piece):
            print_colored_board(board)
            print("🎉 Congratulations! You win!")
            break

        # Check for a tie
        if not board.valid_moves():
            print_colored_board(board)
            print("It's a tie!")
            break

        # Computer Turn
        print("🤖 Computer is thinking...")
        ai_move = player2.get_move(board)
        board.drop_piece(ai_move, player2.piece)
        print(f"Computer played in column {ai_move + 1}")

        # Check if AI won
        if board.check_win(player2.piece):
            print_colored_board(board)
            print("🤖 Computer wins! Better luck next time.")
            break

        # Check for a tie
        if not board.valid_moves():
            print_colored_board(board)
            print("It's a tie!")
            break


if __name__ == "__main__":
    main()
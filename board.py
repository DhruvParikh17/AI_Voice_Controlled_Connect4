class Board:

    ROWS = 6
    COLS = 7

    def __init__(self):
        self.grid = []#creates a empty grid.

        for row in range(self.ROWS):
            self.grid.append(
                [" "] * self.COLS #Creates a row.
            )


    def print_board(self): #printing the board.

        print()

        for row in self.grid: #printing the rows.
            print("|", end="") #printing the vertical bars.

            for cell in row: #printing each cell
                print(cell + "|", end="")

            print()

        print(" 1 2 3 4 5 6 7")
        print()


    def drop_piece(self, column, piece): #drop a piece into the right spot.

        #start from bottom row.
        for row in range(self.ROWS - 1, -1, -1):

            if self.grid[row][column] == " ": #finding empty spot.

                self.grid[row][column] = piece
                return True


        return False


    def valid_moves(self): #finding avaliable moves.

        moves = []

        for col in range(self.COLS):

            if self.grid[0][col] == " ":
                moves.append(col)

        return moves

    def check_win(self, piece):

        # Horizontal check
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):

                if (
                        self.grid[row][col] == piece and
                        self.grid[row][col + 1] == piece and
                        self.grid[row][col + 2] == piece and
                        self.grid[row][col + 3] == piece
                ):
                    return True

        # Vertical check
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):

                if (
                        self.grid[row][col] == piece and
                        self.grid[row + 1][col] == piece and
                        self.grid[row + 2][col] == piece and
                        self.grid[row + 3][col] == piece
                ):
                    return True

        # Diagonal down-right \
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):

                if (
                        self.grid[row][col] == piece and
                        self.grid[row + 1][col + 1] == piece and
                        self.grid[row + 2][col + 2] == piece and
                        self.grid[row + 3][col + 3] == piece
                ):
                    return True

        # Diagonal up-right /
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):

                if (
                        self.grid[row][col] == piece and
                        self.grid[row - 1][col + 1] == piece and
                        self.grid[row - 2][col + 2] == piece and
                        self.grid[row - 3][col + 3] == piece
                ):
                    return True

        return False

    def copy(self):

        new_board = Board()

        for row in range(self.ROWS):
            for col in range(self.COLS):
                new_board.grid[row][col] = self.grid[row][col]

        return new_board
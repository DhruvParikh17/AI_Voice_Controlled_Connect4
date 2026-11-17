import tkinter as tk
import os
import sys
from board import Board
from player import Player
from ai_player import AIPlayer


class Connect4App:
    def __init__(self, root):
        # Initializes the main application window, core game state, and UI parts.
        self.root = root
        self.root.title("AI Voice-Controlled Connect 4")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        # Scoreboard Tracking
        self.user_wins = 0
        self.ai_wins = 0

        # Game Logic Setup
        self.board = Board()
        self.player1 = None  # Lazy initialization to prevent startup lag
        self.player2 = AIPlayer("Computer", "O")
        self.game_over = False

        # Header
        header_frame = tk.Frame(root, bg="white")
        header_frame.pack(pady=8)

        # Title
        title_label = tk.Label(
            header_frame,
            text="Welcome to AI Controlled Connect 4",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg="#111"
        )
        title_label.pack()

        # Title (creator)
        creator_label = tk.Label(
            header_frame,
            text="Created By: Dhruv M. Parikh",
            font=("Helvetica", 11, "italic"),
            bg="white",
            fg="#555"
        )
        creator_label.pack(pady=2)

        # Messanger (Gives live time messages)
        banner_frame = tk.Frame(root, bg="#f8f9fa", bd=1, relief=tk.SOLID, padx=10, pady=6)
        banner_frame.pack(fill=tk.X, padx=20, pady=5)

        self.status_label = tk.Label(
            banner_frame,
            text="Click 'Take Voice Turn' to start!",
            font=("Helvetica", 12, "bold"),
            bg="#f8f9fa",
            fg="#222",
            justify="center"
        )
        self.status_label.pack()

        # Main Game Area
        content_frame = tk.Frame(root, bg="white")
        content_frame.pack(padx=15, pady=5)

        # Connect 4 Board
        self.CELL_SIZE = 75
        canvas_width = 7 * self.CELL_SIZE
        canvas_height = 7 * self.CELL_SIZE
        self.canvas = tk.Canvas(
            content_frame,
            width=canvas_width,
            height=canvas_height,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, padx=10)

        # Control Panel
        sidebar = tk.Frame(content_frame, bg="white", padx=15)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        # Scoreboard Panel
        score_title = tk.Label(sidebar, text="Scoreboard", font=("Helvetica", 13, "bold"), bg="white")
        score_title.pack(anchor="w", pady=(0, 4))
        # The current live score
        self.score_label = tk.Label(
            sidebar,
            text="You: 0  |  AI: 0",
            font=("Helvetica", 12, "bold"),
            bg="#f4f4f4",
            fg="#222",
            padx=10,
            pady=6
        )
        self.score_label.pack(anchor="w", fill=tk.X, pady=(0, 10))

        tk.Frame(sidebar, height=2, bg="#ddd").pack(fill=tk.X, pady=8)

        # Legend Panel
        legend_title = tk.Label(sidebar, text="Players", font=("Helvetica", 13, "bold"), bg="white")
        legend_title.pack(anchor="w", pady=(0, 4))

        tk.Label(sidebar, text=" 🔵 You (Player X)", font=("Helvetica", 11, "bold"), fg="#1E90FF", bg="white").pack(
            anchor="w", pady=2)
        tk.Label(sidebar, text=" 🟡 AI (Computer O)", font=("Helvetica", 11, "bold"), fg="#B8860B", bg="white").pack(
            anchor="w", pady=2)

        tk.Frame(sidebar, height=2, bg="#ddd").pack(fill=tk.X, pady=15)

        # Voice turn & Restart buttons
        self.turn_button = tk.Button(
            sidebar,
            text="Take Voice Turn",
            font=("Helvetica", 11, "bold"),
            bg="#1E90FF",
            fg="black",
            padx=10,
            pady=10,
            command=self.play_turn
        )
        self.turn_button.pack(anchor="w", fill=tk.X, pady=(0, 10))

        self.restart_button = tk.Button(
            sidebar,
            text="Restart Game",
            font=("Helvetica", 11, "bold"),
            bg="#e0e0e0",
            fg="black",
            padx=10,
            pady=8,
            command=self.restart_game
        )
        self.restart_button.pack(anchor="w", fill=tk.X)

        # Initial render of the graphical board grid
        self.draw_board()

    def draw_board(self):
        # Redraws the canvas grid, column header numbers, background board, and game pieces.
        self.canvas.delete("all")

        # Draw column numbers 1 to 7 on top of the grid
        for col in range(7):
            cx = col * self.CELL_SIZE + self.CELL_SIZE // 2
            cy = self.CELL_SIZE // 2
            self.canvas.create_text(
                cx, cy,
                text=str(col + 1),
                font=("Helvetica", 14, "bold"),
                fill="black"
            )

        # The board body
        self.canvas.create_rectangle(
            0, self.CELL_SIZE,
            7 * self.CELL_SIZE, 7 * self.CELL_SIZE,
            fill="black",
            outline="black"
        )

        # Go through rows and column to draw the correct circular slots and pieces
        for r in range(6):
            for c in range(7):
                x1 = c * self.CELL_SIZE + 10
                y1 = (r + 1) * self.CELL_SIZE + 10
                x2 = (c + 1) * self.CELL_SIZE - 10
                y2 = (r + 2) * self.CELL_SIZE - 10

                piece = self.board.grid[r][c]
                color = "white"  # Default color for empty slot
                if piece == "X":
                    color = "#1E90FF"  # Blue for User
                elif piece == "O":
                    color = "#FFD700"  # Yellow for AI

                self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def play_turn(self):
        # Manages the full turn sequence; listening for user voice input, updating board, and triggering AI response.
        if self.game_over:
            return

        # User Turn
        # Lazy initialization; Load microphone helper only on first click to avoid startup lag
        if self.player1 is None:
            self.status_label.config(text="Initializing microphone...")
            self.root.update()
            self.player1 = Player("Player", "X")

        # Prompt user that microphone is active
        self.status_label.config(text="🎙️ Listening for your move (say 1-7)...")
        self.root.update()

        # Listen for speech and convert to column choice
        col = self.player1.voice.listen()

        # Validate if chosen column is legal
        if col not in self.board.valid_moves():
            self.status_label.config(text="❌ Invalid move or unclear speech. Try again!")
            return

        # Drop User Piece and redraw board
        self.board.drop_piece(col, "X")
        self.draw_board()

        # Check if user won the game
        if self.board.check_win("X"):
            self.status_label.config(text="🎉 You Won! Excellent strategy!")
            self.user_wins += 1
            self.update_scoreboard()
            self.turn_button.config(state=tk.DISABLED)
            self.game_over = True
            return

        # Check for a tie
        if not self.board.valid_moves():
            self.status_label.config(text="🤝 It's a tie!")
            self.turn_button.config(state=tk.DISABLED)
            self.game_over = True
            return

        # AI turn
        self.status_label.config(text="🤖 AI is thinking...")
        self.root.update()

        ai_move = self.player2.get_move(self.board)
        self.board.drop_piece(ai_move, "O")
        self.draw_board()

        # Check if AI won the game
        if self.board.check_win("O"):
            self.status_label.config(text="🤖 AI Wins the Round! Better luck next time!")
            self.ai_wins += 1
            self.update_scoreboard()
            self.turn_button.config(state=tk.DISABLED)
            self.game_over = True
            return

        # Check for a tie after AI move
        if not self.board.valid_moves():
            self.status_label.config(text="🤝 It's a tie!")
            self.turn_button.config(state=tk.DISABLED)
            self.game_over = True
            return

        # Hand control back to user
        self.status_label.config(text="Your turn! Click 'Take Voice Turn'.")

    def update_scoreboard(self):
        # Updates the scoreboard panel with current win counts
        self.score_label.config(text=f"You: {self.user_wins}  |  AI: {self.ai_wins}")

    def restart_game(self):
        # Resets the board state and unlocks controls for a new match.
        self.board = Board()
        self.game_over = False
        self.turn_button.config(state=tk.NORMAL)
        self.status_label.config(text="New game started! Click 'Take Voice Turn'.")
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()

    # Force macOS to bring window to the front on launch
    if sys.platform == "darwin":
        os.system(
            '''osascript -e 'tell application "System Events" to set frontmost of every process whose unix id is %d to true' ''' % os.getpid())

    app = Connect4App(root)
    root.mainloop()
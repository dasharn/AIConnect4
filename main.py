import tkinter as tk
from tkinter import messagebox

# Constants for the game
WIDTH = 7
HEIGHT = 6
PLAYER_1 = "X"
PLAYER_2 = "O"

class ConnectFourGame:
    def __init__(self):
        # Create a game board
        self.game_board = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

        # Initialize the Tkinter window
        self.window = tk.Tk()
        self.window.title("Connect Four")

        # Create the GUI elements
        self.canvas = tk.Canvas(self.window, width=WIDTH * 80 + 40, height=HEIGHT * 80 + 40, bg="blue")
        self.canvas.pack()

        # Bind the canvas to a mouse click event
        self.canvas.bind("<Button-1>", self.make_move)

        # Draw the initial game board
        self.draw_board()

    def make_move(self, event):
        # This method is called when the player makes a move by clicking on the game board.
        # It determines the column where the player clicked and updates the game board accordingly.
        # Then it checks if the player has won or if it's a draw, and takes appropriate actions.
        # Get the column based on the mouse click position
        column = event.x // 80

        # Find the next available row in the selected column
        for row in range(HEIGHT - 1, -1, -1):
            if self.game_board[row][column] == ' ':
                # Make the move for player 1
                self.game_board[row][column] = PLAYER_1
                self.draw_board()

                # Check for a winning condition or draw
                if self.check_winner(row, column, PLAYER_1):
                    messagebox.showinfo("Game Over", "Player 1 wins!")
                    self.reset_game()
                    return
                if self.check_draw():
                    messagebox.showinfo("Game Over", "It's a draw!")
                    self.reset_game()
                    return

                # AI makes its move
                self.ai_move()
                return

    def ai_move(self):
        # This method is responsible for the AI's move in the game.
        # It uses the minimax algorithm to evaluate the best move for the AI player.
        # The algorithm recursively explores the game tree to find the optimal move.
        # The AI player makes its move based on the best score obtained from the minimax algorithm.

        best_score = float('-inf')
        best_move = None

        # Iterate over each column and find the best move for the AI player
        for col in range(WIDTH):
            if self.is_valid_move(col):
                row = self.get_next_row(col)
                self.game_board[row][col] = PLAYER_2

                # Use the minimax algorithm to determine the score of the move
                score = self.minimax(self.game_board, 4, float('-inf'), float('inf'), False)

                # Undo the move
                self.game_board[row][col] = ' '

                if score > best_score:
                    best_score = score
                    best_move = col

        # Make the best move for the AI player
        self.game_board[self.get_next_row(best_move)][best_move] = PLAYER_2
        self.draw_board()

        # Check for a winning condition or draw
        if self.check_winner(self.get_next_row(best_move), best_move, PLAYER_2):
            messagebox.showinfo("Game Over", "Player 2 wins!")
            self.reset_game()
            return
        if self.check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
            return

    def is_valid_move(self, column):
        # This method checks if a move (column) is valid, i.e., if the top cell in that column is empty.

        return self.game_board[0][column] == ' '

    def get_next_row(self, column):
        # This method returns the next available row in the specified column.
        # Check if the top row of the selected column is empty
        return self.game_board[0][column] == ' '

    def get_next_row(self, column):
        # Find the next available row in the selected column
        for row in range(HEIGHT - 1, -1, -1):
            if self.game_board[row][column] == ' ':
                return row

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        # This method implements the minimax algorithm with alpha-beta pruning.
        # It evaluates the best score for the current game state and returns it.

        # Check for a winning condition, losing condition, or draw
        if self.check_winner(None, None, PLAYER_2):
            return 1
        elif self.check_winner(None, None, PLAYER_1):
            return -1
        elif self.check_draw():
            return 0

        # Base case: reached the maximum depth
        if depth == 0:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for col in range(WIDTH):
                if self.is_valid_move(col):
                    row = self.get_next_row(col)
                    board[row][col] = PLAYER_2

                    # Recursively call minimax with the board after making the move
                    score = self.minimax(board, depth - 1, alpha, beta, False)

                    # Undo the move
                    board[row][col] = ' '

                    # Update the best score and alpha value
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)

                    # Perform alpha-beta pruning
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for col in range(WIDTH):
                if self.is_valid_move(col):
                    row = self.get_next_row(col)
                    board[row][col] = PLAYER_1

                    # Recursively call minimax with the board after making the move
                    score = self.minimax(board, depth - 1, alpha, beta, True)

                    # Undo the move
                    board[row][col] = ' '

                    # Update the best score and beta value
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)

                    # Perform alpha-beta pruning
                    if beta <= alpha:
                        break
            return best_score

    def check_winner(self, row, col, player):
        # This method checks if the specified player has won the game.
        # If row and col are None, it checks for a win in the entire game board.

        # Check for a winning condition in the entire board or a specific position
        if row is None and col is None:
            for r in range(HEIGHT):
                for c in range(WIDTH):
                    if self.game_board[r][c] == player:
                        if self.check_line(r, c, player):
                            return True
            return False
        else:
            return self.check_line(row, col, player)

    def check_line(self, row, col, player):
        # This method checks if there is a winning line passing through the specified cell.
        # It checks for a win horizontally, vertically, and diagonally.

        # Check for a winning condition horizontally, vertically, and diagonally
        # Check horizontally
        count = 0
        for c in range(WIDTH):
            if self.game_board[row][c] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # Check vertically
        count = 0
        for r in range(HEIGHT):
            if self.game_board[r][col] == player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0

        # Check diagonals
        for r in range(HEIGHT - 3):
            for c in range(WIDTH - 3):
                if (
                    self.game_board[r][c] == player and
                    self.game_board[r+1][c+1] == player and
                    self.game_board[r+2][c+2] == player and
                    self.game_board[r+3][c+3] == player
                ):
                    return True

        for r in range(3, HEIGHT):
            for c in range(WIDTH - 3):
                if (
                    self.game_board[r][c] == player and
                    self.game_board[r-1][c+1] == player and
                    self.game_board[r-2][c+2] == player and
                    self.game_board[r-3][c+3] == player
                ):
                    return True

        return False

    def check_draw(self):
         # This method checks if the game is a draw, i.e., if all cells are filled.
        # Check if the game is a draw (all positions on the board are filled)
        for row in range(HEIGHT):
            for col in range(WIDTH):
                if self.game_board[row][col] == ' ':
                    return False
        return True

    def draw_board(self):
         # This method draws the current game board on the canvas.
        # It uses rectangles to represent cells and ovals to represent player's moves.
        # Draw the game board and the player's moves on the canvas
        self.canvas.delete("all")
        for row in range(HEIGHT):
            for col in range(WIDTH):
                x1 = col * 80 + 20
                y1 = row * 80 + 20
                x2 = x1 + 60
                y2 = y1 + 60
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                if self.game_board[row][col] == PLAYER_1:
                    self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="red")
                elif self.game_board[row][col] == PLAYER_2:
                    self.canvas.create_oval(x1, y1, x2, y2, fill="yellow", outline="yellow")

    def reset_game(self):
         # This method resets the game by clearing the game board and redrawing the initial state.
        # Reset the game board to its initial state
        for row in range(HEIGHT):
            for col in range(WIDTH):
                self.game_board[row][col] = ' '
        self.draw_board()

    def start(self):
        # Start the Tkinter event loop
        self.window.mainloop()

# Create an instance of the game
game = ConnectFourGame()
game.start()

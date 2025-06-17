import tkinter as tk
import random
from collections import deque
import pygame

class SnakeAndLadder:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game with Zigzag Movement")

        self.board_size = 10
        self.board = [-1] * (self.board_size ** 2)

        # Define snakes and ladders on the board
        self.board[1] = 38  # Ladder from 1 to 38
        self.board[4] = 14  # Ladder from 4 to 14
        self.board[9] = 30  # Ladder from 9 to 31
        self.board[28] = 76  # Ladder from 9 to 31
        self.board[21] = 42  # Ladder from 9 to 31
        self.board[50] = 67  # Ladder from 9 to 31
        self.board[71] = 92  # Ladder from 9 to 31
        self.board[80] = 99  # Ladder from 9 to 31
        self.board[36] = 6  # Snake from 16 to 6
        self.board[32] = 10  # Snake from 48 to 26
        self.board[48] = 26  # Snake from 87 to 24
        self.board[62] = 18  # Snake from 87 to 24
        self.board[88] = 24  # Snake from 87 to 24
        self.board[95] = 56  # Snake from 87 to 24
        self.board[97] = 78  # Snake from 87 to 24

        self.players = [0, 0]  # Start two players at position 0
        self.current_player = 0  # Index of the current player
        self.player_colors = ["yellow", "pink"]  # Player colors

        # Game history
        self.history = []

        # Calculate the optimal solution (minimum moves) using BFS
        self.optimal_solution = self.min_dice_rolls()

        # Initialize pygame for sounds
        pygame.mixer.init()
        self.snake_sound = pygame.mixer.Sound("snake.mp3")  # Ensure you have the sound file
        self.ladder_sound = pygame.mixer.Sound("ladder.mp3")

        # Create GUI components
        self.create_board()
        self.create_controls()
        self.create_history()

    def create_board(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.cells = []
        for row in range(self.board_size):
            row_cells = []
            for col in range(self.board_size):
                cell_num = self.get_cell_number(row, col)
                cell_label = tk.Label(self.board_frame, text=str(cell_num), width=4, height=2, borderwidth=1, relief="solid")
                row_cells.append(cell_label)
                cell_label.grid(row=row, column=col)

                # Color the cells for snakes and ladders
                if cell_num == 1 or cell_num == 4 or cell_num == 9 or cell_num == 28 or cell_num == 21 or cell_num == 50 or cell_num == 71 or cell_num == 80:  # Ladders
                    cell_label.config(bg="lightgreen")
                elif cell_num == 36 or cell_num == 48 or cell_num == 32 or cell_num == 88 or cell_num == 62 or cell_num == 95 or cell_num == 97:  # Snakes
                    cell_label.config(bg="red")

            self.cells.append(row_cells)

    def get_cell_number(self, row, col):
        """
        Return the correct board number based on row and column.
        Even rows go left to right; odd rows go right to left.
        """
        if row % 2 == 0:  # Even row: left to right
            return row * self.board_size + col + 1
        else:  # Odd row: right to left
            return row * self.board_size + (self.board_size - col)

    def create_controls(self):
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.dice_label = tk.Label(self.control_frame, text="Roll the Dice!", font=("Arial", 14))
        self.dice_label.pack()

        self.roll_button = tk.Button(self.control_frame, text="Roll Dice", command=self.roll_dice, font=("Arial", 14), bg="lightgreen")
        self.roll_button.pack()

        self.position_label = tk.Label(self.control_frame, text=f"Player 1 Position: {self.players[0] + 1}", font=("Arial", 14))
        self.position_label.pack()

        self.solution_label = tk.Label(self.control_frame, text=f"Optimal Solution: {self.optimal_solution} dice rolls", font=("Arial", 14), fg="blue")
        self.solution_label.pack()

    def create_history(self):
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(pady=10)

        self.history_label = tk.Label(self.history_frame, text="Game History:", font=("Arial", 14))
        self.history_label.pack()

        self.history_text = tk.Text(self.history_frame, width=30, height=10)
        self.history_text.pack()

    def roll_dice(self):
        dice_value = random.randint(1, 6)
        self.dice_label.config(text=f"Dice Rolled: {dice_value}")
        self.history.append(f"Player {self.current_player + 1} rolled a {dice_value}")
        self.update_history()
        self.move_player(dice_value)

    def move_player(self, dice_value):
        new_position = self.players[self.current_player] + dice_value

        if new_position >= (self.board_size ** 2):
            self.dice_label.config(text=f"Player {self.current_player + 1} Wins!")
            self.roll_button.config(state=tk.DISABLED)
            return

        new_row = new_position // self.board_size
        new_col = new_position % self.board_size

        if new_row % 2 == 1:
            new_col = self.board_size - 1 - new_col

        zigzag_position = new_row * self.board_size + new_col

        if self.board[zigzag_position] != -1:
            if self.board[zigzag_position] > zigzag_position:
                self.ladder_sound.play()
            else:
                self.snake_sound.play()
            zigzag_position = self.board[zigzag_position]

        self.animate_move(zigzag_position)

    def animate_move(self, new_position):
        old_row, old_col = divmod(self.players[self.current_player], self.board_size)
        new_row, new_col = divmod(new_position, self.board_size)

        self.cells[old_row][old_col].config(bg="white")

        self.cells[new_row][new_col].config(bg=self.player_colors[self.current_player])
        self.root.update()

        self.root.after(500, self.update_player_position, new_position)

    def update_player_position(self, new_position):
        self.players[self.current_player] = new_position
        # Get the displayed position based on zigzag movement
        displayed_position = self.get_display_position(new_position)
        self.position_label.config(text=f"Player {self.current_player + 1} Position: {displayed_position}")
    
        self.current_player = (self.current_player + 1) % len(self.players)
    
    def get_display_position(self, position):
        """
        Return the correct display position based on the board number.
        """
        # Calculate row and column
        row, col = divmod(position, self.board_size)
    
        # For odd rows, we need to reverse the column index
        if row % 2 == 1:
            col = self.board_size - 1 - col
    
        # Calculate the actual board number (1-indexed)
        return row * self.board_size + col + 1
    

    def update_history(self):
        self.history_text.delete(1.0, tk.END)
        for entry in self.history:
            self.history_text.insert(tk.END, entry + "\n")

    def min_dice_rolls(self):
        n = len(self.board)
        visited = [False] * n
        queue = deque([(0, 0)])

        while queue:
            pos, rolls = queue.popleft()

            if pos == n - 1:
                return rolls

            for dice in range(1, 7):
                new_pos = pos + dice
                if new_pos < n:
                    if self.board[new_pos] != -1:
                        new_pos = self.board[new_pos]

                    if not visited[new_pos]:
                        visited[new_pos] = True
                        queue.append((new_pos, rolls + 1))

        return -1

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadder(root)
    root.mainloop()

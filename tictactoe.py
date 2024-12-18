class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # A 3x3 board
        self.current_player = 'X'

    def print_board(self):
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("--+---+--")
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("--+---+--")
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            if self.check_winner():
                self.print_board()
                print(f"Player {self.current_player} wins!")
                return True
            elif ' ' not in self.board:
                self.print_board()
                print("It's a tie!")
                return True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                return False
        else:
            print("This position is already taken. Try again.")
            return False

    def check_winner(self):
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)  # Diagonal
        ]
        for combo in win_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True
        return False

    def start_game(self):
        print("Welcome to Tic Tac Toe!")
        self.print_board()
        while True:
            try:
                position = int(input(f"Player {self.current_player}, enter a position (0-8): "))
                if position < 0 or position > 8:
                    print("Invalid position. Please choose a number between 0 and 8.")
                    continue
                if self.make_move(position):
                    break
                self.print_board()
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 8.")


if __name__ == "__main__":
    # To play the game
    game = TicTacToe()
    game.start_game()

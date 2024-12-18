from ai_algorithms import RandomAI, GreedyAI, BaseAI, MCTS_AI

def choose_ai_algorithm():
    print("Choose the AI algorithm you want to play against:")
    print("1. Random AI")
    print("2. Greedy AI")
    print("3. Monte Carlo Tree Search")
    choice = input("Enter the number of your choice (1, 2 or 3): ")
    if choice == '1':
        print("You chose Random AI.")
        return RandomAI
    elif choice == '2':
        print("You chose Greedy AI.")
        return GreedyAI
    elif choice == '3':
        print("You chose MCTS AI.")
        exploration_weight = float(
            input("Enter the exploration weight for MCTS (e.g., 1.414): "))
        time_limit = float(
            input("Enter the time limit for MCTS iterations (eg 100): "))
        return lambda symbol: MCTS_AI(symbol, exploration_weight, time_limit)
    else:
        print("Invalid choice. Defaulting to Random AI.")
        return RandomAI

class TicTacToe:
    def __init__(self, player1_type, player2_type):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.players = {
            'X': player1_type if player1_type == "human" else player1_type('X'),
            'O': player2_type('O') if callable(player2_type) else player2_type
    }

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
            player = self.players[self.current_player]
            if isinstance(player, BaseAI):  # AI Player
                print(f"AI Player {self.current_player} is thinking...")
                move = player.choose_move(self.board)
                print(f"AI chooses position {move}")
            else:  # Human Player
                while True:  # Keep asking until valid input
                    try:
                        move = int(
                            input(f"Player {self.current_player}, enter a position (0-8): "))
                        if move < 0 or move > 8:  # Check if move is within bounds
                            print(
                                "Invalid position. Please choose a number between 0 and 8.")
                            continue
                        if self.board[move] != ' ':  # Check if position is already taken
                            print("This position is already taken. Try again.")
                            continue
                        break  # Valid input, exit the loop
                    except ValueError:  # Handle non-integer inputs
                        print("Invalid input. Please enter a valid number between 0 and 8.")

            if self.make_move(move):
                break
            self.print_board()

if __name__ == "__main__":
    ai_class = choose_ai_algorithm()
    game = TicTacToe(
        player1_type="human",
        player2_type=ai_class if ai_class != MCTS_AI else lambda symbol: ai_class(
            symbol)
    )
    game.start_game()

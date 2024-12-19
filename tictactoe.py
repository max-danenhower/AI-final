from ai_algorithms import RandomAI, GreedyAI, BaseAI, MCTS_AI

def choose_ai_algorithm(player_name):
    """Prompt user to choose an AI algorithm for a player."""
    print(f"Choose the AI algorithm for {player_name}:")
    print("1. Random AI")
    print("2. Greedy AI")
    print("3. Monte Carlo Tree Search (MCTS)")
    print("4. Human")
    choice = input("Enter the number of your choice (1, 2, 3, or 4): ")
    if choice == '1':
        print("You chose Random AI.")
        return RandomAI, "Random AI"
    elif choice == '2':
        print("You chose Greedy AI.")
        return GreedyAI, "Greedy AI"
    elif choice == '3':
        print("You chose MCTS AI.")
        C = float(input("Enter the exploration weight for MCTS (e.g., 1.414): "))
        num_sims = int(input("Enter the limit for MCTS iterations (e.g., 100): "))
        return lambda symbol: MCTS_AI(symbol, num_sims=num_sims, C=C), f"MCTS (Sims: {num_sims}, C: {C})"
    elif choice == '4':
        print("You chose Human.")
        return "human", "Human"
    else:
        print("Invalid choice. Defaulting to Random AI.")
        return RandomAI, "Random AI"


class TicTacToe:
    def __init__(self, player1, player2, player1_name, player2_name):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.players = {
            'X': player1,
            'O': player2
        }
        self.player_names = {
            'X': player1_name,
            'O': player2_name
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
                print(f"{self.player_names[self.current_player]} ({self.current_player}) wins!")
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
                print(f"{self.player_names[self.current_player]} ({self.current_player}) is thinking...")
                move = player.choose_move(self.board)
                print(f"{self.player_names[self.current_player]} chooses position {move}")
            else:  # Human Player
                while True:
                    try:
                        move = int(input(f"{self.player_names[self.current_player]} ({self.current_player}), enter a position (0-8): "))
                        if move < 0 or move > 8:
                            print("Invalid position. Please choose a number between 0 and 8.")
                            continue
                        if self.board[move] != ' ':
                            print("This position is already taken. Try again.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number between 0 and 8.")

            if self.make_move(move):
                break
            self.print_board()


if __name__ == "__main__":
    ai1, ai1_name = choose_ai_algorithm("Player 1 (X)")
    ai2, ai2_name = choose_ai_algorithm("Player 2 (O)")
    
    # Instantiate players
    player1 = ai1('X') if callable(ai1) else "human"
    player2 = ai2('O') if callable(ai2) else "human"

    # Create and start the game
    game = TicTacToe(player1=player1, player2=player2, player1_name=ai1_name, player2_name=ai2_name)
    print(f"\nStarting game between Player 1 ({ai1_name}) and Player 2 ({ai2_name})")
    game.start_game()


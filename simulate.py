from ai_algorithms import RandomAI, GreedyAI, MCTS_AI
from tictactoe import TicTacToe

def choose_ai_algorithm(player_name):
    """Prompt user to choose an AI algorithm for a player."""
    print(f"Choose the AI algorithm for {player_name}:")
    print("1. Random AI")
    print("2. Greedy AI")
    print("3. Monte Carlo Tree Search (MCTS)")
    choice = input("Enter the number of your choice (1, 2, or 3): ")
    if choice == '1':
        return RandomAI, "Random AI"
    elif choice == '2':
        return GreedyAI, "Greedy AI"
    elif choice == '3':
        C = float(input("Enter the exploration weight for MCTS (e.g., 1.414): "))
        num_sims = int(input("Enter the number of simulations for MCTS: "))
        return lambda symbol: MCTS_AI(symbol, num_sims=num_sims, C=C), f"MCTS (Sims: {num_sims}, C: {C})"
    else:
        print("Invalid choice. Defaulting to Random AI.")
        return RandomAI, "Random AI"

def simulate_game(player1, player2, player1_name, player2_name):
    """Simulates a single game between two AI players."""
    game = TicTacToe(player1, player2, player1_name, player2_name)
    while True:
        current_player = game.players[game.current_player]
        move = current_player.choose_move(game.board)
        if game.make_move(move):
            # Check if it's a tie
            if ' ' not in game.board and not game.check_winner():
                return None  
            return game.current_player

def run_simulation(num_games, player1_class, player2_class, player1_name, player2_name):
    """Runs a series of games between two AI classes, alternating the starting player."""

    #dictionary holding the results, make it easy to outputs results
    results = {f"{player1_name} Wins": 0, f"{player2_name} Wins": 0, "Ties": 0}

    for game_num in range(num_games):

        # Alternate starting player
        if game_num % 2 == 0:
            player1 = player1_class('X')  
            player2 = player2_class('O')  
            winner = simulate_game(player1, player2, player1_name, player2_name) 
            if winner == 'X':
                results[f"{player1_name} Wins"] += 1
            elif winner == 'O':
                results[f"{player2_name} Wins"] += 1
            else:
                results["Ties"] += 1
        else:
            player1 = player1_class('O')
            player2 = player2_class('X') 
            winner = simulate_game(player2, player1, player2_name, player1_name)
            if winner == 'X':
                results[f"{player2_name} Wins"] += 1
            elif winner == 'O':
                results[f"{player1_name} Wins"] += 1
            else:
                results["Ties"] += 1
    return results


def run_simulation_NOSWITCH(num_games, player1_class, player2_class, player1_name, player2_name):
    """Runs a series of games between two AI classes, keeping the starting player consistent."""

    # Dictionary holding the results
    results = {f"{player1_name} Wins": 0, f"{player2_name} Wins": 0, "Ties": 0}

    for game_num in range(num_games):
        # Player 1 always starts as 'X', and Player 2 is always 'O'
        player1 = player1_class('X')  # Player 1 is 'X'
        player2 = player2_class('O')  # Player 2 is 'O'

        # Simulate the game
        winner = simulate_game(player1, player2, player1_name, player2_name)

        # Update the results
        if winner == 'X':
            results[f"{player1_name} Wins"] += 1
        elif winner == 'O':
            results[f"{player2_name} Wins"] += 1
        else:
            results["Ties"] += 1

    return results


if __name__ == "__main__":
    print("Welcome to Tic Tac Toe AI Simulator!")
    num_games = int(input("Enter the number of games to simulate: "))
    player1_class, player1_name = choose_ai_algorithm("Player 1 (X)")
    player2_class, player2_name = choose_ai_algorithm("Player 2 (O)")

    print("\nStarting simulation...")
    results = run_simulation(num_games, player1_class, player2_class, player1_name, player2_name)

    print("\nSimulation Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

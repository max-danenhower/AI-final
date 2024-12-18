import random


class BaseAI:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol

    def choose_move(self, board):
        raise NotImplementedError(
            "This method should be overridden by subclasses")


class RandomAI(BaseAI):
    
    def choose_move(self, board):
        return random.choice([i for i, x in enumerate(board) if x == ' '])


class GreedyAI(BaseAI):

    def choose_move(self, board):
        # Try to win or block opponent
        for move in range(9):
            if board[move] == ' ':
                # Simulate making a move
                board[move] = self.player_symbol
                if self.check_winner(board):
                    board[move] = ' '  # Reset board
                    return move
                board[move] = ' '  # Reset board
        return random.choice([i for i, x in enumerate(board) if x == ' '])

    def check_winner(self, board):
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)  # Diagonal
        ]
        for combo in win_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
                return True
        return False
    

class MCTS_AI(BaseAI):

    def choose_move(self, board):
        return super().choose_move(board)


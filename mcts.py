import random, math, time
from tictactoe import TicTacToe

class Node:
    def __init__(self, board, parent, player):
        self.player = player
        self.board = board
        self.parent = parent
        self.children = []
        self.num_visits = 0
        self.num_wins = 0

    def get_best_child(self):
        # get best child by implmenting UCT policy
        best_uct = float('-inf')
        best_child = None
        for child in self.children:
            uct = (child.num_wins/child.num_visits) + 1.2(math.sqrt(math.log(self.num_visits) / child.num_visits))
            if uct > best_uct:
                best_uct = uct
                best_child = None

        return best_child
        
    def get_valid_moves(self, board):
        """Returns a list of valid moves (empty spots)."""
        valid_moves = []
        for i, spot in enumerate(board):
            if spot == ' ':  # Check if the spot is empty
                valid_moves.append(i)
        return valid_moves
    
    def add_child(self, child):
        self.children.append(child)

    def check_winner(self, sim_board):
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)  # Diagonal
        ]
        for combo in win_combinations:
            if sim_board[combo[0]] == sim_board[combo[1]] == sim_board[combo[2]] != ' ':
                return True
        return False
    
    def print_board(self, board):
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("--+---+--")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("--+---+--")
        print(f"{board[6]} | {board[7]} | {board[8]}")
    
    def rollout(self):
        sim_player = self.player # 0 is the AI's turn
        sim_board = self.board[:]
        while True:
            valid_moves = self.get_valid_moves(sim_board)

            if (len(valid_moves) == 0):
                return 0 # sim ended in a tie 

            # move randomly
            move = random.choice(valid_moves)

            sim_board[move] = sim_player # the AI is always X

            if (self.check_winner(sim_board)):
                self.print_board(sim_board)
                if (sim_player == self.player):
                    # AI wins!
                    print('win')
                    return 1
                else:
                    print('loss')
                    return -1
            
            # switch turns in the simulation
            if sim_player == 'X':
                sim_player = 'O'
            else:
                sim_player =  'X'

    def backpropogate(self, value):
        self.num_visits += 1
        self.num_wins += value
        curr = self.parent
        while (curr != None):
            curr.num_visits += 1
            curr.num_wins += value
            curr = curr.parent


if __name__ == "__main__":
    board = ['X', ' ', 'O', ' ', ' ', 'X', 'O', 'O', ' ']
    root = Node(board, None, 'X')
    root.print_board(board)
    print(root.num_visits)
    print(root.num_wins)

    moves = root.get_valid_moves(board)
    for m in moves:
        child_board = board[:]
        child_board[m] = root.player
        child = Node(child_board, root, 'X')
        root.add_child(child)

    for child in root.children:
        print(child.print_board(child.board))

    child = root.children[0]

    val = child.rollout()

    child.backpropogate(val)

    print(root.num_visits)
    print(root.num_wins)


    

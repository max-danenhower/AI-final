import random, math, time
from visualize import MCTSVisualizer 



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
    
class Node:
    def __init__(self, board, parent, player, move):
        self.player = player
        self.board = board
        self.parent = parent
        self.children = []
        self.num_visits = 0
        self.num_wins = 0
        self.move = move

    def get_best_child(self, C):
        # get best child by implmenting UCT policy
        best_uct = float('-inf')
        best_child = None
        for child in self.children:
            if child.num_visits > 0:
                uct = (child.num_wins/child.num_visits) + C*(math.sqrt(math.log(self.num_visits) / child.num_visits))
            else:
                uct = float('inf')
            if uct >= best_uct:
                best_uct = uct
                best_child = child

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

    def expand_children(self):
        moves = self.get_valid_moves(self.board)
        for m in moves:
            child_board = self.board[:]
            child_board[m] = self.player
            child = Node(child_board, self, self.player, m)
            self.add_child(child)

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
                if (sim_player == self.player):
                    # AI wins!
                    return 1
                else:
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

class MCTS_AI(BaseAI):
    def __init__(self, player_symbol, num_sims, C):
        super().__init__(player_symbol)
        self.num_sims = num_sims
        self.C = C

    def choose_move(self, board):
        root = Node(board,None,self.player_symbol,None)
        iterations = 0
        curr_node = root

        while (iterations < self.num_sims):

            #explore - find leaf node using best child policy
            while (len(curr_node.children) > 0):
                curr_node = curr_node.get_best_child(self.C)

            #expand
            if curr_node.num_visits > 0:
                curr_node.expand_children()
                if len(curr_node.children) > 0:
                    curr_node = curr_node.children[0]

            #simulate
            val = curr_node.rollout()

            #backpropogate
            curr_node.backpropogate(val)
            iterations += 1
        

        best_child = root.get_best_child(self.C)
        print(best_child)
        return best_child.move


# class MCTS_AI(BaseAI):
#     def __init__(self, player_symbol, exploration_weight=1.414, time_limit=1.0):
#         super().__init__(player_symbol)
#         self.exploration_weight = exploration_weight
#         self.time_limit = time_limit

#     def choose_move(self, board):
#         """Implements the MCTS algorithm to choose the best move."""
#         root = MCTSNode(state=board, player=self.player_symbol)
#         mcts = MonteCarloTreeSearch(
#             time_limit=self.time_limit, exploration_weight=self.exploration_weight)
#         best_child = mcts.search(root)
#         for i, val in enumerate(board):
#             if board[i] != best_child.state[i]:  # Find the move made
#                 return i


class MCTSNode:
    def __init__(self, state, parent=None, player='X'):
        self.state = state[:]  # Board state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.player = player
        self.untried_moves = self.get_valid_moves()

    def get_valid_moves(self):
        """Returns a list of valid moves (empty spots)."""
        valid_moves = []
        for i, spot in enumerate(self.state):
            if spot == ' ':  # Check if the spot is empty
                valid_moves.append(i)
        return valid_moves

    def is_terminal(self):
        """Returns True if this is a terminal state (win or draw)."""
        # Check if there are no valid moves left (draw condition)
        no_valid_moves = len(self.get_valid_moves()) == 0
        has_winner = self.check_winner()

        if no_valid_moves or has_winner:
            return True
        else:
            return False
        
    def check_winner(self):
        """Check for a win in the current state."""
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)  # Diagonal
        ]
        for combo in win_combinations:
            if self.state[combo[0]] == self.state[combo[1]] == self.state[combo[2]] != ' ':
                return True
        return False

    def best_child(self, exploration_weight=1.414):
        """Select the best child node based on UCT."""
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits) +
            exploration_weight *
            math.sqrt(math.log(self.visits) / child.visits)
        )

    def expand(self):
        """Add a new child node for an unexplored move."""
        move = self.untried_moves.pop()
        new_state = self.state[:]
        new_state[move] = self.player
        next_player = 'O' if self.player == 'X' else 'X'
        child = MCTSNode(state=new_state, parent=self, player=next_player)
        self.children.append(child)
        return child

    def rollout(self):
        """Simulate a random game from this node and return the result."""
        current_state = self.state[:]
        current_player = self.player
        while True:
            valid_moves = [i for i, spot in enumerate(current_state) if spot == ' ']

            if not valid_moves:
                return 0  # Tie
            
            move = random.choice(valid_moves)
            current_state[move] = current_player
            if self.check_winner_static(current_state):
                return 1 if current_player == self.player else -1
            current_player = 'O' if current_player == 'X' else 'X'

    def backpropagate(self, result):
        """Backpropagate the result of a simulation."""
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(-result)

    @staticmethod
    def check_winner_static(state):
        """Static method to check if a state is a win."""
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)  # Diagonal
        ]
        for combo in win_combinations:
            if state[combo[0]] == state[combo[1]] == state[combo[2]] != ' ':
                return True
        return False


class MonteCarloTreeSearch:
    def __init__(self, time_limit=1.0, exploration_weight=1.414):
        self.time_limit = time_limit
        self.exploration_weight = exploration_weight

    def search(self, root):
        """Perform MCTS starting from the root node."""
        start_time = time.time()
        iterations = 0

        while time.time() - start_time < self.time_limit:
            node = root

            # Selection
            while node.children and not node.untried_moves:
                node = node.best_child(self.exploration_weight)

            # Expansion
            if node.untried_moves:
                node = node.expand()

            # Simulation
            result = node.rollout()

            # Backpropagation
            node.backpropagate(result)

            iterations += 1

        print(f"MCTS completed {iterations} iterations.")
        return root.best_child(exploration_weight=0.0)



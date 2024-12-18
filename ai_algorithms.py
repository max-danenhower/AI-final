import random, math



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

            if uct > best_uct:
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
            if self.player == 'X':
                child_player = 'O'
            else:
                child_player = 'X'
            child = Node(child_board, self, child_player, m) 
            self.add_child(child)

    def check_winner(self, sim_board):
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
            (0, 4, 8), (2, 4, 6)  # Diagonal
        ]
        for combo in win_combinations:
            if sim_board[combo[0]] == sim_board[combo[1]] == sim_board[combo[2]] != ' ':
                return sim_board[combo[0]]  # Return the winner ('X' or 'O')
        
        if ' ' not in sim_board:  # If no empty spots, it's a tie
            return 'Tie'
        
        return None  # Game is still ongoing

    
    def print_board(self):
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("--+---+--")
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("--+---+--")
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")
    
    def rollout(self):
        sim_player = self.player # 0 is the AI's turn
        sim_board = self.board[:]
        while True:
            valid_moves = self.get_valid_moves(sim_board)

            winner = self.check_winner(sim_board)

            if (winner != None):
                return winner

            # move randomly
            move = random.choice(valid_moves)

            sim_board[move] = sim_player 
            
            # switch turns in the simulation
            if sim_player == 'X':
                sim_player = 'O'
            else:
                sim_player =  'X'

    def backpropogate(self, winner):     
        if winner != 'Tie':
            if self.player == winner:
                self.num_wins -= 1
            else:
                self.num_wins += 1

        self.num_visits += 1
        if (self.parent != None):
            self.parent.backpropogate(winner)

    def print_node(self):
        if (self.parent != None):
            print('parent board:')
            self.parent.print_board()
        else:
            print('root node')
        print('num_visits: ', self.num_visits)
        print('num_wins: ', self.num_wins)
        print('player: ', self.player)
        print('node board:')
        self.print_board()
        print('num children: ', len(self.children))

class MCTS_AI(BaseAI):
    def __init__(self, player_symbol, num_sims, C):
        super().__init__(player_symbol)
        self.num_sims = num_sims
        self.C = C

    def print_tree(self, node, depth=0):
        # Print the current node's information with indentation for depth
        print("  " * depth*2 + f"Node {node.player} (Visits: {node.num_visits} Wins: {node.num_wins})")
        
        # Recursively print all child nodes
        for child in node.children:
            self.print_tree(child, depth + 1)

    def choose_move(self, board):
        root = Node(board,None,self.player_symbol,None)
        iterations = 0

        while (iterations < self.num_sims):
            curr_node = root

            #explore - find leaf node using best child policy
            while (len(curr_node.children) > 0):
                curr_node = curr_node.get_best_child(self.C)

            #expand
            if curr_node.num_visits > 0:
                curr_node.expand_children()
                if len(curr_node.children) > 0:
                    curr_node = curr_node.children[0]

            #simulate
            winner = curr_node.rollout()

            #backpropogate
            curr_node.backpropogate(winner)
            iterations += 1

        # select child with highest number of visits
        most_visits = 0
        i = 0
        next_move = None
        for child in root.children:
            print('-----------')
            print('child ', i)
            print('num visits: ', child.num_visits)
            print('num wins: ', child.num_wins)
            print('child move: ', child.move)
            v = child.num_visits
            if v > most_visits:
                most_visits = v
                next_move = child
            i+=1
        
        return next_move.move
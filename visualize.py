import pprint


class MCTSVisualizer:
    def __init__(self):
        """Initialize the visualizer."""
        self.tree_structure = {}

    def add_node(self, node, level=0):
        """
        Recursively add a node and its children to the visualization structure.
        :param node: The current MCTSNode.
        :param level: The depth of the node in the tree.
        """
        # Add the current node's details
        node_info = {
            # Represent board as a string for readability
            "state": "".join(node.state),
            "player": node.player,
            "visits": node.visits,
            "wins": node.wins,
            "untried_moves": node.untried_moves,
            "children": []
        }

        if level not in self.tree_structure:
            self.tree_structure[level] = []

        self.tree_structure[level].append(node_info)

        # Recursively add child nodes
        for child in node.children:
            self.add_node(child, level + 1)

    def visualize(self, root_node):
        """
        Build the tree structure from the root node and print it.
        :param root_node: The root of the MCTS tree.
        """
        print("Building MCTS visualization...")
        self.tree_structure = {}
        self.add_node(root_node)

        print("\n=== Monte Carlo Tree Search Visualization ===\n")
        for level, nodes in self.tree_structure.items():
            print(f"Level {level}:")
            for node in nodes:
                pprint.pprint(node)
            print("\n")

    def visualize_single_node(self, node):
        """
        Print details of a single node (useful for debugging specific nodes).
        :param node: The MCTSNode to visualize.
        """
        node_info = {
            "state": "".join(node.state),
            "player": node.player,
            "visits": node.visits,
            "wins": node.wins,
            "untried_moves": node.untried_moves,
            "children_count": len(node.children),
        }
        print("\n=== Node Details ===")
        pprint.pprint(node_info)

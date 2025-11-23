
class Node:

    def __init__(self):

        # Holds the children for a character at this level
        self.children = {}

        # If the node represents a word
        self.is_word_end = False

class Trie:

    def __init__(self):

        self.root = Node()

    def insert(self, keyword):
        """
           Insert a keyword into the Trie 
        """
        node = self.root

        # Create the tree for every char in the keyword
        for char in keyword:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]

        node.is_word_end = True

        return node

    # Find the node which matches the prefix
    def find_prefix_node(self, prefix):

        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]

        return node

    # Find words that are under the prefix
    def find_words_for_node(self, node, curr_prefix, results):
        # Node is a word
        if node.is_word_end:
            results.append(curr_prefix)

        # Check the rest of the tree to find all words that match the prefix
        for char, child in node.children.items():
            self.find_words_for_node(child, curr_prefix + char, results)
            
    def autocomplete(self, prefix):
        # Find words in the trie that starts with the prefix

        node_prefix = self.find_prefix_node(prefix)

        if node_prefix is None:
            return []

        results = []
        self.find_words_for_node(node_prefix, prefix, results)

        return results


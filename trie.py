
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

    def autocomplete(self, prefix):
        # TODO: Find words in the trie that starts with the prefix

        pass


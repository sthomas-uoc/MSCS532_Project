import graph

import trie

class TaskManager:

    def __init__(self):

        self.task_graph = graph.Graph()

        self.search_trie = trie.Trie()

    #TODO: Setup the functions that map to user actions

    def list_next_tasks(self):
        # TODO: List possible next tasks to pickup
        
        pass


if __name__ == "__main__":
    #TODO: Initialize the task manager to manage the application

    tm = TaskManager()

    #TODO: Add a REPL to allow users to manage tasks
    
    pass

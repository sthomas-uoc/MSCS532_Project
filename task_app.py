import graph

import trie

class Task:

    def __init__(self, name, description = None, keywords = None, dependencies = None):

        self.name = name

        self.description = description

        self.keywords = keywords

        self.dependencies = dependencies

class TaskManager:

    def __init__(self):

        self.task_graph = graph.Graph()

        self.search_trie = trie.Trie()

    #TODO: Setup the functions that map to user actions

    def add_task(self, task, depends_on = None):
        # TODO: Add task and add dependency if provided
        
        pass

    def list_next_tasks(self):
        # TODO: List possible next tasks to pickup
        
        pass

    def find_task_autocomplete(self, keyword_part):
        # TODO: Use the trie to find keywords that match the user input

        # TODO: List tasks that match the keyword

        pass

if __name__ == "__main__":
    #TODO: Initialize the task manager to manage the application

    tm = TaskManager()

    #TODO: Add a REPL to allow users to manage tasks

    
    
    pass

def tester():
    # TODO: Generate tasks that are dependent.

    # TODO: Search of tasks based on keyword

    # TODO: Select a task and mark as completed.

    # TODO: Get next task and validate

    # TODO: Test cyclic dependency - must fail to add task

    pass

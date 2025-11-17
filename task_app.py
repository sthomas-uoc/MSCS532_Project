from collections import defaultdict
import graph

import trie

from enum import Enum

class TaskStatus(Enum):

    Open = 1
    Closed = 2

class Task:

    def __init__(self, name, description = None, keywords = None, dependencies = None):

        self.name = name

        self.description = description

        # TODO: Ensure it is a list
        self.keywords = keywords

        # Remove direct mention in task, move to task manager
        # self.dependencies = dependencies

        self.status = TaskStatus.Open

class TaskManager:

    def __init__(self):

        self.task_graph = graph.Graph()

        self.search_trie = trie.Trie()

        # Tasks by ID
        self.tasks = {}

        # Keywords to tasks
        self.keyword_tasks = defaultdict(set)
        
    # Setup the functions that map to user actions
    def add_task(self, task):
        # Add task and add dependency if provided

        if task.name in self.tasks:
            print(f"ERROR: Task {task.name} already exists")
            return

        self.tasks[task.name] = task

        if task.keywords is None:
            task.keywords = []

        for keyword in task.keywords:
            keyword_lower = keyword.lower()
            self.keyword_tasks[keyword].add(task.name)

        print(f"Task {task.name} added")

    def get_task(self, task_name):

        return self.tasks[task_name]

    def update_task(self, task):

        has_existing_task = task.name in self.tasks
        if has_existing_task:
            existing_task = self.tasks[task.name]
            
            existing_task.description = task.description

            if task.status:
                existing_task.status = task.status

            if task.keywords is None:
                task.keywords = []

            # TODO: A difference and union of old an new keywords can be used to update the keywords efficiently
            for keyword in existing_task.keywords:
                keyword_lower = keyword.lower()
                self.keyword_tasks[keyword].remove(existing_task.name)
                # TODO: Delete the keyword entry if empty after removing the task
    
            for keyword in task.keywords:
                keyword_lower = keyword.lower()
                self.keyword_tasks[keyword].add(task.name)
            
            print(f"Task {task.name} updated")

            return True
        else:
            print(f"ERROR: No such task {task.name}")
            
            return False

    def delete_task(self, task_name):

        has_existing_task = task_name in self.tasks
        if has_existing_task:
            existing_task = self.tasks[task_name]

            # Check for tasks that depend on this
            if task_name in self.task_graph.graph and self.task_graph.graph[task_name]:
                print(f"ERROR: Cannot delete task {task_name} as it has dependent tasks")

                return False

            # Remove from map of tasks
            self.tasks.pop(task_name)
            
            for keyword in existing_task.keywords:
                keyword_lower = keyword.lower()
                self.keyword_tasks[keyword].remove(existing_task.name)
                # TODO: Delete the keyword entry if empty after removing the task

            # Remove task from the graph
            self.task_graph.graph.pop(task_name, None)

            if task_name in self.task_graph.in_degree:
                del self.task_graph.in_degree[task_name]
            
            print(f"Task {task_name} deleted")

            return True
        else:
            print(f"ERROR: No such task {task_name}")
            
            return False

        pass

    def add_dependency(self, task, task_depends_on):

        if not task.name in self.tasks or not task_depends_on in self.tasks:
            print(f"ERROR: Task or depends on task does not exist")
            return

        # task.name depends on dependency
        self.task_graph.add_edge(task_depends_on, task.name)

    def list_next_tasks(self):
        # List possible next tasks to pickup

        return self.task_graph.sort()

    def find_tasks_by_keyword(self, keyword):
        return None if not keyword in self.keyword_tasks else self.keyword_tasks[keyword]

    def find_task_autocomplete(self, keyword_part):
        # TODO: Use the trie to find keywords that match the user input

        # TODO: List tasks that match the keyword

        pass

if __name__ == "__main__":
    # Initialize the task manager to manage the application

    tm = TaskManager()

    #TODO: Add a REPL to allow users to manage tasks

    
    
    pass

def tester():
    tm = TaskManager()

    # Add tasks
    print("Testing adding tasks")
    task_design = Task("design", description = "Design the data structures", keywords = ["design", "data structures"])
    tm.add_task(task_design)
    
    task_implement = Task("implement", description = "Implement the data structures", keywords = ["implement", "data structures"])
    tm.add_task(task_implement)

    task_task_manager = Task("task_manager", description = "Build the task manager", keywords = ["implement", "task manager"])
    tm.add_task(task_task_manager)

    # Verify task additions
    assert tm.get_task(task_design.name).name == task_design.name

    assert tm.get_task(task_implement.name).name == task_implement.name

    assert tm.get_task(task_task_manager.name).name == task_task_manager.name

    # Add dependencies
    print("Testing adding dependencies")
    tm.add_dependency(task_task_manager, task_implement.name)

    tm.add_dependency(task_implement, task_design.name)

    print(f"Order: {tm.list_next_tasks()}")

    # Update a task
    print("Testing updating tasks")
    task_task_manager = Task("task_manager", description = "Build the task manager - Updated", keywords = ["implement", "task manager", "project"])
    assert tm.update_task(task_task_manager)

    assert tm.get_task(task_task_manager.name).description == task_task_manager.description

    # Update a non existing task
    print("Testing updating non existing task")
    task_not_existing = Task("not_existing", description = "Task does not exist")
    assert not tm.update_task(task_not_existing)

    # Delete a task
    print("Testing deleting task")
    assert tm.delete_task(task_task_manager.name)

    # Delete a non existing task
    print("Testing deleting non existing task")
    assert not tm.delete_task(task_not_existing.name)

    # Delete a task which has tasks dependent on it
    print("Testing deleting tasks which has tasks dependent on it")
    assert not tm.delete_task(task_design.name)

    # Test cyclic dependency - must fail to get an order
    print("Testing adding cyclic dependency")

    task_design = Task("design", description = "Design the data structures", keywords = ["design", "data structures"])
    tm.add_task(task_design)
    
    task_implement = Task("implement", description = "Implement the data structures", keywords = ["implement", "data structures"])
    tm.add_task(task_implement)

    task_task_manager = Task("task_manager", description = "Build the task manager", keywords = ["implement", "task manager"])
    tm.add_task(task_task_manager)

    tm.add_dependency(task_task_manager, task_implement.name)

    tm.add_dependency(task_implement, task_design.name)

    tm.add_dependency(task_design, task_implement.name)
    
    task_order = tm.list_next_tasks()
    print(f"Order: {task_order}")

    assert not task_order

    # Search of tasks based on keyword
    print("Testing search of tasks based on keyword")
    tm = TaskManager()

    task_design = Task("design", description = "Design the data structures", keywords = ["design", "data structures"])
    tm.add_task(task_design)
    
    task_implement = Task("implement", description = "Implement the data structures", keywords = ["implement", "data structures"])
    tm.add_task(task_implement)

    task_task_manager = Task("task_manager", description = "Build the task manager", keywords = ["implement", "task manager"])
    tm.add_task(task_task_manager)

    kw_tasks = tm.find_tasks_by_keyword("implement")
    assert 2 == len(kw_tasks)
    assert set(["task_manager", "implement"]).issubset(kw_tasks)

    # TODO: Select a task and mark as completed.

    # TODO: Get next task and validate

    pass

from collections import defaultdict
import graph

import trie

from enum import Enum
import heapq

class TaskStatus(Enum):

    Open = 1
    Closed = 2

# Priorities for the task
class Priority(Enum):

    High = 1
    Medium = 2
    Low = 3

class Task:

    def __init__(self, name, description = None, keywords = None, dependencies = None, priority = Priority.Medium):

        self.name = name

        self.description = description

        # Ensure it is a list
        self.keywords = keywords if keywords is not None else []

        # Remove direct mention in task, move to task manager
        # self.dependencies = dependencies

        self.priority = priority

        self.status = TaskStatus.Open

class TaskManager:

    def __init__(self):

        self.task_graph = graph.Graph()

        self.search_trie = trie.Trie()

        # Tasks by ID
        self.tasks = {}

        # Keywords to tasks
        self.keyword_tasks = defaultdict(set)
        

    def rebuild_trie(self):
        self.search_trie = trie.Trie()

        uniq_keywords = set()
        for task in self.tasks.values():
            for keyword in task.keywords:
                uniq_keywords.add(keyword.lower())

        for keyword in uniq_keywords:
            self.search_trie.insert(keyword)

    # Setup the functions that map to user actions
    def add_task(self, task):
        # Add task and add dependency if provided

        if task.name in self.tasks:
            print(f"ERROR: Task {task.name} already exists")
            return

        self.tasks[task.name] = task

        if task.keywords is None:
            task.keywords = []

        task.keywords = [keyword.lower() for keyword in task.keywords]

        for keyword in task.keywords:
            self.keyword_tasks[keyword].add(task.name)
            self.search_trie.insert(keyword)

        # print(f"Task {task.name} added")

    def get_task(self, task_name):

        return self.tasks[task_name]

    def update_task(self, task):

        has_existing_task = task.name in self.tasks
        if has_existing_task:
            existing_task = self.tasks[task.name]
            
            existing_task.description = task.description

            if task.status:
                existing_task.status = task.status

            if task.priority:
                existing_task.priority = task.priority

            if task.keywords is None:
                task.keywords = []

            # A difference and union of old an new keywords can be used to update the keywords efficiently
            old_keywords = set(keyword.lower() for keyword in existing_task.keywords)
            new_keywords = set(keyword.lower() for keyword in task.keywords)

            task.keywords = list(new_keywords)

            to_add = new_keywords - old_keywords
            to_remove = old_keywords - new_keywords
            
            for keyword in to_remove:
                self.keyword_tasks[keyword].remove(existing_task.name)
                # Delete the keyword entry if empty after removing the task
                if 0 == len(self.keyword_tasks[keyword]):
                    del self.keyword_tasks[keyword]
    
            for keyword in to_add:
                self.keyword_tasks[keyword].add(task.name)

            # Rebuild the trie
            self.rebuild_trie()
            
            # print(f"Task {task.name} updated")

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
                self.keyword_tasks[keyword].remove(existing_task.name)
                # Delete the keyword entry if empty after removing the task
                if 0 == len(self.keyword_tasks[keyword]):
                    del self.keyword_tasks[keyword]

            # Remove task from the graph
            self.task_graph.graph.pop(task_name, None)

            if task_name in self.task_graph.in_degree:
                del self.task_graph.in_degree[task_name]

            for depends in self.task_graph.graph.values():
                if task_name in depends:
                    depends.remove(task_name)
            
            # Remove from trie
            self.rebuild_trie()
            
            # print(f"Task {task_name} deleted")

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

        # As priority is included, the logic is moved here

        in_degree = self.task_graph.in_degree.copy()
        graph = self.task_graph.graph

        # Use a min-heap to store the tasks by priority
        task_heap = []

        for task_name in self.tasks:
            if in_degree[task_name] == 0:
                priority = self.tasks[task_name].priority.value
                heapq.heappush(task_heap, (priority, task_name))

        sorted_tasks = []

        while task_heap:
            priority, task = heapq.heappop(task_heap)
            sorted_tasks.append(task)

            if task in graph:
                for depends_on in graph[task]:
                    in_degree[depends_on] -= 1
                    if in_degree[depends_on] == 0:
                        nest_priority = self.tasks[depends_on].priority.value
                        heapq.heappush(task_heap, (nest_priority, depends_on))
        
        if len(sorted_tasks) == len(self.tasks):
            return sorted_tasks
        else:
            return None
            
    def find_tasks_by_keyword(self, keyword):
        return None if not keyword in self.keyword_tasks else self.keyword_tasks[keyword]

    def find_tasks_autocomplete(self, keyword_part):
        # Use the trie to find keywords that match the user input
        keywords = self.search_trie.autocomplete(keyword_part)

        tasks = set()
        # List tasks that match the keyword
        for keyword in keywords:
            tasks.update(self.keyword_tasks[keyword])

        return tasks

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
    assert tm.get_task(task_design.name).name == task_design.name, "Task design should be added"

    assert tm.get_task(task_implement.name).name == task_implement.name, "Task implement should be added"

    assert tm.get_task(task_task_manager.name).name == task_task_manager.name, "Task task manager should be added"

    # Add dependencies
    print("Testing adding dependencies")
    tm.add_dependency(task_task_manager, task_implement.name)

    tm.add_dependency(task_implement, task_design.name)

    # print(f"Order: {tm.list_next_tasks()}")

    # Get valid task order when no cycles are present
    print("Testing valid order of tasks when no cycles are present")
    assert tm.list_next_tasks(), "A valid order for tasks should be retrieved"

    # Update a task
    print("Testing updating tasks")
    task_task_manager = Task("task_manager", description = "Build the task manager - Updated", keywords = ["implement", "task manager", "project"])
    assert tm.update_task(task_task_manager), "Task should be updated"

    assert tm.get_task(task_task_manager.name).description == task_task_manager.description, "Task description should match"

    # Update a non existing task
    print("Testing updating non existing task")
    task_not_existing = Task("not_existing", description = "Task does not exist")
    assert not tm.update_task(task_not_existing), "Should not update  non existing task"

    # Delete a task
    print("Testing deleting task")
    assert tm.delete_task(task_task_manager.name), "Should delete task"

    # Delete a non existing task
    print("Testing deleting non existing task")
    assert not tm.delete_task(task_not_existing.name), "Should not delete a non existing task"

    # Delete a task which has tasks dependent on it
    print("Testing deleting tasks which has tasks dependent on it")
    assert not tm.delete_task(task_design.name), "Should not delete a task that have dependencies"

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

    assert not task_order, "No valid order should be found"

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
    assert set(["task_manager", "implement"]).issubset(kw_tasks), "Keyword search should find the right tasks"

    # Search for task by keyword
    print("Testing autocomplete of tasks based on partial keyword")
    found_tasks = tm.find_tasks_autocomplete("de")
    # print(f"Find tasks - auto complete {found_tasks}")
    assert 1 == len(found_tasks), "One task should be found"

    # Test priorities
    print("Testing priorities")
    tm = TaskManager()

    task_design = Task("design", description = "Design the data structures", keywords = ["design", "data structures"], priority = Priority.High)
    tm.add_task(task_design)
    
    task_study = Task("study", description = "Study the ask", keywords = ["study", "design"], priority = Priority.Medium)
    tm.add_task(task_study)
    
    task_user_interview = Task("user_interview", description = "Interview the users", keywords = ["interview", "design"], priority = Priority.Low)
    tm.add_task(task_user_interview)
    
    task_budget = Task("budget", description = "Define budget", keywords = ["budget"], priority = Priority.High)
    tm.add_task(task_budget)
    
    task_implement = Task("implement", description = "Implement the data structures", keywords = ["implement", "data structures"])
    tm.add_task(task_implement)

    task_task_manager = Task("task_manager", description = "Build the task manager", keywords = ["implement", "task manager"])
    tm.add_task(task_task_manager)

    tm.add_dependency(task_budget, task_study.name)

    tm.add_dependency(task_design, task_study.name)

    tm.add_dependency(task_task_manager, task_implement.name)

    tm.add_dependency(task_implement, task_design.name)
   
    task_order = tm.list_next_tasks()
    print(f"Order: {task_order}")

    assert task_order, "A valid tasks order is expected"

    assert task_user_interview.name == task_order[-1], "User interview should be the last task"

if __name__ == "__main__":

    # Run the tests
    tester()
    

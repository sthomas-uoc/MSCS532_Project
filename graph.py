from collections import defaultdict, deque

class Graph:

    def __init__(self):

        # Store the tasks and dependencies
        self.graph = defaultdict(list)

        # Tracks if a task is a dependency for others
        self.in_degree = defaultdict(int)

    def add_edge(self, task_a, task_b):

        self.graph[task_a].append(task_b)

        self.in_degree[task_b] += 1

        if task_a not in self.in_degree:
            self.in_degree[task_a] = 0

    def sort(self):
        # Return list of tasks to be completed in order

        process_queue = deque([task for task in self.in_degree if self.in_degree[task] == 0])
        sorted = []
        num_tasks = len(self.in_degree)

        while process_queue:
            task = process_queue.popleft()
            sorted.append(task)
            for depends_on in self.graph[task]:
                self.in_degree[depends_on] -= 1
                if self.in_degree[depends_on] == 0:
                    process_queue.append(depends_on)

        # If all task were added to the sorted list, then there is no cycle, else a cycle exists
        if len(sorted) == num_tasks:
            return sorted
        else:
            return None
        

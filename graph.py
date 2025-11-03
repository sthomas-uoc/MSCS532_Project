from collections import defaultdict


class Graph:

    def __init__(self):

        self.graph = defaultdict(list)

        self.in_degree = defaultdict(int)

    def add_edge(self, task_a, task_b):

        self.graph[task_a].append(task_b)

        self.in_degree[task_b] += 1

        if task_a not in self.in_degree:
            self.in_degree[task_a] = 0

    def sort(self):
        # TODO return list of tasks to be completed in order
        pass
        

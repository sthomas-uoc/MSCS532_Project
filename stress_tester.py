import time
import random
import string
import sys
from task_app import TaskManager, Task, Priority

DATASET_SIZES = [1000, 5000, 10000]
KEYWORDS_POOL = ["design", "backend", "frontend", "db", "api", "auth", "ui", "ux", "testing", "deploy"]

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length))

def run_stress_test():
    print("===================================================")
    print("Starting test")
    print("===================================================")

    results = {
        "sizes": [],
        "add_time": [],
        "dependency_time": [],
        "sort_time": [],
        "search_time": []
    }

    for size in DATASET_SIZES:
        print(f"\nTesting Dataset Size: {size} Tasks")
        tm = TaskManager()
        
        # 1. Test add
        start_time = time.time()
        tasks = []
        for i in range(size):
            # Randomly pick keywords
            kws = random.sample(KEYWORDS_POOL, k=random.randint(1, 3))
            # Randomly pick priority
            prio = random.choice(list(Priority))
            
            t = Task(f"Task_{i}", description=generate_random_string(20), keywords=kws, priority=prio)
            tm.add_task(t)
            tasks.append(t)
        
        add_duration = time.time() - start_time
        print(f"Added {size} tasks in {add_duration:.4f} seconds")

        # 2. Test dependencies
        # Create a chain to force a deep graph: 0->1->2->3...
        # Also add random dependencies to create density
        start_time = time.time()
        for i in range(size - 1):
            tm.add_dependency(tasks[i+1], tasks[i].name) # Chain
            
            # Add random edges (sparse)
            if i % 10 == 0 and i + 10 < size:
                tm.add_dependency(tasks[i+10], tasks[i].name)

        dep_duration = time.time() - start_time
        print(f"Built Graph dependencies in {dep_duration:.4f} seconds")

        # 3. Test task order
        start_time = time.time()
        order = tm.list_next_tasks()
        sort_duration = time.time() - start_time
        
        if order is None:
            print("Cycle detected during stress test (Unexpected!)")
        else:
            print(f"Topological Sort execution: {sort_duration:.4f} seconds")

        # 4. Test autocomplete
        # Search for a common prefix
        start_time = time.time()
        # "de" matches "design", "deploy", "dev", etc.
        results_trie = tm.find_tasks_autocomplete("de") 
        search_duration = time.time() - start_time
        print(f"Trie Autocomplete found {len(results_trie)} tasks in {search_duration:.6f} seconds")

        # Record metrics
        results["sizes"].append(size)
        results["add_time"].append(add_duration)
        results["dependency_time"].append(dep_duration)
        results["sort_time"].append(sort_duration)
        results["search_time"].append(search_duration)

    # report
    print("\n")
    print("===================================================")
    print("Report")
    print("===================================================")
    print(f"{'Size':<10} | {'Add (s)':<12} | {'Sort (s)':<12} | {'Search (s)':<12}")
    print("-" * 50)
    for i in range(len(results["sizes"])):
        print(f"{results['sizes'][i]:<10} | {results['add_time'][i]:<12.4f} | {results['sort_time'][i]:<12.4f} | {results['search_time'][i]:<12.6f}")

if __name__ == "__main__":
    # Increase recursion limit for deep dependency chains in large graphs
    sys.setrecursionlimit(20000)
    run_stress_test()

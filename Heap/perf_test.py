import time
import random
import matplotlib.pyplot as plt
from array_heap import ArrayMaxHeap 

def performance_test(heap, operation, stop=1000000, step=50000, order="random", visualize=True):
    sizes = []
    times = []

    for i in range((stop // step) + 1):
        num_elements = i * step
        data = generate_data(num_elements, order)

        start_time = time.time()
        for datum in data:
            element_title = datum[0]
            element_priority = datum[1]
            operation(element_title, element_priority)
        end_time = time.time()
        duration = end_time - start_time
        
        heap.clear_heap()

        times.append(duration)
        sizes.append(num_elements)

    return sizes, times


def plot_results(results, title='Performance Test', xlabel='Input Size', ylabel='Time (seconds)'):
    plt.figure()
    for branching_factor, (sizes, times) in results.items():
        plt.plot(sizes, times, marker='o', linestyle='-', label=f"B = {branching_factor}")

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend()
    plt.show()

def generate_data(num_elements, order):
    if order == "ascending":
        return [(i, i) for i in range(0, num_elements)]
    elif order == "descending":
        return [(i, i) for i in range(num_elements - 1, -1, -1)]
    elif order == "random":
        random.seed(42)
        element_title = 0
        data = []

        for i in range(num_elements):
            element_priority = random.randint(0, num_elements - 1)
            data.append((element_title, element_priority))
            element_title += 1

        return data

    else:
        raise ValueError("Order must be ascending, descending, or random")


def compare_branching_factors(branching_factors, stop=1000000, step=50000, order="random"):
    results = {}

    for branching_factor in branching_factors:
        heap = ArrayMaxHeap(branching_factor=branching_factor)  # Initialize heap with branching factor
        sizes, times = performance_test(heap, heap.insert, stop=stop, step=step, order=order, visualize=False)
        results[branching_factor] = (sizes, times)

    plot_results(results, title='Performance Comparison of Different Branching Factors')


branching_factors = [2, 4, 8, 16]  
compare_branching_factors(branching_factors, stop=500000, step=50000, order="random")

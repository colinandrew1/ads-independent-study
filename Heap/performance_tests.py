import time
import random
import matplotlib.pyplot as plt
from array_heap import ArrayMaxHeap



def performace_test(operation, stop = 1000000, step=50000, order = "random", visualize=True):
    start = step
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
        end_time=time.time()
        duration = end_time - start_time
        heap.clear_heap()

        times.append(duration)
        sizes.append(num_elements)



    if visualize==True:
        plot_results(sizes, times)
    return sizes, times
    

def plot_results(sizes, times, title='Performance Test', xlabel='Input Size', ylabel='Time (seconds)'):
    plt.figure()
    plt.plot(sizes, times, marker='o', linestyle='-', color='b', label="Execution Time")
    plt.title = title
    plt.xlabel = xlabel
    plt.ylabel = ylabel
    plt.grid()
    plt.legend()
    plt.show()


# returns data as a list -- ie tuples
def generate_data(num_elements, order):
    if order == "ascending":
        return [(i,i) for i in range(0,num_elements)]
    elif order == "descending":
        return [(i,i) for i in range(num_elements-1, -1, -1)]
    elif order == "random":
        random.seed(42)
        element_title = 0
        data = []
        
        for i in range(num_elements):
            element_priority = random.randint(0, num_elements-1)
            data.append((element_title, element_priority))
            element_title += 1 
        
        return data
        
    else: 
        raise ValueError("Order must be ascending, descending, or random")

# sample call to performance_test
heap = ArrayMaxHeap()
performace_test(heap.insert, stop = 1000000, step=50000, order="random", visualize = True)
# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 1/30/2025
# Description: Array implementation of a Max Heap based on the description from Advanced Algorithms and Data Structures by Marello La Roca
# -----------------------------------------------------------------------------

import random
import time


"""
    A class to represent a max heap data structure.
    The heap is conceptually a complete tree with a Python list as the underlying representation
    List stores (element, priority) pairs

    This class provides basic heap operations like insertion, removal as well as update.
    
    Time complexities:
        - Peek: O(1)
        - Top, Insert, Update: O(log n) (amortized) 
    
    Attributes:
        branching_factor (int): The branching factor of the heap (default is 2).
        maintain_map (bool): Whether to maintain an additional map alongside the heap (default is False).
    """
class ArrayMaxHeap:
    def __init__(self, branching_factor=2):
        self.d = branching_factor
        self.elements = []  # underyling data model is a Python list
        self.index_map = {} # mapping from element to its index within the array
    

    # User facing methods: top, insert, delete, peek, size, contains

    """
    Returns the element with the highest priority and removes it from the heap
    """
    def top(self):
        if len(self.elements) == 0:  # Check if heap is empty
            raise IndexError("Heap is empty")

        old_root = self.elements[0]
        del self.index_map[old_root[0]]
        
        if len(self.elements) == 1:
            return self.elements.pop()[0]
        
        last_element = self.elements.pop()  
        self.elements[0] = last_element # move the last element to the root
        self.index_map[last_element[0]] = 0 # update index map
        self._push_down(0)
        
        return old_root[0]  # Return the old root's title (not priority)

        
    """
    Inserts a new element-priority pair into the heap at the appropriate position

    Args:
        element_title (Any): The title of the element to insert
        element_priority (int): The priority of the element to be inserted
    """
    def insert(self, element_title, element_priority):
        if (element_title in self.index_map):
            raise KeyError("Duplicate elements not allowed")
        new_element = (element_title, element_priority)
        self.elements.append(new_element)   # add new element to end of array
        self.index_map[element_title] = len(self.elements)-1  # add new entry to map
        self._bubble_up(len(self.elements)-1)    # updates to index map will occur in bubble_up()


    """
    updates an the priority of an elemnt within the heap

    Args:
        element: The element whose priority is to be updated
        new_priority (int): The new priority of the element
    """
    def update(self, element, new_priority):
        if element not in self.index_map:   
            raise KeyError("Element does not exist within heap")
        
        cur_idx = self.index_map[element]   # O(log n) runtime of update relies on obtaining index in constant time, otherwise linear
        old_priority = self.elements[cur_idx][1]
        self.elements[cur_idx] = (element, new_priority)    # update the priority of the element - heap is potentially violating constraints

        # update position within heap as necessary
        if new_priority > old_priority:
            self._bubble_up(cur_idx)
        elif old_priority > new_priority:
            self._push_down(cur_idx)
            

    """
    Removes the specified element from the heap

    Args:
        element: The element to update
    """
    def delete(self, element_title):
        if element_title not in self.index_map:
            raise KeyError("Element does not exist within heap")

        cur_idx = self.index_map[element_title]
        last_element  = self.elements.pop()
        del self.index_map[element_title]

        if cur_idx < len(self.elements):    # only need to rebalance if deleted element was not at end
            self.elements[cur_idx] = last_element   # store last element at current index
            self.index_map[last_element[0]] = cur_idx
            self._push_down(cur_idx)  # then push down the heap as necessary


    """
    Returns the element with the highest priority without removing it
    """
    def peek(self):
        if len(self.elements) == 0:  # Check if heap is empty
            raise IndexError("Heap is empty")
        return self.elements[0][0]
    

    """
    Returns the number of elements in the heap
    """
    def size(self):
        return len(self.elements)
    

    def get_element_priority(self, element_title):
        if element_title not in self.index_map:
            raise IndexError("Element does not exist within heap")
        return self.elements[self._get_index(element_title)][1]

    """
    Returns true if the element is in the heap, false otherwise

    Args:
        element: The element to search for
    """
    def contains(self, element):
        return element in self.index_map


    def is_empty(self):
        if len(self.elements) == 0:
            return True
        else:
            return False


    def clear_heap(self):
        self.elements = []
        self.index_map = {}


    def is_valid(self):
        cur_idx = 0 # start at root
        first_leaf_idx = self._first_leaf_index()    # leaves will be checked via their parents
        while cur_idx < first_leaf_idx: # traversing down the tree, verifying valid subtrees
            cur_priority = self.elements[cur_idx][1]
            first_child_idx = self._first_child_index(cur_idx)
            last_child_idx = min(first_child_idx + self.d, len(self.elements))
            for child_idx in range(first_child_idx, last_child_idx):    # for each node in the tree:
                if cur_priority < self.elements[child_idx][1]:              # check that its priority is greater than its children
                    return False
            cur_idx += 1    
        return True

    # Internal methods used as helper functions

    """
    Moves element in question up the tree to its appropriate position

    Args:
        element_idx: The index of the element to move
    """
    def _bubble_up(self, element_idx):
        element = self.elements[element_idx]    # element that is moving
        while (element_idx > 0):    # make sure we dont go past root
            parent_idx = self._parent_index(element_idx)
            if self.elements[parent_idx][1] < element[1]:
                self.elements[element_idx] = self.elements[parent_idx]  # move parent down by one level
                self.index_map[self.elements[parent_idx][0]] = element_idx # maintain the element-index mapping (update parents index)
                element_idx = parent_idx    # move up one layer
            else:
                break   # we have found correct index/position within the heap
        self.elements[element_idx] = element
        self.index_map[element[0]] = element_idx
        

    """
    Moves element in question down the tree to its appropriate position

    Args:
        element_idx: The index of the element to move
    """
    def _push_down(self, element_idx):
        element = self.elements[element_idx]    # element that is moving down the tree
        while (element_idx < self._first_leaf_index()):    # make sure we dont go past leaves
            child_idx = self._highest_priority_child_index(element_idx)
            child = self.elements[child_idx]
            if child[1] > element[1]:
                self.elements[element_idx] = self.elements[child_idx]  # move parent down by one level
                self.index_map[self.elements[child_idx][0]] = element_idx   # Doesn't matter which parent location we use because key is string
                element_idx = child_idx    # move down one layer
            else:
                break   # we have found correct index
        self.elements[element_idx] = element
        self.index_map[element[0]] = element_idx
    

    def _first_child_index(self, index):
        return index * self.d + 1
    

    def _parent_index(self, index):
        return (index - 1) // self.d
    

    def _first_leaf_index(self):
        return (len(self.elements) - 2) // self.d + 1
    

    def _highest_priority_child_index(self, index):
        start_idx = self._first_child_index(index)
        size = len(self.elements)
        end_idx = min(start_idx + self.d, size)

        if start_idx >= size:
            return None

        highest_priority = -float('inf')    # smallest possible value

        idx = start_idx
        for i in range(start_idx, end_idx):
            if self.elements[i][1] > highest_priority:
                highest_priority = self.elements[i][1]
                idx = i

        return idx
    

    def _get_index(self, element_title):
        return self.index_map[element_title]


    def benchmark_insert(self, num_elements, seed=0):
        rng = random.Random(seed)
        self.clear_heap()

        start_time = time.perf_counter()
        for i in range(num_elements):
            self.insert(i, rng.randint(0, num_elements))
        end_time = time.perf_counter()

        return end_time - start_time
    

    def benchmark_delete(self, num_elements, seed=0):
        rng = random.Random(seed)
        self.clear_heap()

        for i in range(num_elements):
            self.insert(i, rng.randint(0, num_elements))

        start_time = time.perf_counter()
        while not self.is_empty():
            self.top()
        end_time = time.perf_counter()

        return end_time - start_time





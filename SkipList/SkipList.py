# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 2/25/25
# Description: Implementation of a Skip List based on Skip Lists: A Probabilistic Alternative to Balanced Trees by William Pugh
# -----------------------------------------------------------------------------

import time
import random
import sys  # used for header key -- must be larger than any legal key

class SkipListNode:
    def __init__(self, key, value, level):
        self.key:int = key
        self.value = value
        self.forward:list = [None] * level
    

    def __repr__(self):
        node_string = ""
        if self.key == sys.maxsize:
            node_string += f"Header, "
        else:
            node_string += f"(key = {self.key}, "
        node_string += f"value = {self.value}, forward = {self.forward})"
        return node_string
        

class SkipList:
    def __init__(self, max_level = 4, p = 1/2):
        if max_level < 1:
            raise ValueError("Max level must be at least 1 for traditional linked list")
        self.max_level = max_level
        self.cur_level = 1
        self.p = p
        self.header = SkipListNode(sys.maxsize, None, max_level)    # header has max_level # of pointers

    def random_level(self)->int:
        level = 1
        while random.random() < self.p and level < self.max_level:  # basic probability function
            level += 1
        return level
    

    def search(self, search_key:int)->SkipListNode:
        cur_node = self.header
        for level in range(self.cur_level-1, -1, -1):
            while (cur_node.forward[level] is not None) and (cur_node.forward[level].key < search_key): 
                cur_node = cur_node.forward[level]
        cur_node = cur_node.forward[0]  # we stop right before the node we are searching for. We always reach a node via a level 1 forward pointer

        if cur_node is not None and cur_node.key == search_key:  # possible that cur_node not == search key
            return cur_node.value
        else:
            return None # search_key is not present within the list
        

    def insert(self, search_key: int, new_value):
        update = [None] * self.max_level
        cur_node = self.header

        for level in range(self.cur_level - 1, -1, -1):
            while (cur_node.forward[level] is not None) and \
                (cur_node.forward[level].key < search_key):
                cur_node = cur_node.forward[level]
            update[level] = cur_node

        cur_node = cur_node.forward[0]

        if cur_node is not None and cur_node.key == search_key:
            cur_node.value = new_value
            return

        new_node_level = self.random_level()
        new_node = SkipListNode(search_key, new_value, new_node_level)

        if new_node_level > self.cur_level:
            for i in range(self.cur_level, new_node_level):
                update[i] = self.header
            self.cur_level = new_node_level

        for level in range(new_node_level):
            new_node.forward[level] = update[level].forward[level]
            update[level].forward[level] = new_node

        
    def delete(self, search_key):
        update = [None] * self.max_level
        cur_node = self.header

        for level in range(self.cur_level - 1, -1, -1):
            while (cur_node.forward[level] is not None) and (cur_node.forward[level].key < search_key):
                cur_node = cur_node.forward[level]
            update[level] = cur_node
        cur_node = cur_node.forward[0]

        if cur_node is not None and cur_node.key == search_key:
            node_level = len(cur_node.forward)
            for level in range(node_level): # rewire forward pointers
                if update[level].forward[level] == cur_node:
                    update[level].forward[level] = cur_node.forward[level]
            # decrease list level if highest level becomes empty
            while self.cur_level > 1 and self.header.forward[self.cur_level - 1] is None:
                self.cur_level -= 1


    def is_empty(self):
        for level in range(self.max_level-1, -1, -1):
            if self.header.forward[level] is not None:
                return False
        return True


    def __repr__(self):
        list_string = "\n"
        for level in range(self.max_level-1, -1, -1):
            cur_node = self.header.forward[level]
            level_string = f"{level+1}|-->"
            while cur_node is not None:
                node_string = f"({cur_node.key})-->"
                level_string += node_string
                cur_node = cur_node.forward[level]
            level_string += "NULL\n"
            list_string += level_string
        return list_string

            
    def is_valid(self):
        for level in range(self.cur_level-1, -1, -1):
            cur_node = self.header.forward[level]
            while (cur_node is not None):
                if (cur_node != self.header) and (cur_node.forward[level] is not None) and (cur_node.key > cur_node.forward[level].key):
                    return False
                cur_node = cur_node.forward[level]
        return True


    def benchmark_insert(self, size, seed=0):
        rng = random.Random(seed)
        keys = rng.sample(range(size * 10), size)

        start = time.perf_counter()
        for k in keys:
            self.insert(k, k)
        return time.perf_counter() - start
    

    def benchmark_delete(self, size, seed=0):
        rng = random.Random(seed)
        keys = rng.sample(range(size * 10), size)

        for k in keys:
            self.insert(k, k)

        start = time.perf_counter()
        for k in keys:
            self.delete(k)  
        return time.perf_counter() - start


    def benchmark_search(self, size, seed=0):
        rng = random.Random(seed)
        keys = rng.sample(range(size * 10), size)

        for k in keys:
            self.insert(k, k)

        start = time.perf_counter()
        for k in keys:
            self.search(k)  
        return time.perf_counter() - start

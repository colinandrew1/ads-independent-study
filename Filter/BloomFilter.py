# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 4/17/2025
# Description: Implementation of a Bloom Filter
# -----------------------------------------------------------------------------

from bitarray import bitarray
import math
import mmh3 # provides "a set of fast and robust non-cryptographic hash functions"
import random
import time

class BloomFilter():
    def __init__(self, max_num_items=50, false_positive_rate=.05):
        self.max_num_items = max_num_items
        self.size = int(-((max_num_items * math.log(false_positive_rate)) / (math.log(2) ** 2)))
        self.num_hashes = int((self.size/max_num_items) * math.log(2))  # optimum number of hash functions
        self.bit_array = bitarray(self.size) # declare a bit array with the size given by the function
        self.bit_array.setall(0) # initialize all indices of the bit array to 0
        

    def contains(self, key):
        # if all indices are set to 1 return true, else false
        for i in range(self.num_hashes):
            index = mmh3.hash(key, i) % self.size   # hash the key to indices of the bit array
            if self.bit_array[index] == 0:
                return False    # key is definitely not present
        return True    # key is most likely present

    
    def insert(self, key):
        # hash the key to indices of the bit array
        # set each of the indices to 1
        for i in range(self.num_hashes):
           index = mmh3.hash(key, i) % self.size
           self.bit_array[index] = 1


    def benchmark_insert(self, n, seed=0):
        rng = random.Random(seed)
        keys = rng.sample(range(n * 10), n)

        start = time.perf_counter()
        for k in keys:
            self.insert(str(k))
        return time.perf_counter() - start
    

    def benchmark_query(self, n, seed=0):
        rng = random.Random(seed)
        keys = rng.sample(range(n * 10), n)

        # preload filter
        for k in keys:
            self.insert(str(k))

        start = time.perf_counter()
        for k in keys:
            self.contains(str(k))
        return time.perf_counter() - start
    

    def benchmark_false_positive_rate(self, n, num_queries=10000, seed=0):
        rng = random.Random(seed)
        
        inserted = rng.sample(range(n * 10), n)
        queries = rng.sample(range(n * 20, n * 30), num_queries)

        for k in inserted:
            self.insert(str(k))

        false_positives = 0
        for q in queries:
            if self.contains(str(q)):
                false_positives += 1

        return false_positives / num_queries
    

    def benchmark_load_fpr(self, load_factor, num_queries=10000, seed=0):
        rng = random.Random(seed)
        n = int(self.max_num_items * load_factor) 

        inserted = rng.sample(range(n * 10), n)
        queries = rng.sample(range(n * 20, n * 30), num_queries)

        for k in inserted:
            self.insert(str(k))

        false_positives = sum(self.contains(str(q)) for q in queries)
        return false_positives / num_queries


# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 4/17/2025
# Description: Implementation of a Bloom Filter
# -----------------------------------------------------------------------------

from bitarray import bitarray
import math
import mmh3 # provides "a set of fast and robust non-cryptographic hash functions"

class BloomFilter():
    def __init__(self, max_num_items=50, false_positive_rate=.05):
        self.size = int(-((max_num_items * math.log(false_positive_rate)) / (math.log(2) ** 2)))
        self.num_hashes = int((self.size/max_num_items) * math.log(2))  # optimum number of hash functions
        self.bit_array = bitarray(self.size) # declare a bit array with the size given by the function
        self.bit_array.setall(0) # initialize all indices of the bit array to 0
        

    def contains(self, key):
        # hash the key to indices of the bit array
        # if all indices are set to 1 return true, else false
        for i in range(self.num_hashes):
            index = mmh3.hash(key, i) % self.size
            if self.bit_array[index] == 0:
                return False    # key is definitely not present
        return True    # key is most likely present

    
    def insert(self, key):
        # hash the key to indices of the bit array
        # set each of the indices to 1
        # increment num_elements
        for i in range(self.num_hashes):
           index = mmh3.hash(key, i) % self.size
           self.bit_array[index] = 1


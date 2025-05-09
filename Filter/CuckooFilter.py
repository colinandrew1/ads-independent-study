# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 4/21/2025
# Description: Implementation of a Cuckoo Filter
# -----------------------------------------------------------------------------

from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba
import math
import mmh3 # provides "a set of fast and robust non-cryptographic hash functions"
import random


class CuckooFilter():
    def __init__(self, target_fp_rate, max_num_elements, bucket_size=4):
        self.bucket_size = bucket_size  # default bucket size is 4, suitable for most applications according to paper
        self.max_num_elements = max_num_elements
        self.load_factor = .95  # corresponds to the bucket size of 4 but can be changed, see paper for details
        self.num_buckets = math.ceil(max_num_elements / (self.load_factor * bucket_size))
        self.num_buckets = 1 << (self.num_buckets - 1).bit_length()
        self.fp_size = math.ceil(math.log2(1/target_fp_rate) + math.log2(2 * bucket_size))  # details in paper
        total_bits = self.num_buckets * self.bucket_size * self.fp_size
        self.table = bitarray(total_bits)
        self.table.setall(0)


    def insert(self, key):
        location1 = self.index(key) # returns the index of a bucket
        fingerprint = self.fingerprint(key)
        location2 = self.alt_index(fingerprint, location1)  # returns the index of a bucket
        for bucket in (location1, location2):
            empty_entry = self.find_empty_entry(bucket)
            if empty_entry is not None:
                self.write_entry(bucket, empty_entry, fingerprint)
                return True
        bucket = random.choice([location1, location2]) # randomly choose to evict a 'victim' fingerprint from one of the buckets
        max_num_kicks = 500
        for i in range(max_num_kicks):
            entry = random.randrange(self.bucket_size)  # chose a random entry within the bucket to evict
            victim_fingerprint = self.read_entry(bucket, entry)
            self.write_entry(bucket, entry, fingerprint)    # overwrite the victim fp
            fingerprint = victim_fingerprint    # we now have to find a home for the evicted victim
            bucket = self.alt_index(victim_fingerprint, bucket)
            empty_entry = self.find_empty_entry(bucket)
            if empty_entry is not None:
                self.write_entry(bucket, empty_entry, fingerprint)
                return True
        return False    # a complete rehash is required with new functions   


    def contains(self, key):
        location1 = self.index(key) # returns the index of a bucket
        fingerprint = self.fingerprint(key)
        location2 = self.alt_index(fingerprint, location1)  # returns the index of a bucket
        if self.find_entry(location1, fingerprint) is not None or self.find_entry(location2, fingerprint) is not None: return True
        else: return False


    def delete(self, key):
        location1 = self.index(key) # returns the index of a bucket
        fingerprint = self.fingerprint(key)
        location2 = self.alt_index(fingerprint, location1)  # returns the index of a bucket
        for bucket in (location1, location2):
            entry = self.find_entry(bucket, fingerprint)
            if entry is not None:
                self.write_entry(bucket, entry, 0)  # set the entry in the given bucket to 0
                return True
        return False


    def read_entry(self, bucket_idx, entry_idx):
        bucket_start = bucket_idx * self.bucket_size * self.fp_size
        start = bucket_start + (entry_idx * self.fp_size)
        end = start + self.fp_size
        bits = self.table[start:end]
        return ba2int(bits) # converts bit array to integer
    

    def write_entry(self, bucket_idx, entry_idx, fingerprint):
        bucket_start = bucket_idx * self.bucket_size * self.fp_size
        start = bucket_start + (entry_idx * self.fp_size)
        end = start + self.fp_size
        bits = fp_bits = int2ba(fingerprint, self.fp_size, 'big')
        self.table[start:end] = bits
        

    def find_empty_entry(self, bucket_idx):
        for i in range(self.bucket_size):
            if self.read_entry(bucket_idx, i) == 0:
                return i
        return None


    def find_entry(self, bucket_idx, fingerprint):   # retuns the index of given fingerprint (within a bucket) if it exists within the given bucket
        for i in range(self.bucket_size):
            if self.read_entry(bucket_idx, i) == fingerprint:
                return i
        return None


    def get_lower_bits(self, num):
        mask = (1 << self.fp_size) - 1
        return num & mask


    def fingerprint(self, key):
        key_hash =  mmh3.hash(key, 0, False)
        fingerprint = self.get_lower_bits(key_hash) # return the relevant lower bits specified by self.fp_size
        return fingerprint if fingerprint != 0 else 1


    def index(self, key):
        return mmh3.hash(key, 1, False) % self.num_buckets
    

    def alt_index(self, fingerprint, bucket_idx):
        hashed_fp = mmh3.hash(str(fingerprint), 2, False)
        return (bucket_idx ^ hashed_fp) % self.num_buckets
    

    def print_table(self):
        print(self.table)
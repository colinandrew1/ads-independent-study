from BloomFilter import BloomFilter
import random
import string

def gen_random_key(len=8):
    return ''.join(random.choices(string.ascii_lowercase, k=len))


n = 20
p = 0.05
bloom_filter = BloomFilter(n,p)

member_keys_set = set()
while len(member_keys_set) < n:
    member_keys_set.add(gen_random_key(6))
member_keys = list(member_keys_set)

num_non_member_keys = 1000
non_member_keys_set = set()
while len(non_member_keys_set) < num_non_member_keys:
    key = gen_random_key(6)
    if key not in member_keys_set:
        non_member_keys_set.add(gen_random_key(6))
non_member_keys = list(non_member_keys_set)

for key in member_keys:
    bloom_filter.insert(key)

num_false_negatives = 0
for key in member_keys:
    if not bloom_filter.contains(key):
        num_false_negatives += 1


num_false_positives = 0
for key in non_member_keys:
    if bloom_filter.contains(key):
        num_false_positives += 1

print("Number of False Negatives:", num_false_negatives)
print("Number of False Positives:", num_false_positives)
print("False Positive Rate =", num_false_positives/num_non_member_keys)

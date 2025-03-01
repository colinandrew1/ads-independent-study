import random

print(random.random())

print(1/2)

update = [1,2,3]
cur_level = len(update) + 1
node_level = 4
print(update)
update.extend([None for i in range(cur_level, node_level+1)])
print(update)

max_level = 5
for level in range(max_level-1, 0-1, -1):
    print(level, end=",")
print()


import sys
print(sys.maxsize)
print(sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize * sys.maxsize)

# results in an index error
# list = []
# list[0] = 1

list = [None] * 4
list[0] = 1

print(list)

string = "abc"
string += "def"
print(string)
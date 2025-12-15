import pytest
from SkipList import SkipListNode, SkipList



def test_empty_list():
    list = SkipList(max_level=3, p=1/2)
    assert list.cur_level == 1
    assert len(list.header.forward) == 3


def test_is_empty():
    list = SkipList(3, 1/2)
    assert list.is_empty()

    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(1, 1, 1) 
    list.header.forward[1] = node_a
    assert list.is_empty() == False

    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(2, 1, 1) 
    list.header.forward[1] = node_a
    assert list.is_empty() == False


def test_search_one_element_level_1_list():
    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(1, 1, 1)    # single level 1 node
    list.header.forward[0] = node_a
    assert list.search(1) == 1


def test_search_two_element_level_1_list():
    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(1, 2, 1)    # level 1 node
    node_b = SkipListNode(2, 2, 1)    # level 1 node

    list.header.forward[0] = node_a
    list.header.forward[0].forward[0] = node_b

    assert list.search(2) == 2


def test_search_three_element_level_1_list():
    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(1, 1, 1)    # level 1 node
    node_b = SkipListNode(2, 2, 1)    # level 1 node
    node_c = SkipListNode(3, 3, 1)    # level 1 node

    list.header.forward[0] = node_a
    list.header.forward[0].forward[0] = node_b
    list.header.forward[0].forward[0].forward[0] = node_c

    assert list.search(3) == 3


def test_non_existant_element_level_1_list():
    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(1, 1, 1)    # level 1 node
    node_b = SkipListNode(2, 2, 1)    # level 1 node
    node_c = SkipListNode(3, 3, 1)    # level 1 node

    list.header.forward[0] = node_a
    node_a.forward[0] = node_b
    node_b.forward[0] = node_c

    assert list.search(4) == None


def test_is_valid_positive():
    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(0, 1, 1)    # level 1 node
    node_b = SkipListNode(0, 2, 2)    # level 2 node
    node_c = SkipListNode(0, 3, 3)    # level 3 node
    list.header.forward[0] = node_a
    list.header.forward[1] = node_b
    list.header.forward[2] = node_c

    level_inserts = 10
    for level in range(0, list.max_level):
        cur_node = list.header.forward[level]
        for i in range(1, level_inserts+1):
            new_node = SkipListNode(i,i,level+1)
            cur_node.forward[level] = new_node
            cur_node = new_node
    assert list.is_valid()


def test_is_valid_negative():
    list = SkipList(max_level=3, p=1/2)
    node_a = SkipListNode(0, 1, 1)    # level 1 node
    node_b = SkipListNode(0, 2, 2)    # level 2 node
    node_c = SkipListNode(0, 3, 3)    # level 3 node
    list.header.forward[0] = node_a
    list.header.forward[1] = node_b
    list.header.forward[2] = node_c
    list.cur_level = 3  # have to set manually because cur_level only gets set in insert()

    level_inserts = 10
    for level in range(0, list.max_level):
        cur_node = list.header.forward[level]
        for i in range(1, level_inserts+1):
            if i == 8 and level == 1:
                new_node = SkipListNode(20,20,level+1)
            else:
                new_node = SkipListNode(i,i,level+1)
            cur_node.forward[level] = new_node
            cur_node = new_node
    assert list.is_valid() == False


def test_insert():
    list = SkipList(max_level=3, p=1/2)
    num_inserts = 5
    for i in range(num_inserts):
        list.insert(i,i)
    assert list.is_valid()
    print(list)
    # assert True == False


def test_delete():
    list = SkipList(max_level=3, p=1/2)
    num_inserts = 5
    for i in range(num_inserts):
        list.insert(i,i)
    assert list.is_valid()
    print(list)

    print("Deleting 3")
    list.delete(3)
    print(list)
    assert list.search(3) == None
    assert list.is_valid()

    print("Deleting 1")
    list.delete(1)
    print(list)
    assert list.search(1) == None
    assert list.is_valid()


    print("Deleting 0")
    list.delete(0)
    print(list)
    assert list.search(0) == None
    assert list.is_valid()


    print("Deleting 2")
    list.delete(2)
    print(list)
    assert list.search(2) == None
    assert list.is_valid()


    print("Deleting 4")
    list.delete(4)
    print(list)
    assert list.search(4) == None
    assert list.is_valid()

    # assert True == False


import pytest
import random
from linked_heap import ArrayMaxHeap, HeapObject

# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 1/30/2025
# Description: Unit tests for linked 3-ary max heap implementation
# -----------------------------------------------------------------------------


def test_is_valid_iterative():
    # Assume ArrayMaxHeap and HeapObject are defined elsewhere,
# and that ArrayMaxHeap(3) creates a 3‑ary (ternary) max‑heap.

    heap = ArrayMaxHeap(3)

    # Case: Empty heap
    assert heap.is_valid()

    # Case: Single element (root only)
    heap.root = HeapObject('a', 10)
    heap.num_elements = 1
    assert heap.is_valid()

    # Case: Valid max‑heap with two elements (root with one child)
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 5)
    heap.root._children = [b]  # Only one child (allowed in a 3‑ary heap)
    b._parent = heap.root
    heap.num_elements = 2
    assert heap.is_valid()

    # Case: Valid max‑heap with three elements (root with two children)
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 8)
    c = HeapObject('c', 7)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    heap.num_elements = 3
    assert heap.is_valid()

    # Case: Valid max‑heap with four elements (root with three children)
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 9)
    c = HeapObject('c', 8)
    d = HeapObject('d', 7)
    heap.root._children = [b, c, d]
    b._parent = heap.root
    c._parent = heap.root
    d._parent = heap.root
    heap.num_elements = 4
    assert heap.is_valid()

    # Case: Invalid heap where parent is smaller than its child
    heap.root = HeapObject('a', 5)
    b = HeapObject('b', 10)  # b > a: violates max‑heap property
    heap.root._children = [b]
    b._parent = heap.root
    heap.num_elements = 2
    assert heap.is_valid() == False

    # Case: Invalid heap where a second‑level element is greater than the root
    heap.root = HeapObject('a', 5)
    b = HeapObject('b', 8)
    c = HeapObject('c', 6)
    d = HeapObject('d', 9)  # d is a child of b, but 9 > 5 (root)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    b._children = [d]
    d._parent = b
    heap.num_elements = 4
    assert heap.is_valid() == False

    # Case: Valid max‑heap with multiple levels
    # Structure:
    #         e (50)
    #       /   |   \
    #    d(40) c(30) b(20)
    #     /
    #  a (10)
    heap.root = HeapObject('e', 50)
    b = HeapObject('d', 40)
    c = HeapObject('c', 30)
    d = HeapObject('b', 20)
    e = HeapObject('a', 10)
    heap.root._children = [b, c, d]
    b._parent = heap.root
    c._parent = heap.root
    d._parent = heap.root
    # Let the first child have one child:
    b._children = [e]
    e._parent = b
    heap.num_elements = 5
    assert heap.is_valid()

    # Case: Invalid heap where the first child is greater than the root
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 20)  # b > a
    c = HeapObject('c', 5)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    heap.num_elements = 3
    assert heap.is_valid() == False

    # Case: Valid heap with duplicate values
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 10)
    c = HeapObject('c', 10)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    heap.num_elements = 3
    assert heap.is_valid()

    # Case: Large heap, valid max‑heap structure
    # Structure (ternary distribution):
    #              a (100)
    #         /       |       \
    #      b (90)   c (80)    d (70)
    #     / | \      / | \
    #  e(60) f(50) g(40) h(30) i(20) j(10)
    heap.root = HeapObject('a', 100)
    b = HeapObject('b', 90)
    c = HeapObject('c', 80)
    d = HeapObject('d', 70)
    e = HeapObject('e', 60)
    f = HeapObject('f', 50)
    g = HeapObject('g', 40)
    h = HeapObject('h', 30)
    i = HeapObject('i', 20)
    j = HeapObject('j', 10)
    heap.root._children = [b, c, d]
    b._parent = heap.root
    c._parent = heap.root
    d._parent = heap.root
    b._children = [e, f, g]
    e._parent = b
    f._parent = b
    g._parent = b
    c._children = [h, i, j]
    h._parent = c
    i._parent = c
    j._parent = c
    heap.num_elements = 10
    assert heap.is_valid()

    # Case: Large heap, invalid structure (one child breaks the max‑heap property)
    heap.root = HeapObject('a', 100)
    b = HeapObject('b', 90)
    c = HeapObject('c', 80)
    d = HeapObject('d', 70)
    e = HeapObject('e', 60)
    f = HeapObject('f', 110)  # f > 90, violates the property in b's subtree
    g = HeapObject('g', 40)
    h = HeapObject('h', 30)
    i = HeapObject('i', 20)
    j = HeapObject('j', 10)
    heap.root._children = [b, c, d]
    b._parent = heap.root
    c._parent = heap.root
    d._parent = heap.root
    b._children = [e, f, g]
    e._parent = b
    f._parent = b
    g._parent = b
    c._children = [h, i, j]
    h._parent = c
    i._parent = c
    j._parent = c
    heap.num_elements = 10
    assert heap.is_valid() == False

    # Case: Valid heap with edge case values (zeroes and negatives)
    heap.root = HeapObject('a', 0)
    b = HeapObject('b', -1)
    c = HeapObject('c', -2)
    d = HeapObject('d', -3)
    heap.root._children = [b, c, d]
    b._parent = heap.root
    c._parent = heap.root
    d._parent = heap.root
    heap.num_elements = 4
    assert heap.is_valid()

    # Case: Invalid heap with negative values (root is smaller than a child)
    heap.root = HeapObject('a', -3)
    b = HeapObject('b', -1)  # b > a (i.e. -1 > -3)
    c = HeapObject('c', -2)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    heap.num_elements = 3
    assert heap.is_valid() == False


def test_is_empty():
    heap = ArrayMaxHeap(3)
    assert heap.is_valid()
    assert heap.size() == 0
    assert heap.is_empty()

    heap.insert('a', 1)
    assert not heap.is_empty()
    assert heap.is_valid()

    heap.delete('a')
    assert heap.is_empty()
    assert heap.is_valid()


# def test_contains():
#     heap = ArrayMaxHeap(3)
#     heap.insert('a',1)
#     heap.insert('b',2)
#     heap.insert('c',3)
#     heap.insert('d',4)
#     heap.insert('e',5)

#     assert heap.contains('a')
#     assert heap.contains('b')
#     assert heap.contains('c')
#     assert heap.contains('d')
#     assert heap.contains('e')

#     assert not heap.contains('f')
#     assert not heap.contains('g')
#     assert not heap.contains('h')

#     heap.insert('f', 2)
#     assert heap.contains('f')

#     heap.delete('d')
#     assert not heap.contains('d')

#     assert heap.contains('a')
#     assert heap.contains('b')
#     assert heap.contains('c')
#     assert heap.contains('e')
#     assert heap.contains('f')


def test_calculate_height_binary():
    heap = ArrayMaxHeap(2)
    assert heap._calculate_height(0) == 0
    assert heap._calculate_height(1) == 0
    
    assert heap._calculate_height(2) == 1
    assert heap._calculate_height(3) == 1

    for i in range (4, 8):
        assert heap._calculate_height(i) == 2

    for i in range (8, 16):
        assert heap._calculate_height(i) == 3

    for i in range (16, 32):
        assert heap._calculate_height(i) == 4

    for i in range (32, 64):
        assert heap._calculate_height(i) == 5

    for i in range (64, 128):
        assert heap._calculate_height(i) == 6

    for i in range (128, 256):
        assert heap._calculate_height(i) == 7


def test_calculate_height_ternary():
    heap = ArrayMaxHeap(3)
    assert heap._calculate_height(0) == 0
    assert heap._calculate_height(1) == 0

    assert heap._calculate_height(2) == 1
    assert heap._calculate_height(3) == 1
    assert heap._calculate_height(4) == 1

    for i in range (5, 14):
        assert heap._calculate_height(i) == 2

    for i in range (14, 41):
        assert heap._calculate_height(i) == 3

    for i in range (41, 122):
        assert heap._calculate_height(i) == 4

    for i in range (122, 365):
        assert heap._calculate_height(i) == 5

    for i in range (365, 1094):
        assert heap._calculate_height(i) == 6


def test_calculate_height_quaternary():
    heap = ArrayMaxHeap(4)
    assert heap._calculate_height(0) == 0
    assert heap._calculate_height(1) == 0

    assert heap._calculate_height(2) == 1
    assert heap._calculate_height(3) == 1
    assert heap._calculate_height(4) == 1
    assert heap._calculate_height(5) == 1

    for i in range (6, 22):
        assert heap._calculate_height(i) == 2

    for i in range (22, 86):
        assert heap._calculate_height(i) == 3

    for i in range (86, 342):
        assert heap._calculate_height(i) == 4

    for i in range (342, 1366):
        assert heap._calculate_height(i) == 5

    for i in range (1366, 5462):
        assert heap._calculate_height(i) == 6


def test_convert_to_base():
    heap = ArrayMaxHeap()

    assert heap._convert_to_base(2, 0) == '0'
    assert heap._convert_to_base(2, 1) == '1'
    assert heap._convert_to_base(2, 2) == '10'
    assert heap._convert_to_base(2, 3) == '11'
    assert heap._convert_to_base(2, 4) == '100'
    assert heap._convert_to_base(2, 5) == '101'
    assert heap._convert_to_base(2, 6) == '110'
    assert heap._convert_to_base(2, 7) == '111'
    assert heap._convert_to_base(2, 8) == '1000'
    assert heap._convert_to_base(2, 9) == '1001'
    assert heap._convert_to_base(2, 10) == '1010'
    assert heap._convert_to_base(2, 11) == '1011'
    assert heap._convert_to_base(2, 12) == '1100'
    assert heap._convert_to_base(2, 13) == '1101'
    assert heap._convert_to_base(2, 14) == '1110'
    assert heap._convert_to_base(2, 15) == '1111'
    assert heap._convert_to_base(2, 16) == '10000'


    assert heap._convert_to_base(3, 0) == '0'
    assert heap._convert_to_base(3, 1) == '1'
    assert heap._convert_to_base(3, 2) == '2'
    assert heap._convert_to_base(3, 3) == '10'
    assert heap._convert_to_base(3, 4) == '11'
    assert heap._convert_to_base(3, 5) == '12'
    assert heap._convert_to_base(3, 6) == '20'
    assert heap._convert_to_base(3, 7) == '21'
    assert heap._convert_to_base(3, 8) == '22'
    assert heap._convert_to_base(3, 9) == '100'
    assert heap._convert_to_base(3, 10) == '101'
    assert heap._convert_to_base(3, 11) == '102'
    assert heap._convert_to_base(3, 12) == '110'
    assert heap._convert_to_base(3, 13) == '111'
    assert heap._convert_to_base(3, 14) == '112'
    assert heap._convert_to_base(3, 15) == '120'
    assert heap._convert_to_base(3, 16) == '121'


def test_size():  
    heap = ArrayMaxHeap(3)
    assert heap.size() == 0

    num_elements = 15
    for i in range(0, num_elements):
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
        heap.insert(i,i)
        assert heap.size() == i + 1
        # assert heap.is_valid()

    assert True == False

    for i in range(num_elements, 0):
        heap.delete(i)
        assert heap.size() == i


# Tests for insert()
def test_one_insert():
    heap = ArrayMaxHeap(3)
    heap.insert(1,1)
    assert heap.is_valid()
    assert heap.size() == 1
    assert heap.contains(1)


def test_two_elements_lower_priority_inserted_first():
    heap = ArrayMaxHeap(3)
    heap.insert('a',1)
    heap.insert('b',2)
    assert heap.is_valid()
    assert heap.size() == 2
    assert heap.contains('a')
    assert heap.contains('b')


def test_two_elements_higher_priority_inserted_first():
    heap = ArrayMaxHeap(3)
    heap.insert('a',2)
    heap.insert('b',1)
    assert heap.contains('a')
    assert heap.contains('b')
    assert heap.is_valid()


def test_two_elements_same_priorities():
    heap = ArrayMaxHeap(3)
    heap.insert('a',1)
    heap.insert('b',1)
    assert heap.contains('a')
    assert heap.contains('b')
    assert heap.is_valid()


def test_two_elements_same_priorities():
    heap = ArrayMaxHeap(3)
    heap.insert('a',1)
    heap.insert('b',1)
    assert heap.is_valid()


def test_many_inserts_ascending_order():
    heap = ArrayMaxHeap(3)
    heap.insert('a',1)
    heap.insert('b',2)
    heap.insert('c',3)
    heap.insert('d',4)
    heap.insert('e',5)
    heap.insert('f',6)
    heap.insert('g',7)
    heap.insert('h',8)
    heap.insert('i',9)
    heap.insert('j',10)
    assert heap.contains('a')
    assert heap.contains('b')
    assert heap.contains('c')
    assert heap.contains('d')
    assert heap.contains('e')
    assert heap.contains('f')
    assert heap.contains('g')
    assert heap.contains('h')
    assert heap.contains('i')
    assert heap.contains('j')
    assert heap.is_valid()
    assert heap.size() == 10


def test_many_inserts_descending_order():
    heap = ArrayMaxHeap(3)
    heap.insert('a', 10)
    heap.insert('b', 9)
    heap.insert('c', 8)
    heap.insert('d', 7)
    heap.insert('e', 6)
    heap.insert('f', 5)
    heap.insert('g', 4)
    heap.insert('h', 3)
    heap.insert('i', 2)
    heap.insert('j', 1)
    assert heap.peek() == 'a'
    assert heap.is_valid()


def test_many_inserts_mixed_order():
    heap = ArrayMaxHeap(3)
    heap.insert('e', 6)
    heap.insert('i', 2)
    heap.insert('c', 8)
    heap.insert('h', 3)
    heap.insert('b', 9)
    heap.insert('g', 4)
    heap.insert('j', 1)
    heap.insert('a', 10)
    heap.insert('d', 7)
    heap.insert('f', 5)
    assert heap.peek() == 'a'
    assert heap.is_valid()


def test_random_heap_insert(): 
    for i in range(5):
        heap = ArrayMaxHeap(3)
        existing_elements = set()
        num_inserts = 100

        actual_inserts = 0
        while actual_inserts < num_inserts:
            element_title = random.randint(1, 10000)  # Random value to insert
            element_priority = random.randint(1, 100)  # Random priority for the value

            if element_title not in existing_elements:
                heap.insert(element_title, element_priority)  # Insert into the heap
                assert heap.is_valid()

                existing_elements.add(element_title)
                actual_inserts += 1


# Tests for update()
def test_update_heap_single_element():
    heap = ArrayMaxHeap(3)
    heap.insert('a', 1)
    assert heap.get_element_priority('a') == 1
    heap.update('a', 5)
    assert heap.get_element_priority('a') == 5


def test_update_heap_two_elements():
    heap = ArrayMaxHeap(3)
    heap.insert('a', 1)
    heap.insert('b', 2)
    assert heap.get_element_priority('a') == 1
    heap.update('a', 5)
    heap.update('b',6 )
    assert heap.get_element_priority('a') == 5
    assert heap.get_element_priority('b') == 6


def test_update_heap_many_elements(): 
    heap = ArrayMaxHeap(3)
    num_elements = 20
    for i in range(0, num_elements):
        heap.insert(i, i)

    for i in range(0, num_elements):
        heap.update(i, i+5)

    for i in range(0, num_elements):
        assert heap.get_element_priority(i) == i + 5


def test_two_elements_update_priority():
    heap = ArrayMaxHeap(3)
    heap.insert('a', 1)
    heap.insert('b', 2)
    assert heap.is_valid()
    assert heap.peek() == 'b'

    heap.update('a', 3)
    assert heap.is_valid()
    assert heap.peek() == 'a'


# Tests for delete()
def test_delete_single_element():
    heap = ArrayMaxHeap(3)
    heap.insert('a',1)
    assert heap.size() == 1
    assert heap.contains('a') == True
    heap.delete('a')
    assert heap.size() == 0
    assert heap.contains('a') == False


def test_delete_leaves_until_empty():   # index error with get_last
    heap = ArrayMaxHeap(3)
    heap.insert(1,1)
    heap.insert(2,2)
    heap.insert(3,3)
    heap.insert(4,4)
    heap.insert(5,5)
    assert heap.size() == 5
    assert heap.is_valid()
    
    heap.delete(1)
    assert heap.size() == 4
    assert heap.is_valid()
    assert heap.contains(1) == False
    
    heap.delete(2)
    assert heap.size() == 3
    assert heap.is_valid()
    assert heap.contains(2) == False

    heap.delete(3)
    assert heap.size() == 2
    assert heap.is_valid()
    assert heap.contains(3) == False

    heap.delete(4)
    assert heap.size() == 1
    assert heap.is_valid()
    assert heap.contains(4) == False

    heap.delete(5)
    assert heap.size() == 0
    assert heap.contains(5) == False
    assert heap.is_valid()

    assert heap.is_empty()


def test_heap_delete_root():    # index error with get_last
    heap = ArrayMaxHeap(3)

    heap.insert(24, 24)
    heap.insert(51, 51)
    heap.insert(5, 5)
    heap.insert(29, 29)
    heap.insert(88, 88)
    heap.insert(76, 76)
    heap.insert(41, 41)

    assert heap.is_valid()
    assert heap.peek() == 88
    assert heap.size() == 7
    heap.delete(88)
    assert heap.peek() == 76
    assert heap.size() == 6
    assert heap.contains(88) == False
    assert heap.is_valid()


def test_delete_root_until_empty(): # index error with get_last
    heap = ArrayMaxHeap(3)
    heap.insert('a',1)
    heap.insert('b',2)
    heap.insert('c',3)
    heap.insert('d',4)
    heap.insert('e',5)
    heap.insert('f',6)
    heap.insert('g',7)    

    assert heap.size() == 7
    assert heap.is_valid()

    heap.delete('g')
    assert heap.size() == 6
    assert heap.contains('g') == False
    assert heap.is_valid()

    heap.delete('f')
    assert heap.size() == 5
    assert heap.contains('f') == False
    assert heap.is_valid()

    heap.delete('e')
    assert heap.size() == 4
    assert heap.contains('e') == False
    assert heap.is_valid()

    heap.delete('d')
    assert heap.size() == 3
    assert heap.contains('d') == False
    assert heap.is_valid()

    heap.delete('c')
    assert heap.size() == 2
    assert heap.contains('c') == False
    assert heap.is_valid()

    heap.delete('b')
    assert heap.size() == 1
    assert heap.contains('c') == False
    assert heap.is_valid()

    heap.delete('a')
    assert heap.size() == 0
    assert heap.contains('c') == False
    assert heap.is_valid()

    assert heap.is_empty()


# Tests for top
def test_top_empty_heap():
    heap = ArrayMaxHeap(3)
    with pytest.raises(IndexError):
        heap.top()


def test_top_one_element():
    heap = ArrayMaxHeap(3)
    heap.insert('a', 1)
    assert heap.top() == 'a'
    assert heap.is_empty()


def test_top_many_elements():   # index error with get_last
    heap = ArrayMaxHeap(3)
    heap.insert('e', 6)
    heap.insert('i', 2)
    heap.insert('c', 8)
    heap.insert('h', 3)
    heap.insert('b', 9)
    heap.insert('g', 4)
    heap.insert('j', 1)
    heap.insert('a', 10)
    heap.insert('d', 7)
    heap.insert('f', 5)

    assert heap.top() == 'a'
    assert heap.top() == 'b'
    assert heap.top() == 'c'
    assert heap.top() == 'd'
    assert heap.top() == 'e'
    assert heap.top() == 'f'
    assert heap.top() == 'g'
    assert heap.top() == 'h'
    assert heap.top() == 'i'
    assert heap.top() == 'j'
    assert heap.is_empty()


def test_peek_empty_heap():
    heap = ArrayMaxHeap(3)
    with pytest.raises(IndexError):
        heap.peek()


def test_peek_one_element():
    heap = ArrayMaxHeap(3)
    heap.insert('a', 1)
    assert heap.peek() == 'a'


def test_peek_mant_elements():
    heap = ArrayMaxHeap(3)
    heap.insert('e', 6)
    heap.insert('i', 2)
    heap.insert('c', 8)
    heap.insert('h', 3)
    heap.insert('b', 9)
    heap.insert('g', 4)
    heap.insert('j', 1)
    heap.insert('a', 10)
    heap.insert('d', 7)
    heap.insert('f', 5)

    assert heap.size() == 10
    assert heap.peek() == 'a'
    assert heap.size() == 10


def top_peek_consistent():
    heap = ArrayMaxHeap(3)
    heap.insert('e', 6)
    heap.insert('i', 2)
    heap.insert('c', 8)
    heap.insert('h', 3)
    heap.insert('b', 9)
    heap.insert('g', 4)
    heap.insert('j', 1)
    heap.insert('a', 10)
    heap.insert('d', 7)
    heap.insert('f', 5)

    assert heap.peek() == heap.top() == 'a'
    assert heap.peek() == heap.top() == 'b'
    assert heap.peek() == heap.top() == 'c'
    assert heap.peek() == heap.top() == 'd'
    assert heap.peek() == heap.top() == 'e'
    assert heap.peek() == heap.top() == 'f'
    assert heap.peek() == heap.top() == 'g'
    assert heap.peek() == heap.top() == 'h'
    assert heap.peek() == heap.top() == 'i'
    assert heap.peek() == heap.top() == 'j'



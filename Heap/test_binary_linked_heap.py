import pytest
import random
from linked_heap import ArrayMaxHeap, HeapObject

# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 1/30/2025
# Description: Unit tests for linked binary max heap implementation
# -----------------------------------------------------------------------------


def test_is_valid_iterative():
    heap = ArrayMaxHeap()

    # Case: Empty heap
    assert heap.is_valid()

    # Case: Single element (root only)
    heap.root = HeapObject('a', 10)
    heap.num_elements = 1
    assert heap.is_valid()

    # Case: Valid max-heap with two elements
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 5)
    heap.root._children = [b]
    b._parent = heap.root
    heap.num_elements = 2
    assert heap.is_valid()

    # Case: Valid max-heap with three elements
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 8)
    c = HeapObject('c', 7)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    heap.num_elements = 3
    assert heap.is_valid()

    # Case: Invalid heap where parent is smaller than child
    heap.root = HeapObject('a', 5)
    b = HeapObject('b', 10)
    heap.root._children = [b]
    b._parent = heap.root
    heap.num_elements = 2
    assert heap.is_valid() == False

    # Case: Invalid heap where second level element is greater than the root
    heap.root = HeapObject('a', 5)
    b = HeapObject('b', 8)
    c = HeapObject('c', 6)
    d = HeapObject('d', 9)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    b._children = [d]
    d._parent = b
    heap.num_elements = 4
    assert heap.is_valid() == False

    # Case: Valid max-heap with multiple elements
    heap.root = HeapObject('d', 50)
    b = HeapObject('c', 30)
    c = HeapObject('b', 20)
    d = HeapObject('a', 10)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    b._children = [d]
    d._parent = b
    heap.num_elements = 4
    assert heap.is_valid()

    # Case: Invalid heap where left child is greater than root
    heap.root = HeapObject('a', 10)
    b = HeapObject('b', 20)
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

    # Case: Large heap, valid max-heap structure
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
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    b._children = [d, e]
    d._parent = b
    e._parent = b
    c._children = [f, g]
    f._parent = c
    g._parent = c
    d._children = [h, i]
    h._parent = d
    i._parent = d
    e._children = [j]
    j._parent = e
    heap.num_elements = 10
    assert heap.is_valid()

    # Case: Large heap, invalid structure (element at index 5 breaks the max-heap property)
    heap.root = HeapObject('a', 100)
    b = HeapObject('b', 90)
    c = HeapObject('c', 80)
    d = HeapObject('d', 70)
    e = HeapObject('e', 60)
    f = HeapObject('f', 110)
    g = HeapObject('g', 40)
    h = HeapObject('h', 30)
    i = HeapObject('i', 20)
    j = HeapObject('j', 10)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    b._children = [d, e]
    d._parent = b
    e._parent = b
    c._children = [f, g]
    f._parent = c
    g._parent = c
    d._children = [h, i]
    h._parent = d
    i._parent = d
    e._children = [j]
    j._parent = e
    heap.num_elements = 10
    assert heap.is_valid() == False

    # Case: Valid heap with edge case values (zeroes and negatives)
    heap.root = HeapObject('a', 0)
    b = HeapObject('b', -1)
    c = HeapObject('c', -2)
    d = HeapObject('d', -3)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    b._children = [d]
    d._parent = b
    heap.num_elements = 4
    assert heap.is_valid()

    # Case: Invalid heap with negative values (root is smaller than a child)
    heap.root = HeapObject('a', -3)
    b = HeapObject('b', -1)
    c = HeapObject('c', -2)
    heap.root._children = [b, c]
    b._parent = heap.root
    c._parent = heap.root
    heap.num_elements = 3
    assert heap.is_valid() == False


def test_is_empty():
    heap = ArrayMaxHeap()
    assert heap.is_valid()
    assert heap.size() == 0
    assert heap.is_empty()

    heap.insert('a', 1)
    assert not heap.is_empty()
    assert heap.is_valid()

    heap.delete('a')
    assert heap.is_empty()
    assert heap.is_valid()


def test_contains():
    heap = ArrayMaxHeap()
    heap.insert('a',1)
    heap.insert('b',2)
    heap.insert('c',3)
    heap.insert('d',4)
    heap.insert('e',5)

    assert heap.contains('a')
    assert heap.contains('b')
    assert heap.contains('c')
    assert heap.contains('d')
    assert heap.contains('e')

    assert not heap.contains('f')
    assert not heap.contains('g')
    assert not heap.contains('h')

    heap.insert('f', 2)
    assert heap.contains('f')

    heap.delete('d')
    assert not heap.contains('d')

    assert heap.contains('a')
    assert heap.contains('b')
    assert heap.contains('c')
    assert heap.contains('e')
    assert heap.contains('f')


def test_size():  
    heap = ArrayMaxHeap()
    assert heap.size() == 0

    num_elements = 100
    for i in range(0, num_elements):
        heap.insert(i,i)
        assert heap.size() == i + 1
        assert heap.is_valid()

    for i in range(num_elements, 0):
        heap.delete(i)
        assert heap.size() == i


# Tests for insert()
def test_one_insert():
    heap = ArrayMaxHeap()
    heap.insert(1,1)
    assert heap.is_valid()
    assert heap.size() == 1
    assert heap.contains(1)


def test_two_elements_lower_priority_inserted_first():
    heap = ArrayMaxHeap()
    heap.insert('a',1)
    heap.insert('b',2)
    assert heap.is_valid()
    assert heap.size() == 2
    assert heap.contains('a')
    assert heap.contains('b')


def test_two_elements_higher_priority_inserted_first():
    heap = ArrayMaxHeap()
    heap.insert('a',2)
    heap.insert('b',1)
    assert heap.contains('a')
    assert heap.contains('b')
    assert heap.is_valid()


def test_two_elements_same_priorities():
    heap = ArrayMaxHeap()
    heap.insert('a',1)
    heap.insert('b',1)
    assert heap.contains('a')
    assert heap.contains('b')
    assert heap.is_valid()


def test_two_elements_same_priorities():
    heap = ArrayMaxHeap()
    heap.insert('a',1)
    heap.insert('b',1)
    assert heap.is_valid()


def test_many_inserts_ascending_order():
    heap = ArrayMaxHeap()
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
    heap = ArrayMaxHeap()
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
    heap = ArrayMaxHeap()
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
        heap = ArrayMaxHeap()
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
    heap = ArrayMaxHeap()
    heap.insert('a', 1)
    assert heap.get_element_priority('a') == 1
    heap.update('a', 5)
    assert heap.get_element_priority('a') == 5


def test_update_heap_two_elements():
    heap = ArrayMaxHeap()
    heap.insert('a', 1)
    heap.insert('b', 2)
    assert heap.get_element_priority('a') == 1
    heap.update('a', 5)
    heap.update('b',6 )
    assert heap.get_element_priority('a') == 5
    assert heap.get_element_priority('b') == 6


def test_update_heap_many_elements(): 
    heap = ArrayMaxHeap()
    num_elements = 20
    for i in range(0, num_elements):
        heap.insert(i, i)

    for i in range(0, num_elements):
        heap.update(i, i+5)

    for i in range(0, num_elements):
        assert heap.get_element_priority(i) == i + 5


def test_two_elements_update_priority():
    heap = ArrayMaxHeap()
    heap.insert('a', 1)
    heap.insert('b', 2)
    assert heap.is_valid()
    assert heap.peek() == 'b'

    heap.update('a', 3)
    assert heap.is_valid()
    assert heap.peek() == 'a'


# Tests for delete()
def test_delete_single_element():
    heap = ArrayMaxHeap()
    heap.insert('a',1)
    assert heap.size() == 1
    assert heap.contains('a') == True
    heap.delete('a')
    assert heap.size() == 0
    assert heap.contains('a') == False


def test_delete_leaves_until_empty():   # index error with get_last
    heap = ArrayMaxHeap()
    heap.insert(1,1)
    heap.insert(2,2)
    heap.insert(3,3)
    heap.insert(4,4)
    heap.insert(5,5)
    assert heap.size() == 5
    assert heap.is_valid()
    
    print("Removing: 1")
    heap.delete(1)
    assert heap.size() == 4
    assert heap.is_valid()
    assert heap.contains(1) == False
    
    print("Removing: 2")
    heap.delete(2)
    assert heap.size() == 3
    assert heap.is_valid()
    assert heap.contains(2) == False

    print("Removing: 3")
    heap.delete(3)
    assert heap.size() == 2
    assert heap.is_valid()
    assert heap.contains(3) == False

    print("Removing: 4")
    heap.delete(4)
    assert heap.size() == 1
    assert heap.is_valid()
    assert heap.contains(4) == False

    print("Removing: 5")
    heap.delete(5)
    assert heap.size() == 0
    assert heap.contains(5) == False
    assert heap.is_valid()

    assert heap.is_empty()


def test_heap_delete_root():    # index error with get_last
    heap = ArrayMaxHeap()

    heap.insert(24, 24)
    heap.insert(51, 51)
    heap.insert(5, 5)
    heap.insert(29, 29)
    heap.insert(88, 88)
    heap.insert(76, 76)
    heap.insert(41, 41)

    assert heap.peek() == 88
    assert heap.size() == 7
    heap.delete(88)
    assert heap.peek() == 76
    assert heap.size() == 6
    assert heap.contains(88) == False
    assert heap.is_valid()


def test_delete_root_until_empty(): # index error with get_last
    heap = ArrayMaxHeap()
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
    heap = ArrayMaxHeap()
    with pytest.raises(IndexError):
        heap.top()


def test_top_one_element():
    heap = ArrayMaxHeap()
    heap.insert('a', 1)
    assert heap.top() == 'a'
    assert heap.is_empty()


def test_top_many_elements():   # index error with get_last
    heap = ArrayMaxHeap()
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
    heap = ArrayMaxHeap()
    with pytest.raises(IndexError):
        heap.peek()


def test_peek_one_element():
    heap = ArrayMaxHeap()
    heap.insert('a', 1)
    assert heap.peek() == 'a'


def test_peek_mant_elements():
    heap = ArrayMaxHeap()
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
    heap = ArrayMaxHeap()
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



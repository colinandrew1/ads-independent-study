import pytest
import random
from heap import ArrayMaxHeap

# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 1/30/2025
# Description: Unit tests for binary max heap implementation
# -----------------------------------------------------------------------------


def test_is_valid():
    heap = ArrayMaxHeap()

    # Case: Empty heap
    heap.elements = []
    assert heap.is_valid()

    # Case: Single element (root only)
    heap.elements = [('a', 10)]
    assert heap.is_valid()

    # Case: Valid max-heap with two elements
    heap.elements = [('a', 10), ('b', 5)]
    assert heap.is_valid()

    # Case: Valid max-heap with three elements
    heap.elements = [('a', 10), ('b', 8), ('c', 7)]
    assert heap.is_valid()

    # Case: Invalid heap where parent is smaller than child
    heap.elements = [('a', 5), ('b', 10)]
    assert heap.is_valid() == False

    # Case: Invalid heap where second level element is greater than the root
    heap.elements = [('a', 5), ('b', 8), ('c', 6), ('d', 9)]
    assert heap.is_valid() == False

    # Case: Valid max-heap with multiple elements
    heap.elements = [('d', 50), ('c', 30), ('b', 20), ('a', 10)]
    assert heap.is_valid()

    # Case: Invalid heap where left child is greater than root
    heap.elements = [('a', 10), ('b', 20), ('c', 5)]
    assert heap.is_valid() == False

    # Case: Valid heap with duplicate values
    heap.elements = [('a', 10), ('b', 10), ('c', 10)]
    assert heap.is_valid()

    # Case: Large heap, valid max-heap structure
    heap.elements = [
        ('a', 100), ('b', 90), ('c', 80), ('d', 70), ('e', 60),
        ('f', 50), ('g', 40), ('h', 30), ('i', 20), ('j', 10)
    ]
    assert heap.is_valid()

    # Case: Large heap, invalid structure (element at index 5 breaks the max-heap property)
    heap.elements = [
        ('a', 100), ('b', 90), ('c', 80), ('d', 70), ('e', 60),
        ('f', 110), ('g', 40), ('h', 30), ('i', 20), ('j', 10)
    ]
    assert heap.is_valid() == False

    # Case: Valid heap with edge case values (zeroes and negatives)
    heap.elements = [('a', 0), ('b', -1), ('c', -2), ('d', -3)]
    assert heap.is_valid()

    # Case: Invalid heap with negative values (root is smaller than a child)
    heap.elements = [('a', -3), ('b', -1), ('c', -2)]
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

    num_elements = 1000

    for i in range(0, num_elements):
        heap.insert(i,i)
        assert heap.size() == i + 1

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


def test_two_elements_update_priority():
    heap = ArrayMaxHeap()
    heap.insert('a', 1)
    heap.insert('b', 2)
    assert heap.is_valid()
    assert heap.peek() == 'b'

    heap.update('a', 3)
    assert heap.is_valid()
    assert heap.peek() == 'a'


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
    print(heap.elements)


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
    print(heap.elements)


def test_random_heap_insert():
    for i in range(5):
        heap = ArrayMaxHeap()
        existing_elements = set()
        num_inserts = 1000

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


# Tests for delete()
def test_delete_single_element():
    heap = ArrayMaxHeap()
    heap.insert('a',1)
    assert heap.size() == 1
    assert heap.contains('a') == True
    heap.delete('a')
    assert heap.size() == 0
    assert heap.contains('a') == False


def test_delete_leaves_until_empty():
    heap = ArrayMaxHeap()
    heap.insert('a',1)
    heap.insert('b',2)
    heap.insert('c',3)
    heap.insert('d',4)
    heap.insert('e',5)
    assert heap.size() == 5
    assert heap.is_valid()

    heap.delete('a')
    assert heap.size() == 4
    assert heap.contains('a') == False

    heap.delete('b')
    assert heap.size() == 3
    assert heap.contains('b') == False

    heap.delete('c')
    assert heap.size() == 2
    assert heap.contains('c') == False

    heap.delete('d')
    assert heap.size() == 1
    assert heap.contains('d') == False

    heap.delete('e')
    assert heap.size() == 0
    assert heap.contains('e') == False
    assert heap.is_empty()


def test_heap_delete_root():
    heap = ArrayMaxHeap()

    heap.insert(67, 24)
    heap.insert(12, 51)
    heap.insert(39, 5)
    heap.insert(91, 29)
    heap.insert(4, 88)
    heap.insert(55, 76)
    heap.insert(23, 41)

    assert heap.peek() == 4
    assert heap.size() == 7
    heap.delete(4)
    assert heap.peek() == 55
    assert heap.size() == 6
    assert heap.contains(4) == False
    assert heap.is_valid()


def test_delete_root_until_empty():
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


def test_top_mant_elements():
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



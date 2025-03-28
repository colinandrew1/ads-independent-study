import pytest
from Tree import TreeNode, TwoThreeFourTree

def test_empty_tree():
    tree = TwoThreeFourTree()
    assert tree.num_elements == 0
    assert tree.root == None


def test_single_insert():
    tree = TwoThreeFourTree()
    tree.insert(5,5)
    tree.print_tree()
    # assert True == False


def test_fill_root():
    tree = TwoThreeFourTree()
    print("Inserting 5")
    tree.insert(5,5)
    tree.print_tree()
    print("Inserting 7")
    tree.insert(7,7)
    tree.print_tree()
    print("Inserting 9")
    tree.insert(9,9)
    tree.print_tree()


def test_root_split():
    tree = TwoThreeFourTree()
    tree.insert(5,5)
    tree.insert(7,7)
    tree.insert(9,9)
    tree.print_tree()   # root is full
    tree.insert(1,1)    # need to split root before insert
    tree.print_tree()


def test_split_internal_node():
    tree = TwoThreeFourTree()
    tree.insert(5,5)
    tree.insert(7,7)
    tree.insert(9,9)
    tree.insert(1,1)
    tree.insert(2,2)
    tree.print_tree()
    tree.insert(3,3)
    tree.print_tree()


def test_tree_from_notes():
    tree = TwoThreeFourTree()
    print("Inserting 1,7,11")
    tree.insert(1,1)
    tree.insert(7,7)
    tree.insert(11,11)
    tree.print_tree()

    print("Inserting 2")
    tree.insert(2,2)
    tree.print_tree()

    print("Inserting 3")
    tree.insert(3,3)
    tree.print_tree()

    print("Inserting 4")
    tree.insert(4,4)
    tree.print_tree()

    print("Inserting 16,18")
    tree.insert(16,16)
    tree.insert(18,18)
    tree.print_tree()

    print("Inserting 8")
    tree.insert(8,8)
    tree.print_tree()

    print("Inserting 5")
    tree.insert(5,5)
    tree.print_tree()

    print(tree.sorted_keys())

    assert True == False




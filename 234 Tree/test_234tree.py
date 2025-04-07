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


def test_insert_tree_from_notes():
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

    # assert True == False


def test_delete():
    # build the tree from the leaves up
    leaf_a = TreeNode()
    leaf_a.kv_pairs.append(('A','A'))
    leaf_a.kv_pairs.append(('B','B'))

    leaf_b = TreeNode()
    leaf_b.kv_pairs.append(('E','E'))
    leaf_b.kv_pairs.append(('F','F'))

    leaf_c = TreeNode()
    leaf_c.kv_pairs.append(('N','N'))

    leaf_d = TreeNode()
    leaf_d.kv_pairs.append(('R','R'))
    leaf_d.kv_pairs.append(('S','S'))

    leaf_e = TreeNode()
    leaf_e.kv_pairs.append(('X','X'))
    leaf_e.kv_pairs.append(('Y','Y'))
    leaf_e.kv_pairs.append(('Z','Z'))

    internal_a = TreeNode()
    internal_a.kv_pairs.append(('C','C'))
    internal_a.kv_pairs.append(('H','H'))

    internal_b = TreeNode()
    internal_b.kv_pairs.append(('V','V'))

    internal_a.children = [leaf_a, leaf_b, leaf_c]
    internal_b.children = [leaf_d, leaf_e]

    tree = TwoThreeFourTree()
    tree.root = TreeNode('P','P')
    tree.root.children = [internal_a, internal_b]

    tree.print_tree()

    # Start deleting nodes in the order: A N H R C P E F V B X Y S Z
    # This tree/order cover all delete cases
    
    print("Delete A")
    tree.delete('A')    # Case 1
    tree.print_tree()

    print("Delete N")
    tree.delete('N')  # Case 3.1
    tree.print_tree()

    print("Delete H")
    tree.delete('H')  # Case 3.2
    tree.print_tree()

    print("Delete R")
    tree.delete('R')  # Case 1
    tree.print_tree()

    print("Delete C")
    tree.delete('C')  # Case 2.2
    tree.print_tree()

    print("Delete P")
    tree.delete('P')  # Case 2.3
    tree.print_tree()

    print("Delete E")
    tree.delete('E')  # Case 2.2
    tree.print_tree()

    print("Delete F")
    tree.delete('F')  # Case 2.3
    tree.print_tree()

    print("Delete V")
    tree.delete('V')  # Case 2.1
    tree.print_tree()

    print("Delete B")
    tree.delete('B')  # Case 3.1
    tree.print_tree()

    print("Delete X")
    tree.delete('X')  # Case 2.2
    tree.print_tree()

    print("Delete Y")
    tree.delete('Y')  # Case 2.3
    tree.print_tree()

    print("Delete S")
    tree.delete('S')  # Case 1
    tree.print_tree()

    print("Delete Z")
    tree.delete('Z')  # Case 1
    tree.print_tree()

    # assert True == False


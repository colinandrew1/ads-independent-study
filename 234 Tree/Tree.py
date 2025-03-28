# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 3/4/25
# Description: Implementation of a 234 Tree
# -----------------------------------------------------------------------------


class TreeNode:
    # Class level global vars, used for readability in the context of a 4-node
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

    def __init__(self, key, value):
        if key is None: self.kv_pairs = [] 
        else: 
            self.kv_pairs = [(key, value)]  # k-v pairs maintained as a list of tuples (key, value)
        self.children:list = None # a list of treenodes if it has children
    

    def num_keys(self):
        return len(self.kv_pairs)


    def is_full(self):  # if node has 3 keys (and 4 children) it is full - ie it is a 4 node
        return self.num_keys() == 3

    
    def __repr__(self):
        node_string = "["
        for i in range(len(self.kv_pairs)):
            node_string += str(self.key(i))
            if i != len(self.kv_pairs)-1:
                node_string += " | "
        node_string += "]\n"
        return node_string


    def is_leaf(self):
        return self.children is None
    

    def key(self,i) -> int:    # returns i-th key of a given tree node
        return self.kv_pairs[i][0]
    

    def val(self,i):    # returns i-th value of a given tree node
        return self.kv_pairs[i][1]
    
    
    def child(self,i) -> 'TreeNode':    # returns i-th child of a given tree node
        if self.children is None:
            return None
        return self.children[i]
    

    def pairs(self, i) -> tuple:
        return self.kv_pairs[i]


    def split(self) -> tuple:    # splits a 4 node into two 2-nodes and reassigns children of the oroginal node as necessary
        if not self.is_full(): raise ValueError("Node must be full to split")
        left = self.pairs(self.LEFT)
        right = self.pairs(self.RIGHT)
        # Create new 2-nodes
        new_left_node = TreeNode(left[0], left[1])
        new_right_node = TreeNode(right[0], right[1])
        # Reassign children nodes
        if not self.is_leaf():  # node is an internal node with 4 children that need to be reassigned
            new_left_node.children = self.children[0:2]
            new_right_node.children = self.children[2:4]
        return (new_left_node, new_right_node)  # retun new 2-nodes as a tuple


    def insert(self, kv_tuple): # inserts a key-value pair at the correct position
        i = 0
        while i < self.num_keys() and kv_tuple[0] > self.kv_pairs[i][0]:
            i += 1
        self.kv_pairs.insert(i, kv_tuple)

    
    def insert_child(self, child_node:'TreeNode'):  # inserts a child node at the correct position
        if self.children is None:
            self.children = [child_node]
        else:
            child_key = child_node.key(0)  
            i = 0
            while i < len(self.children) and child_key > self.children[i].key(0):
                i += 1
            self.children.insert(i, child_node)



class TwoThreeFourTree:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

    def __init__(self):
        self.root = None    # root initialized to NULL
        self.num_elements = 0   # number of keys in tree, not number of nodes


    def search(self, search_key):
        if self.root:
            return self.search_recursive(search_key, self.root) # start searching at the root
        return None

    def search_recursive(self, search_key, cur_node:TreeNode):
        for i in range(0, cur_node.num_keys()):   # examine keys, smallest -> largest
            if search_key < cur_node.key(i):    # if search key is smaller than current node key, search the given child...we are in the correct range
                self.search_recursive(search_key, cur_node.child(i))
            elif search_key == cur_node.key(i):
                return cur_node.val(i)
        self.search_recursive(search_key, cur_node.child(i))    # search last child if search key is larger than all node keys
        return None


    def insert(self, new_key, new_value):
        if not self.root:   # Case: empty tree
            self.root = TreeNode(new_key, new_value)    # a list consiting of one tuple
            return

        if self.root.is_full():   # Case: root is full, ie it has 3 elements and potentially children
            new_root = TreeNode(self.root.key(self.MIDDLE), self.root.val(self.MIDDLE)) # new root is middle pair
            left, right = self.root.split()   # split root into two 2-nodes and assign root's children to these new nodes (2 children each)
            self.root = new_root
            self.root.children = [left, right]

        cur:TreeNode = self.root
        prev:TreeNode = None
        while cur is not None:    # traverse down the tree until we reach a leaf node
            if cur.is_full():
                prev.insert(cur.kv_pairs[self.MIDDLE])  # push middle value to prev node, which we know is not full
                left, right = cur.split()   # split 4 node into two 2-nodes
                prev.children.remove(cur)   # remove the old node from the parent node
                prev.insert_child(left)     # set the new 2-nodes as children of the parent node
                prev.insert_child(right)
                cur = prev  # have to start search from the previous node
            i = 0
            while i < cur.num_keys():
                if new_key < cur.key(i):
                    break
                i += 1
            prev = cur          # set prev pointer to the current node
            cur = cur.child(i)  # traverse to appropriate child node
        prev.insert((new_key, new_value)) # descend until cur is None, so we must insert at prev
        self.num_elements += 1


    def delete(self, search_key):
        return True
    

    def sorted_keys(self):
        if self.root:
            return self.sorted_keys_recursive(self.root, '')
        return ''

    def sorted_keys_recursive(self, cur_node: TreeNode, sorted_keys_string: str) -> str:
        for i in range(0, cur_node.num_keys()):
            if not cur_node.is_leaf():
                sorted_keys_string = self.sorted_keys_recursive(cur_node.child(i), sorted_keys_string)
            sorted_keys_string += str(cur_node.key(i)) + ' '
        if not cur_node.is_leaf():
            sorted_keys_string = self.sorted_keys_recursive(cur_node.child(cur_node.num_keys()), sorted_keys_string)
        return sorted_keys_string


    def print_tree(self):
        if not self.root:
            print("Tree is empty")
            return
        
        queue = [(self.root, 0)]  # store (node, level)
        current_level = 0
        while queue:
            node, level = queue.pop(0)

            if level > current_level:
                print()
                current_level = level
            
            node_str = "["
            for key,val in node.kv_pairs:
                node_str += str(key) + " | " 
            node_str = node_str[:-3] + "]"  # removes " | ", adds closing bracket
            print(node_str, end=" ") 
            
            if not node.is_leaf():
                for child in node.children:
                    queue.append((child, level + 1))
        
        print("\n")



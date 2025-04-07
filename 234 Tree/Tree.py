# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 3/18/25
# Description: Implementation of a 234 Tree
# -----------------------------------------------------------------------------


class TreeNode:
    # Class level global vars, used for readability in the context of a 4-node
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

    def __init__(self, key=None, value=None):
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


    def contains(self, key):
        for i in range(self.num_keys()):
            if self.kv_pairs[i][0] == key:  # kv pairs stored as tuple
                return i
        return None
    

    def remove(self, key):
        for i in range(len(self.kv_pairs)):
            if self.key(i) == key:
                del self.kv_pairs[i]
                break        

        

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
        if self.root is not None: self.delete_recursive(search_key, self.root)
        else: raise ValueError("Tree is empty")


    def delete_recursive(self, search_key, cur_node:TreeNode):
        if cur_node.is_leaf():
            # print(cur_node)
            print("Case 1")
            if cur_node.contains(search_key) is not None: cur_node.remove(search_key)   # Case 1 -- contains() returns index if key not present, None otherwise
            else: raise KeyError("Key does not exist within tree")

        else:   # cur node is an internal node
            key_idx = cur_node.contains(search_key) 
            if key_idx is not None: # Case 2, present within current internal node
                left_child = cur_node.child(key_idx)
                right_child = cur_node.child(key_idx+1)

                if left_child.num_keys() >= 2:   # case 2.1: replace w predecessor then recursively delete predecessor from child
                    print("Case 2.1")
                    predecessor = left_child.pairs(left_child.num_keys()-1)  # predecessor is the last key in the left child
                    cur_node.kv_pairs[key_idx] = predecessor
                    self.delete_recursive(predecessor[0], left_child)   # predecessor is a tuple
                
                elif right_child.num_keys() >= 2:    # case 2.2
                    print("Case 2.2")
                    successor = right_child.pairs(0)
                    cur_node.kv_pairs[key_idx] = successor
                    self.delete_recursive(successor[0], right_child)
                
                else:   # case 2.3: both L,R children have 1 key -> merge case
                    print("Case 2.3")
                    left_child.insert(right_child.kv_pairs[0])  # we know the right child has only 1 key
                    left_child.insert(cur_node.kv_pairs[key_idx]) # insert the key into the merged node (will be at the middle position)
                    cur_node.kv_pairs.remove(cur_node.pairs(key_idx))
                    if right_child.children is not None:
                        for child in right_child.children:  # have to reassign children of right child to left child
                            left_child.insert_child(child)
                    cur_node.children.remove(right_child)
                    del right_child # have to remove the parents reference to the child
                    if self.root.num_keys() == 0:
                        self.root = left_child
                    self.delete_recursive(search_key, left_child)
                    

            else:   # Case 3: we must first find the appropriate child, then proceed
                i = 0
                while i < cur_node.num_keys() and search_key > cur_node.key(i): 
                    i += 1
                parent_idx = i-1 if i == cur_node.num_keys() else i # in the case that the search key is > than largest key in the parent, we must search the rightmost child but parent key (potentially used in restructuring) is one spot to the left. If not, then child_idx == parent_idx
                # at this point, we have identified the appropriate path to the search key
                if cur_node.child(i).num_keys() == 1:   # restructuring of the tree is required to ensure safe delete
                    left_sibling = None if i == 0 else cur_node.child(i-1) #if i > 0 else None   # the left-most child cant have a left sibling
                    right_sibling = None if i == cur_node.num_keys() else cur_node.child(i+1) # if i < cur_node.num_keys() else None   # nor can the right most have a right sibling, but that will never happen here
                    
                    if left_sibling is not None and left_sibling.num_keys() >= 2:    # case 3.1: left sibling of appropriate child has 2+ keys
                        print("Case 3.1")
                        cur_node.child(i).insert(cur_node.pairs(parent_idx))  # push the key from the parent to the child
                        cur_node.kv_pairs.remove(cur_node.pairs(parent_idx)) # remove the key from the parent
                        left_sibling_key = left_sibling.pairs(left_sibling.num_keys()-1)
                        cur_node.insert(left_sibling_key)   # move the right most key in the left child to the parent
                        left_sibling.kv_pairs.remove(left_sibling_key) # remove that key from the left sibling
                    
                    elif right_sibling is not None and right_sibling.num_keys() >= 2:   # case 3.1: right sibling has 2+ keys
                        print("Case 3.1")
                        cur_node.child(i).insert(cur_node.pairs(parent_idx))
                        cur_node.kv_pairs.remove(cur_node.pairs(parent_idx))
                        right_sibling_key = right_sibling.pairs(0)
                        cur_node.insert(right_sibling_key)
                        right_sibling.kv_pairs.remove(right_sibling_key)

                    else:   # case 3.2: both siblings have only 1 key -> merge case
                        print("Case 3.2")
                        # maybe need to check if L and R sibling are None
                        # need to check that appropriate child is not the rightmost becasue it wont have a right sibling
                        if right_sibling is None: # if right sibling is None, then the appropriate child is the rightmost node and therfore does not have a righmost sibling
                            right_sibling = cur_node.child(i)
                            i -= 1  # have to continue the search from the merged node, which is the left sibling
                        # elif left_sibling is None: left_sibling = cur_node.child(i) # similiar logic as the above
                        left_sibling.insert(right_sibling.pairs(0))    # merge right sibling into the right sibling - we know right sibling only has 1 key.
                        left_sibling.insert(cur_node.pairs(parent_idx))# add a key from the parent into the merged node
                        cur_node.kv_pairs.remove(cur_node.pairs(parent_idx))    # remove the pushed key from the parent
                        cur_node.children.remove(right_sibling) # remove the parents reference to the right child
                        if right_sibling.children is not None:  # if the right sibling (the node that was merged in) has children, we must assign its children to the left sibling
                            for child in right_sibling.children:
                                left_sibling.insert_child(child)
                        del right_sibling # free the right sibling
                        if self.root.num_keys() == 0:  # check if root was "deleted" if so make left child the root
                            self.root = left_sibling
                self.delete_recursive(search_key, cur_node.child(i))    # continue the search from the appropriate child
                

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
                print() # start a new line (for visual purposes)
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



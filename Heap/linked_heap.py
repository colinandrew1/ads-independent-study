# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 1/30/2025
# Description: Linked implementation of a Max Heap
# -----------------------------------------------------------------------------

from math import log

class HeapObject:
    def __init__(self, element_title, element_priority):
        self.element_title = element_title
        self.element_priority = element_priority
        self._parent: HeapObject = None
        self._children: HeapObject = []
    

    def get_title(self):
        return self.element_title
    

    def get_priority(self):
        return self.element_priority
    

    def get_parent(self):
        return self._parent
    

    def get_children(self)->list:
        return self._children
    

    def get_highest_priority_child(self):
        if self._children == []:
            return None
        
        highest_priority_child = self._children[0]    # start with first child as highest
        for child in self._children:
            if child.get_priority() > highest_priority_child.get_priority():
                highest_priority_child = child
        return highest_priority_child
    

    def __repr__(self):
        return f"HeapObject(title={self.element_title}, priority={self.element_priority})"
   


class ArrayMaxHeap:
    def __init__(self, branching_factor=2):
        self.d: int = branching_factor
        self.root: HeapObject = None    # create new heap root
        self.num_elements: int = 0
        self.elements = set()


    def top(self):
        if self.is_empty():
            raise IndexError("Heap is empty")
        if self.size() == 1:
            root_title = self.root.get_title()
            # self.delete(self.root)
            self.root = None
            self.num_elements -= 1
            return root_title
        else:
            old_root = self.root
            self.root = self._get_last()
            self.root.get_parent().get_children().remove(self.root)
            self.root._parent = old_root.get_parent()
            self.root._children = old_root.get_children()
            self._push_down(self.root)
            self.num_elements -= 1
            return old_root.element_title
    
    
    def insert(self, element_title, element_priority):
        if self.contains(element_title):
            raise IndexError("Element already exists within heap, duplicates not allowed")
        self.elements.add(element_title)
        new_element = HeapObject(element_title, element_priority)
        self._add_to_end(new_element)
        self._bubble_up(new_element)
    

    def update(self, element_title, new_priority):
        if not self.contains(element_title):
            raise IndexError("Element does not exist within heap")
        
        element = self._get_element(element_title)
        old_priority = element.get_priority()
        element.element_priority = new_priority

        if new_priority > old_priority:
            self._bubble_up(element)
        if new_priority < old_priority:
            self._push_down(element)
    

    def delete(self, element_title):
        if not self.contains(element_title):
            raise IndexError("Element does not exist within heap")
        
        if self.size() == 1:
            self.root = None
        
        else:
            element = self._get_element(element_title)  # element that will be deleted
            last_element = self._get_last() # replace with last element, then bubble down the tree as needed

            old_priority = element.get_priority()
            replacement_priority = last_element.get_priority()

            # break connections associated with the last element
            last_element.get_parent().get_children().remove(last_element)
            last_element._parent = None
            # at this point last element is a stand alone HeapObject, it is not a part of the tree

            if element != last_element: # need to (potentially) rebalance if it is not the last element in the heap
                self._swap(element, last_element)   # shallow swap
                if replacement_priority > old_priority:
                    self._bubble_up(element)
                if replacement_priority < old_priority:
                    self._push_down(element)

            del last_element    # could do this sooner, but swap() takes 2 HeapObjects

        self.elements.remove(element_title)
        self.num_elements -= 1
        

    def peek(self):
        if not self.root:
            raise IndexError("Heap is empty")
        return self.root.get_title()
    

    def size(self):
        return self.num_elements
    

    def get_element_priority(self, element_title):
        return self._get_element(element_title).get_priority()


    def contains(self, element_title):
        return element_title in self.elements
        

    def is_empty(self):
        if self.num_elements == 0:
            return True
        return False
    

    def clear_heap(self):
        self.root = None
        self.num_elements = 0


    # def is_valid(self):
    #     if self.is_empty():
    #         return True
    #     print("here")
    #     return self._is_valid_recursive(self.root)


    # def _is_valid_recursive(self, element: HeapObject):
    #     parent_priority = element.get_priority()
    #     print("parent priority=", parent_priority)
    #     for child in element.get_children():
    #         print("child priority=", child.get_priority())
    #         if child.get_priority() > parent_priority:
    #             return False
    #         if not self._is_valid_recursive(child):
    #             return False
    #     return True
    

    def is_valid(self):
        if self.is_empty():
            return True
        
        stack = []
        stack.append(self.root)
        while len(stack) != 0:
            cur_node = stack.pop(0)
            if len(cur_node.get_children()) > self.d:
                return False
            for child in cur_node.get_children():
                if child.get_priority() > cur_node.get_priority():
                    return False
                stack.append(child)
        return True
            

    def _bubble_up(self, element:HeapObject):   
        while element != self.root:
            parent = element.get_parent()
            if element.get_priority() > parent.get_priority():
                self._swap(element, parent) # "shallow" swap
                element = parent    # move a layer up the tree
            else:
                break   # element is in its correct position


    def _push_down(self, element:HeapObject):
        while element.get_children() != []:
            highest_priority_child = element.get_highest_priority_child()
            if highest_priority_child.get_priority() > element.get_priority():
                self._swap(element, highest_priority_child)
                element = highest_priority_child    # move a layer down the tree
            else:
                break
    

    def _add_to_end(self, element:HeapObject):
        # similiar logic to get_last(), but treat heap as if it has one more element and stop at its parent
        if self.is_empty():
            self.root = element
        else:
            new_num_elements = self.num_elements + 1
            height = int(log((new_num_elements * (self.d - 1)) + 1, self.d))

            path = ""
            if log(new_num_elements, self.d).is_integer():
                for i in range(height+1):
                    path += '0'
            else:
                path = self._convert_to_base(self.d, new_num_elements)
            path = path[1:] # remove first value (root) from path
            path = path[:-1] # remove last element from path (stop at "parent to be")


            cur_node = self.root
            while len(path) > 0:
                direction = int(path[0])
                cur_node = cur_node.get_children()[direction]
                path = path[1:] # move one layer down the tree
            
            cur_node.get_children().append(element)
            element._parent = cur_node
        self.num_elements += 1
    

    def _get_last(self) -> HeapObject:
        # assume heap is non-empty if this method gets called
        if self.size() == 1:
            return self.root
        
        height = int(log((self.num_elements * (self.d - 1)) + 1, self.d))
        path = ""
        if log(self.num_elements, self.d).is_integer(): # the first node at the new level 
            for i in range(height+1):
                path += '0'
        else:
            path = self._convert_to_base(self.d, self.num_elements)
        path = path[1:] # remove first value (root) from path

        cur_node = self.root
        while len(path) > 0:
            direction = int(path[0])
            cur_node = cur_node.get_children()[direction]
            path = path[1:] # move one layer down the tree

        return cur_node


    def _convert_to_base(self, base, n):
        if n == 0:
            return "0"
        digits = []
        while n:
            digits.append(int(n % base))
            n //= base
        digits.reverse()
        return ''.join(map(str, digits))


    def _get_element(self, element_title) -> HeapObject:
        if not self.contains(element_title):
            raise KeyError("Element is not present within heap")
        return self._get_element_recursive(self.root, element_title)
    

    def _get_element_recursive(self, element:HeapObject, element_title) -> HeapObject:
        if element.get_title() == element_title:
            return element

        for child in element.get_children():
            result =  self._get_element_recursive(child, element_title)
            if result:
                return result
    
    
    def _swap(self, element_a:HeapObject, element_b:HeapObject):
        element_a_title = element_a.get_title()
        element_a_priority = element_a.get_priority()

        element_a.element_title = element_b.get_title()
        element_a.element_priority = element_b.get_priority()

        element_b.element_title = element_a_title
        element_b.element_priority = element_a_priority

    
    def print_tree(self):
        if self.root:
            self._print_node(self.root, 0)


    def _print_node(self, node, level):
        if node is not None:
            print(" " * (level * 2) + f"Title: {node.element_title}, Priority: {node.element_priority}")
            for child in node._children:
                self._print_node(child, level + 1)



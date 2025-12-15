# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 5/5/2025
# Description: Implementation of a kd-tree
# -----------------------------------------------------------------------------

import heapq
import math
import time
import random

class KDNode:
    def __init__(self, point, axis, left=None, right=None):
        self.point = point      # each node reprresents a point in space
        self.axis = axis        # the dimension in the node that is used for comparisons
        self.left = left        # all points in the left subtree have a value less than the current point in the specified dimension
        self.right = right     


class KDTree:
    def __init__(self, points):
        self.root = self.build_tree(points)


    def build_tree(self, point_list, cur_depth=0):
        if not point_list:  # base case: stop when we reach a leaf node
            return None

        dimensions = len(point_list[0]) # 2d, 3d, etc
        axis = cur_depth % dimensions   # tree is structured such that it alternates dimension every level. For 2d tree: x,y,x,y,...

        sorted_points = sorted(point_list, key=lambda point: point[axis]) # key param is a function that returns the value on which we are sorting
        # could have instead used a method to return point[axis] but this requires passing a parameter, which is not possible when passing a function
        # A nested function would also work
        median_index = len(sorted_points) // 2
        median_point = sorted_points[median_index]

        left_points = sorted_points[:median_index]
        right_points = sorted_points[median_index+1:]

        left_child = self.build_tree(left_points, cur_depth+1)
        right_child = self.build_tree(right_points, cur_depth+1)

        return KDNode(point=median_point, axis=axis, left=left_child, right=right_child)


    def distance_squared(self, point1, point2):
        dist = 0
        for i in range(len(point1)):
            dist += (point1[i] - point2[i]) ** 2    # square to avoid negatives
        return dist


    def search(self, node, target, k, heap):
        if node is None:    # base case: leaf node
            return

        dist_sq = self.distance_squared(target, node.point)

        if len(heap) < k:   # until heap has k points, every point encountered is a nearest neighbor
            heapq.heappush(heap, (-dist_sq, node.point))    # heap stores tuple: (distance, point)
        else:
            if dist_sq < -heap[0][0]:   # 'Furthest near neighbor' is stored at root of heap
                heapq.heapreplace(heap, (-dist_sq, node.point))

        axis = node.axis    # the dimension we are comparing on
        diff = target[axis] - node.point[axis]  # distance in just the current dimension

        # kd-tree is a BST so can either go left or right
        if diff < 0:    # the current point "splits" the current dimension into 2 sub-planes. In 2d this is L,R or top,bottom
            nearer, farther = node.left, node.right
        else:
            nearer, farther = node.right, node.left

        self.search(nearer, target, k, heap)    # search from the nearer node (in current dimension only)

        # because we only consider one dimension when choosing which subtree to search, it is possible that there is a closer point that we did not consider in the other subtree
        # for example, if we are targeting (2,4) and are in the x dimension, we would choose (1,1000) instead of (4, 5)
        # when recursing back up, we must do the following checks: 
            # 1) if we dont have k nearest neighbors then we have to find more points
            # 2) if there is a possibility that there is a closer point in the other subtree, then we must explore it
                # note that the distance (to the nearer point) does not actually get computed until the next recursive call
        if (len(heap) < k) or (diff * diff < -heap[0][0]):
            self.search(farther, target, k, heap)


    def query(self, target, k=1):
        heap = []  
        # application of heap: use a max heap to track the k smallest value. Book describes this
        # Root stores the max value, so when computing a new distance, can just compare to the top of the heap and then insert if warranted
        # heapq provides a min heap, so we have to use negative distance
        
        self.search(self.root, target, k, heap) # performs the actual knn search, stores results in the heap

        nearest = []
        while heap:
            dist_sq, point = heapq.heappop(heap)   # heap stores tuple: (distance, point)
            nearest.append((math.sqrt(-dist_sq), point))    # take squre root for actual distance (used squared distance in search). Negate distance for actual distance (negative distance used in search)
        nearest.reverse()   # have to reverse bc of heap property
        return nearest


    def benchmark_build(self, num_points, seed=0):
        rng = random.Random(seed)
        points = [(rng.random(), rng.random()) for i in range(num_points)]
        start_time = time.perf_counter()
        self.root = self.build_tree(points)
        return time.perf_counter() - start_time


    def benchmark_query(self, num_points, k=3, seed=0):
        rng = random.Random(seed)
        points = [(rng.random(), rng.random()) for index in range(num_points)]
        self.root = self.build_tree(points)

        start_time = time.perf_counter()
        for point in points:
            self.query(point, k=k)
        end_time = time.perf_counter()
        return end_time - start_time
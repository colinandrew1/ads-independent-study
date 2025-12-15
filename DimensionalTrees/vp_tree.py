# -----------------------------------------------------------------------------
# Author: Colin McClelland
# Date: 5/8/2025
# Description: Implementation of a vantage point tree
# -----------------------------------------------------------------------------

import math
import heapq
import random
import time


class VPNode:
    def __init__(self, point, threshold, left=None, right=None):
        self.point = point          # the vantage point
        self.threshold = threshold  # median radius to partition the other points
        self.left = left            # all points closer than threshold
        self.right = right          # all points farther  than threshold


class VPTree:
    def __init__(self, points):
        self.root = self.build_tree(points)


    def build_tree(self, point_list):
        if not point_list: return None

        vantage = point_list[0]

        if len(point_list) == 1: return VPNode(vantage, 0, None, None)

        distances = []
        for point in point_list[1:]:    # first point chosen as the vantage point
            distance = self.distance_squared(vantage, point)
            distances.append((distance, point))

        distances.sort(key=lambda dp: dp[0])
        median_index = len(distances) // 2
        threshold = distances[median_index][0]

        left_points = []
        right_points = []
        for distance, point in distances:
            if distance < threshold:
                left_points.append(point)
            else:
                right_points.append(point)

        left_child = self.build_tree(left_points)
        right_child = self.build_tree(right_points)

        return VPNode(vantage, threshold, left_child, right_child)



    def distance_squared(self, point1, point2): # same as kd-tree
        dist = 0
        for i in range(len(point1)):
            dist += (point1[i] - point2[i]) ** 2    # square to avoid negatives
        return dist


    def search(self, node, target, k, heap):
        if node is None:
            return

        distance_squared = self.distance_squared(target, node.point)

        if len(heap) < k:
            heapq.heappush(heap, (-distance_squared, node.point))
        else:
            if distance_squared < -heap[0][0]:
                heapq.heapreplace(heap, (-distance_squared, node.point))

        if distance_squared < node.threshold:
            nearer, farther = node.left, node.right
        else:
            nearer, farther = node.right, node.left

        self.search(nearer, target, k, heap)
       
        if (len(heap) < k) or (abs(distance_squared - node.threshold) < -heap[0][0]):
            self.search(farther, target, k, heap)


    def query(self, target, k=1):   # same idea as the kd-tree
        heap = []
        self.search(self.root, target, k, heap)

        result = []
        while heap:
            neg_d2, p = heapq.heappop(heap)
            result.append((math.sqrt(-neg_d2), p))
        result.reverse()
        return result
    

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

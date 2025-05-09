import pytest
from kd_tree import KDTree

def get_points(results):
    return [result[1] for result in results]


def test_video_tree_knn1():
    pts = [(5,4), (2,6), (13,3), (3,1), (10,2), (8,7)]
    tree = KDTree(pts)
    assert get_points(tree.query((9,4), k=1)) == [(10,2)]


def test_sample_tree_knn2():
    pts = [(5,4), (2,6), (13,3), (3,1), (10,2), (8,7)]
    tree = KDTree(pts)
    result = get_points(tree.query((9,4), k=2))
    assert result == [(10,2), (8,7)]


def test_sample_tree_knn3():
    pts = [(5,4), (2,6), (13,3), (3,1), (10,2), (8,7)]
    tree = KDTree(pts)
    result = get_points(tree.query((9,4), k=3))
    assert result == [(10,2), (8,7), (5,4)]


def test_sample_tree_origin():
    pts = [(5,4), (2,6), (13,3), (3,1), (10,2), (8,7)]
    tree = KDTree(pts)
    assert get_points(tree.query((0,0), k=2)) == [(3,1), (2,6)]


def test_sample_tree_k_exceeds():
    pts = [(5,4), (2,6), (13,3), (3,1), (10,2), (8,7)]
    tree = KDTree(pts)
    result = tree.query((9,4), k=10)
    assert len(result) == 6


def test_equidistant_2d():
    pts = [(0,0), (0,5), (5,0), (5,5), (2,2)]
    tree = KDTree(pts)
    assert get_points(tree.query((1,1), k=1)) == [(0,0)] or get_points(tree.query((1,1), k=1)) == [(2,2)]


def test_1d():
    pts = [(i,0) for i in range(10)]
    tree = KDTree(pts)
    assert get_points(tree.query((3.3,0), k=3)) == [(3,0),(4,0),(2,0)]


def test_3d():
    pts = [(1,2,3), (4,5,6), (7,8,9), (-1,-1,-1), (0,0,0)]
    tree = KDTree(pts)
    result = get_points(tree.query((1,1,1), k=2))
    assert result == [(0,0,0), (1,2,3)]
    assert get_points(tree.query((8,8,8), k=1)) == [(7,8,9)]


def test_one_point():
    pts = [(1,1)]
    tree = KDTree(pts)
    assert get_points(tree.query((100,100), k=1)) == [(1,1)]
    assert get_points(tree.query((1,1), k=5)) == [(1,1)]


def test_duplicates():
    pts = [(2,2), (2,2), (3,3), (3,3)]
    tree = KDTree(pts)
    result = get_points(tree.query((2,2), k=3))
    assert result.count((2,2)) == 2
    assert result[2] == (3,3)
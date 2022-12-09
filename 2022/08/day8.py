#!/usr/bin/env python3
from typing import List, Dict
from functools import reduce
import operator


def in_bounds(pos_y: int, pos_x: int, map: List[List[int]]) -> bool:
    """check if a position is in bounds in the 2 dimensional array `map`"""
    return (
        pos_y <= len(map) - 1
        and pos_y >= 0
        and pos_x <= len(map[pos_y]) - 1
        and pos_x >= 0
    )


def visible_from_outside(pos_y: int, pos_x: int, map: List[List[int]]):
    """
    check if a position is visible from outside the grid
    visibility is defined that all values in one direction of the two-dimensional array `map`
    are lower than the value of the given point.
    Returns `True`, if the tree is the largest in any direction.
    """
    height: int = map[pos_y][pos_x]
    vects: Dict = [
        {"x": 1, "y": 0},
        {"x": -1, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": -1},
    ]
    return any([visible_outside(pos_y, pos_x, map, height, vect) for vect in vects])


def scenic_score_for_pos(pos_y: int, pos_x: int, map: List[List[int]]):
    """
    calculates the amount of trees visible per direction in the two-dimensional array `map`
    visibility is defined that all values in one direction of the two-dimensional array `map`
    are lower than the value of the given point.
    Returns the 'scenic score' (multiplying the amount of visible trees in each direction)

    """
    height: int = map[pos_y][pos_x]
    vects: Dict = [
        {"x": 1, "y": 0},
        {"x": -1, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": -1},
    ]
    return reduce(
        operator.mul, [count_visible(pos_y, pos_x, map, height, vect) for vect in vects]
    )


def count_visible(
    pos_y: int, pos_x: int, map: List[List[int]], height: int, vect: Dict
) -> int:
    """
    count the amount of visible trees in a given direction `vect`
    values smaller are always seen, visibility stops at equal or higher values
    (but the higher values are seen as well)
    """
    count = 0
    pos_y += vect["y"]
    pos_x += vect["x"]
    while in_bounds(pos_y, pos_x, map):
        if height <= map[pos_y][pos_x]:
            return count + 1
        count += 1
        pos_y += vect["y"]
        pos_x += vect["x"]
    return count


def visible_outside(
    pos_y: int, pos_x: int, map: List[List[int]], height: int, vect: Dict
) -> bool:
    """
    check if all trees in a given direction are smaller, stops at the bounds of the array.
    Exits early, when finding a higher value than the given height.
    """
    pos_y += vect["y"]
    pos_x += vect["x"]
    while in_bounds(pos_y, pos_x, map):
        if height <= map[pos_y][pos_x]:
            return False
        pos_y += vect["y"]
        pos_x += vect["x"]
    return True


map: List[List[int]] = [
    [int(i) for i in x] for x in open("day8.txt", "r").read().splitlines()
]
p1 = 0
p2 = 1

for y in range(0, len(map)):
    for x in range(0, len(map[0])):
        p1 = p1 + 1 if (visible_from_outside(y, x, map)) else p1
        tmp_score = scenic_score_for_pos(y, x, map)
        p2 = tmp_score if tmp_score > p2 else p2

print(p1)
print(p2)

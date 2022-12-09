#!/usr/bin/env python3
def in_bounds(pos_y: int, pos_x: int, map: list) -> bool:
    """check if a position is in bounds in the 2 dimensional array `map`"""
    return (
        pos_y <= len(map) - 1
        and pos_y >= 0
        and pos_x <= len(map[pos_y]) - 1
        and pos_x >= 0
    )


def visible_from_outside(pos_y: int, pos_x: int, map: list):
    """
    check if a position is visible from outside the grid
    visibility is defined that all values in one direction of the two-dimensional array `map`
    are lower than the value of the given point.
    Returns `True`, if the tree is the largest in any direction.
    """
    height: int = map[pos_y][pos_x]
    vects = [{"x": 1, "y": 0}, {"x": -1, "y": 0}, {"x": 0, "y": 1}, {"x": 0, "y": -1}]
    result = False
    for dir in vects:
        result = result or visible(pos_y, pos_x, map, height, dir)
        if result:
            return result
    return result


def scenic_score_for_pos(pos_y: int, pos_x: int, map: list):
    """
    calculates the amount of trees visible per direction in the two-dimensional array `map`
    visibility is defined that all values in one direction of the two-dimensional array `map`
    are lower than the value of the given point.
    Returns the 'scenic score' (multiplying the amount of visible trees in each direction)

    """
    height: int = map[pos_y][pos_x]
    vects = [{"x": 1, "y": 0}, {"x": -1, "y": 0}, {"x": 0, "y": 1}, {"x": 0, "y": -1}]
    scenic_score = 1
    for x in vects:
        print(f"calc for vect {x}")
        scenic_score = count_visible(pos_y, pos_x, map, height, x) * scenic_score
    return scenic_score


def count_visible(pos_y: int, pos_x: int, map: list, height: int, vect: dict) -> int:
    """
    count the amount of visible trees in a given direction `vect`
    values smaller are always seen, visibility stops at equal or higher values
    (but the higher values are seen as well)
    """
    pos_y += vect["y"]
    pos_x += vect["x"]
    if not in_bounds(pos_y, pos_x, map):
        return 0
    if height <= map[pos_y][pos_x]:
        return 1
    return 1 + count_visible(pos_y, pos_x, map, height, vect)


def visible(pos_y: int, pos_x: int, map: list, height: int, vect: dict) -> bool:
    """
    check if all trees in a given direction are smaller, stops at the bounds of the array.
    Exits early, when finding a higher value than the given height.
    """
    pos_y += vect["y"]
    pos_x += vect["x"]
    if not in_bounds(pos_y, pos_x, map):
        return True
    return height > map[pos_y][pos_x] and visible(pos_y, pos_x, map, height, vect)


map: list = [[int(i) for i in x] for x in open("day8.txt", "r").read().splitlines()]
p1 = 0
p2 = 0

for y in range(0, len(map)):
    for x in range(0, len(map[0])):
        p1 = p1 + 1 if (visible_from_outside(y, x, map)) else p1
        t = scenic_score_for_pos(y, x, map)
        p2 = t if t > p2 else p2

print(p1)
print(p2)

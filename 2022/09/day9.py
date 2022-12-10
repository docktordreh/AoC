#!/usr/bin/env python3
import copy
from typing import List


class Position:
    """Class for packaging positions"""

    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.x}/{self.y}"

    def __add__(self, other):
        new = Position(0, 0)
        new.x = self.x + other.x
        new.y = self.y + other.y
        return new

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __radd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __rsub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __sub__(self, other):
        new = Position(0, 0)
        new.x = self.x - other.x
        new.y = self.y - other.y
        return new

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __contains__(self, item):
        return item.x == self.x and item.y == self.y

    def __copy__(self):
        new: Position = Position(0, 0)
        new.x = self.x
        new.y = self.y
        return new

    def negate(self):
        neg: Position = Position(0, 0)
        neg.x = -self.x
        neg.y = -self.y
        return neg

    def touching(self, other):
        """
        check if two positions are touching
        diagonally adjacent or overlapping
        """
        return any([(other + vect) == self for vect in DIRECTION_VECTORS])


VECT_RIGHT = Position(1, 0)
VECT_LEFT = Position(-1, 0)
VECT_UP = Position(0, 1)
VECT_DOWN = Position(0, -1)
DIAGONAL_VECTORS: List[Position] = [
    Position(-1, -1),
    Position(-1, 1),
    Position(1, 1),
    Position(1, -1),
]
DIRECTION_VECTORS: List[Position] = [
    Position(0, 0),
    VECT_RIGHT,
    VECT_LEFT,
    VECT_UP,
    VECT_DOWN,
    Position(-1, -1),
    Position(-1, 1),
    Position(1, 1),
    Position(1, -1),
]


def distance_per_direction_ge_than(pos1: Position, pos2: Position, dist_max: int = 2):
    """
    checks if two given positions differ more than `dist_max` in x/y
    while the other part is not differing at all
    """
    dist: Position = pos2 - pos1
    return any(
        [
            abs(dist.x) >= dist_max and dist.y == 0,
            abs(dist.y) >= dist_max and dist.x == 0,
        ]
    )


def same_row_or_same_column(pos1: Position, pos2: Position):
    """check if pos1 and pos2 are in the same column"""
    return any([pos1.x == pos2.x, pos1.y == pos2.y])


def move_tail_diagonally(pos_head: Position, pos_tail: Position):
    for vect in DIAGONAL_VECTORS:
        pos_tail += vect
        if pos_head.touching(pos_tail):
            return
        pos_tail -= vect


def move_tail_udlr(pos_head: Position, pos_tail: Position):
    for vect in [VECT_DOWN, VECT_LEFT, VECT_RIGHT, VECT_UP]:
        pos_tail += vect
        if not pos_head.touching(pos_tail):
            pos_tail -= vect
            continue
        return


def handle_tail_movement(
    pos_head: Position, pos_tails: List[Position],
    tail_positions: List[Position]
):
    pos1: Position = pos_head
    for i in range(0, len(pos_tails)):
        if i != 0:
            pos1: Position = pos_tails[i - 1]
        pos2: Position = pos_tails[i]
        if distance_per_direction_ge_than(pos1, pos2):
            move_tail_udlr(pos1, pos2)
        else:
            if not pos1.touching(pos2):
                if not same_row_or_same_column(pos1, pos2):
                    move_tail_diagonally(pos1, pos2)
    if pos_tails[len(pos_tails) - 1] not in tail_positions:
        tail_positions.append(copy.copy(pos_tails[len(pos_tails) - 1]))
        return


def move_count(
    count: int,
    vector: Position,
    pos_head: Position,
    pos_tails: List[Position],
    tail_positions: List[Position]
):
    for i in range(0, count):
        pos_head += vector
        handle_tail_movement(pos_head, pos_tails, tail_positions)


def direction_string_to_direction_vector(direction: str) -> Position:
    if direction == "R":
        return VECT_RIGHT
    if direction == "L":
        return VECT_LEFT
    if direction == "U":
        return VECT_UP
    if direction == "D":
        return VECT_DOWN


def move(instruction: str, pos_head: Position, pos_tails: List[Position], tail_positions: List[Position]):
    direction, count = instruction.split()
    direction = direction_string_to_direction_vector(direction)
    move_count(int(count), direction, pos_head, pos_tails, tail_positions)


def sol1(instructions: List[str]):
    pos_head = Position(0, 0)
    pos_tails: List[Position] = []
    tail_positions = []
    amt_tails = 1
    pos_tails = [Position(0, 0) for i in range(0, amt_tails)]
    for instruction in instructions:
        move(instruction, pos_head, pos_tails, tail_positions)
    print(f"sol 1 {len(tail_positions)}")


def sol2(instructions: List[str]):
    pos_head = Position(0, 0)
    tail_positions = []
    amt_tails = 9
    pos_tails = [Position(0, 0) for i in range(0, amt_tails)]
    for instruction in instructions:
        move(instruction, pos_head, pos_tails, tail_positions)
    print(f"sol 2 {len(tail_positions)}")


instructions: List[str] = [x for x in open("day9.txt", "r").read().splitlines()]
sol1(instructions)
sol2(instructions)

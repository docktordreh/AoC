#!/usr/bin/env python3
import sys

data: list = [puzzle for puzzle in open("day5.txt", "r").read().split("\n\n") if puzzle]

puzzle = data[0].splitlines()[:-1]
input = data[1].splitlines()

stacks = []
for x in range(0, len(puzzle[0]) // 3):
    stacks.append([])
    for y in range(1, len(puzzle) + 1):
        if len(puzzle[-y]) < 1 + 4 * x:
            continue
        cur_elem = puzzle[-y][1 + 4 * x]
        if cur_elem == " ":
            continue
        stacks[x].append(cur_elem)

for line in input:
    split = line.split()
    amount = int(split[1])
    frm = int(split[3])
    to = int(split[-1])
    for i in range(0, amount):
        elem = stacks[frm - 1].pop()
        stacks[to - 1].append(elem)

p1 = ""
for stack in stacks:
    p1 += stack.pop()
stacks = []
for x in range(0, len(puzzle[0]) // 3):
    stacks.append([])
    for y in range(1, len(puzzle) + 1):
        if len(puzzle[-y]) < 1 + 4 * x:
            continue
        cur_elem = puzzle[-y][1 + 4 * x]
        if cur_elem == " ":
            continue
        stacks[x].append(cur_elem)
for line in input:
    split = line.split()
    amount = int(split[1])
    frm = int(split[3])
    to = int(split[-1])
    elems=[]
    for i in range(0, amount):
        print(f"stack {frm} currently {stacks[frm-1]}")
        elem = stacks[frm - 1].pop()
        elems.append(elem)
    for e in range(1,len(elems)+1):
        stacks[to - 1].append(elems[-e])

p2 = ""
for stack in stacks:
    p2 += stack.pop()
solution: dict = {"solution_1": p1, "solution_2": p2}
print(f"solution 1: {solution['solution_1']}")
print(f"solution 2: {solution['solution_2']}")

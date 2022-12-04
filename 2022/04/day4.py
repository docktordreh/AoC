#!/usr/bin/env python3


def overlaps(first_range, second_range) -> int:
    if second_range[0] >= first_range[0] and second_range[0] <= first_range[1]:
        return 1
    if first_range[0] >= second_range[0] and first_range[0] <= second_range[1]:
        return 1
    return 0


def between(first_range, second_range):
    print(
        f"checking if {first_range[0]}, {first_range[1]} fits between {second_range[0]} and {second_range[1]} or the other way around"
    )
    return (
        (first_range[0] >= second_range[0] and first_range[1] <= second_range[1])
        or second_range[0] >= first_range[0]
        and second_range[1] <= first_range[1]
    )


data: list = [
    assignment.split(",")
    for assignment in [
        assignment_pair
        for assignment_pair in open("day4.txt", "r").read().split("\n")
        if assignment_pair
    ]
]
assignment_ranges = [
    [assignment_per_elve[0].split("-"), assignment_per_elve[1].split("-")]
    for assignment_per_elve in data
]
countbetween = 0
countoverlaps = 0
for i in range(0, len(assignment_ranges)):
    assignments = assignment_ranges[i]
    first_assignment = [int(x) for x in assignments[0]]
    second_assignment = [int(x) for x in assignments[1]]
    if between(first_assignment, second_assignment):
        print("fits")
        countbetween += 1
        countoverlaps += 1
        continue
    countoverlaps += overlaps(first_assignment, second_assignment)

print(countbetween)
solution: dict = {"solution_1": countbetween, "solution_2": countoverlaps}
print(f"solution 1: {solution['solution_1']}")
print(f"solution 2: {solution['solution_2']}")

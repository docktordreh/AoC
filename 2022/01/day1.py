#!/usr/bin/env python3
data: list = sorted([
    sum(cal_per_elve)
    for cal_per_elve in [
        [int(x) for x in batch.splitlines()] for batch in open("day1.txt").read().split("\n\n")
    ]
])
print(f"solution 1: {data[-1]}")
print(f"solution 2: {sum(data[-3:])}")

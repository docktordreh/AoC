#!/usr/bin/env python3

data: str = open("day6.txt").read()
for i in range(0, len(data)):
    cur_sample: str = data[i : i + 4]
    cur_set = set(cur_sample)
    print(cur_set)
    if len(set(cur_sample)) == 4:
        print(f"sol 1: {i+4}")
        for j in range(i + 4, len(data)):
            s2 = data[j : j + 14]
            if len(set(s2)) == 14:
                print(f"sol 2: {j+14}")
        break

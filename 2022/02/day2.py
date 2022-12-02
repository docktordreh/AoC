#!/usr/bin/env python3
WIN=6
DRAW=3
lookup_1 = {"A X":DRAW+1,"A Y":WIN+2,"A Z":3,
            "B X": 1, "B Y": DRAW+2,"B Z":3+WIN,
            "C X":WIN+1, "C Y":2, "C Z": DRAW+3}
lookup_2 ={"A X":3,"A Y":DRAW+1,"A Z":WIN+2,
          "B X": 1, "B Y": DRAW+2,"B Z":WIN+3,
           "C X":2, "C Y":DRAW+3, "C Z": WIN+1}
data:list = [x for x in
    open("day2.txt","r").read().split("\n") if x ]
solution:dict = {"solution_1": sum([lookup_1[y] for y in data]), "solution_2":sum([lookup_2[y] for y in data]) }
print(f"solution 1: {solution['solution_1']}")
print(f"solution 2: {solution['solution_2']}")

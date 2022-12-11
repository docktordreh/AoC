#!/usr/bin/env python3
from typing import List, Tuple
import sys
from functools import reduce
import operator
import math


class Check:
    operation: str
    target_true: int
    target_false: int
    num: int

    def __init__(self, operation: str, target_true: int, target_false: int):
        self.operation = f"{operation.replace('divisible by', '%')} == 0"
        self.num = int(self.operation.split("%")[1].split("=")[0].strip())
        self.target_true = target_true
        self.target_false = target_false

    def get_num(self):
        return self.num

    def operate(self, val: int) -> int:
        """returns next monkey the item is thrown to"""
        return self.target_true if val % self.num == 0 else self.target_false

    def __repr__(self):
        return f"% {self.num} == 0 - target true {self.target_true} false {self.target_false} "


class Operation:
    operation: str

    def __init__(self, operation: str):
        self.operation = operation.split("=")[1]

    def operate(self, val: int, modulo: int) -> int:
        return eval(self.operation.replace("old", f"{val}")) % modulo

    def __repr__(self):
        return self.operation


class Monkey:
    items: List[int]
    operation: Operation
    check: Check
    monkey_business: int

    def __init__(self, items: List[int], operation: Operation, check: Check):
        self.items = items
        self.operation = operation
        self.check = check
        self.monkey_business = 0

    def __repr__(self):
        return f"{self.items}, {self.operation}, {self.check}"

    def retrieve(self, item):
        self.items.append(item)

    def get_monkey_business(self) -> int:
        return self.monkey_business

    def turn(self):
        return len(self.items) > 0

    def inspect(
        self, common_divisor: int, reduce_worries: bool = True
    ) -> Tuple[int, int]:
        self.monkey_business += 1
        self.items[0] = self.operation.operate(self.items[0], common_divisor)
        if reduce_worries:
            self.items[0] = math.trunc(self.items[0] / 3)
        next_monkey = self.check.operate(self.items[0])
        val = self.items.pop(0)
        return next_monkey, val


def sol1(monkeys: List[Monkey]):
    common_divisor = reduce(
        operator.mul, [monkey.check.get_num() for monkey in monkeys]
    )
    for i in range(20):
        for monkey in monkeys:
            while monkey.turn():
                next_monkey, val = monkey.inspect(common_divisor)
                monkeys[next_monkey].retrieve(val)

    monkey_businesses = [m.get_monkey_business() for m in monkeys]
    monkey_businesses.sort()
    print(reduce(operator.mul, monkey_businesses[-2:]))


def sol2(monkeys: List[Monkey]):
    common_divisor = reduce(
        operator.mul, [monkey.check.get_num() for monkey in monkeys]
    )
    for i in range(10000):
        for j in range(len(monkeys)):
            monkey = monkeys[j]
            while monkey.turn():
                next_monkey, val = monkey.inspect(common_divisor, reduce_worries=False)
                monkeys[next_monkey].retrieve(val)

    monkey_businesses = [m.get_monkey_business() for m in monkeys]
    monkey_businesses.sort()
    print(reduce(operator.mul, monkey_businesses[-2:]))


def main():
    monkeys_str: List[str] = open("day11.txt", "r").read().split("\n\n")
    monkeys: List[Monkey] = []

    for monkey in monkeys_str:
        cur_monkey = monkey.split("\n")
        items: List[int] = [int(x) for x in cur_monkey[1].split(":")[1].split(",")]
        operation: Operation = Operation(cur_monkey[2].split(":")[1])
        check: Check = Check(
            cur_monkey[3].split(":")[1],
            int(cur_monkey[4].split(":")[1].replace(" throw to monkey ", "")),
            int(cur_monkey[5].split(":")[1].replace(" throw to monkey ", "")),
        )
        monkeys.append(Monkey(items, operation, check))
    sol1(monkeys)
    monkeys: List[Monkey] = []

    for monkey in monkeys_str:
        cur_monkey = monkey.split("\n")
        items: List[int] = [int(x) for x in cur_monkey[1].split(":")[1].split(",")]
        operation: Operation = Operation(cur_monkey[2].split(":")[1])
        check: Check = Check(
            cur_monkey[3].split(":")[1],
            int(cur_monkey[4].split(":")[1].replace(" throw to monkey ", "")),
            int(cur_monkey[5].split(":")[1].replace(" throw to monkey ", "")),
        )
        monkeys.append(Monkey(items, operation, check))
    sol2(monkeys)


if __name__ == "__main__":
    main()

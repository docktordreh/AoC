#!/usr/bin/env python3
from typing import List, Dict
import sys
from enum import Enum
from functools import reduce
import operator


class Instructions(Enum):
    noop = "noop"
    addx = "addx"


class Sprite:
    """
    A sprite displayed on the CRT
    """

    width: int

    def __init__(self, width=3):
        self.width = width


class InstructionCost:
    cost: Dict

    def __init__(self, costs: Dict = {"noop": 1, "addx": 2}):
        self.cost = {}
        for instruction in Instructions:
            self.cost[instruction.value] = costs[instruction.value]

    def __getitem__(self, key):
        return self.cost[key]


class CathodeRayTube:
    width: int
    height: int
    pixels: List[List[bool]]

    def __init__(self, width=40, height=6):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]
        pass

    def draw(self, sprite_pos: int, cycle: int):
        y: int = (cycle - 1) // 40
        x: int = cycle - 1 - (y * 40)
        print(f"during cycle {cycle}: CRT draws pixel in position {x}")
        if x in [sprite_pos - 1, sprite_pos, sprite_pos + 1]:
            self.pixels[y][x] = True
        else:
            self.pixels[y][x] = False
        p: str = ""
        for pix in self.pixels[y]:
            p += "" if pix is None else ("." if not pix else "#")
        print(f"Current CRT row: {p}")

    def __repr__(self):
        pix: str = ""
        for y in range(0, len(self.pixels)):
            for x in range(0, len(self.pixels[y])):
                pix += (
                    ""
                    if self.pixels[y][x] is None
                    else ("#" if self.pixels[y][x] else ".")
                )
            pix += "\n"
        return pix


class CPU:
    """
    a simple cpu driven by a clock circuit
    """

    register: int
    crt: CathodeRayTube

    def __init__(self, register_init: int = 1, crt: CathodeRayTube = CathodeRayTube()):
        """
        Initialize a CPU.
        `register_init`: The starting value of the register
        """
        self.register = register_init
        self.crt = crt

    def noop(self):
        pass

    def addx(self, amt):
        self.register += amt

    def get_register(self):
        return self.register

    def get_signal(self, cycle_count: int):
        return self.register * cycle_count


class ClockCircuit:
    """
    a clock ticking at constant rate, each tick is called 'cycle'
    """

    cpu: CPU
    count_cycles: int
    cost: InstructionCost
    signal_strength: List[int]

    def __init__(
        self,
        cpu: CPU = CPU(),
        crt: CathodeRayTube = CathodeRayTube(),
        cost: InstructionCost = InstructionCost(),
    ):
        """
        Initialize the clock circuit
        Pass the `cpu` and the `crt` connected to it.
        """
        self.cpu = cpu
        self.crt = crt
        self.count_cycles = 0
        self.cost = cost
        self.signal_strength = [0]

    def get_cpu_register_val(self):
        return self.cpu.get_register()

    def get_count_cycles(self):
        return self.count_cycles

    def get_signal_strength_at(self, count_cycle: int):
        return self.signal_strength[count_cycle]

    def cycle(self, instruction: str):
        self.count_cycles += 1
        print("\n")
        print(f"start cycle {self.count_cycles}: begin executing {instruction}")
        self.signal_strength.append(self.cpu.get_signal(self.count_cycles))
        self.crt.draw(self.get_cpu_register_val(), self.count_cycles)
        if self.count_cycles == 240:
            print(self.crt)
            sys.exit(5)
            pass

    def schedule_instruction(self, instruction: str):
        """
        schedules an instruction
        """
        instr: Instructions = Instructions[instruction.split()[0]]
        cost: int = self.cost[instr.value]
        for _ in range(cost):
            self.cycle(instruction)
        if instr == Instructions.noop:
            self.cpu.noop()
            print(f"End of cycle {self.count_cycles}: finish executing {instruction}")
            return
        if instr == Instructions.addx:
            self.cpu.addx(int(instruction.split()[1]))
            print(
                f"End of cycle {self.count_cycles}: finish executing {instruction} (Register X {self.get_cpu_register_val()})"
            )
            sprite: List[str] = [
                "."
                if not i
                in [
                    self.get_cpu_register_val(),
                    self.get_cpu_register_val() + 1,
                    self.get_cpu_register_val() - 1,
                ]
                else "#"
                for i in range(0, self.crt.width)
            ]
            print(f"Sprite position: {''.join(sprite)}")
            return


instructions: List[str] = open("day10.txt", "r").read().splitlines()
cc: ClockCircuit = ClockCircuit()
for cmd in instructions:
    cc.schedule_instruction(cmd)

sol1 = reduce(
    operator.add,
    [
        cc.get_signal_strength_at(count_cycle)
        for count_cycle in [20, 60, 100, 140, 180, 220]
    ],
)
print(sol1)
print(cc.crt)

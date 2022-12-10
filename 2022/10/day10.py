#!/usr/bin/env python3
from typing import List, Dict
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
        self.pixels = [[False for _ in range(width)] for _ in range(height)]
        pass

    def in_bounds(self, position:int):
        return position>=(self.width-1)

    def change_sprite_pos(self, position:int, cycle_count_drawing:int):
        if not self.in_bounds(position):
            raise ValueError(f"{position} is not a valid position")
        pass

    def print(self):
        pass


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

    def draw(self, count_cycles):
        self.crt.change_sprite_pos(self.register, count_cycles)

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

    def schedule_instruction(self, instruction: str):
        """
        schedules an instruction
        """
        instr: Instructions = Instructions[instruction.split()[0]]
        cost: int = self.cost[instr.value]
        for _ in range(cost):
            self.count_cycles += 1
            self.signal_strength.append(self.cpu.get_signal(self.count_cycles))
            if self.count_cycles in [20, 60, 100, 140, 180, 220]:
                print(
                    f"signal strength at {self.count_cycles} is {self.cpu.get_signal(self.count_cycles)}"
                )
        if instr == Instructions.noop:
            self.cpu.noop()
            return
        if instr == Instructions.addx:
            self.cpu.addx(int(instruction.split()[1]))
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

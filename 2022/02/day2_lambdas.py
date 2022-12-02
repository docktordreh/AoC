#!/usr/bin/env python3
OPP_ROCK = "A"
OPP_PAPER = "B"
OPP_SCISSOR = "C"
ME_ROCK = "X"
ME_PAPER = "Y"
ME_SCISSOR = "Z"
ME_LOSE = "X"
ME_DRAW = "Y"
ME_WIN = "Z"
POINTS_ROCK = 1
POINTS_PAPER = 2
POINTS_SCISSOR = 3
POINTS_WIN = 6
POINTS_DRAW = 3
POINTS_LOSE = 0


def needed_symbol_points(curr_game_moves: str):
    if win_2(curr_game_moves):
        return (
            POINTS_ROCK
            if OPP_SCISSOR in curr_game_moves
            else (POINTS_PAPER if OPP_ROCK in curr_game_moves else POINTS_SCISSOR)
        )
    if draw_2(curr_game_moves):
        return (
            POINTS_ROCK
            if OPP_ROCK in curr_game_moves
            else (POINTS_PAPER if OPP_PAPER in curr_game_moves else POINTS_SCISSOR)
        )
    return (
        POINTS_ROCK
        if OPP_PAPER in curr_game_moves
        else (POINTS_PAPER if OPP_SCISSOR in curr_game_moves else POINTS_SCISSOR)
    )


def points_per_symbol(sol: int) -> int:
    if sol == 1:
        return (
            lambda curr_game_moves: POINTS_ROCK
            if ME_ROCK in curr_game_moves
            else (POINTS_PAPER if ME_PAPER in curr_game_moves else POINTS_SCISSOR)
        )
    if sol == 2:
        return  lambda curr_game_moves : needed_symbol_points(curr_game_moves)


def win(sol: int):
    if sol == 1:
        return lambda curr_game_moves: curr_game_moves in [
            f"{OPP_ROCK} {ME_PAPER}",
            f"{OPP_PAPER} {ME_SCISSOR}",
            f"{OPP_SCISSOR} {ME_ROCK}",
        ]
    if sol == 2:
        return lambda curr_game_moves: ME_WIN in curr_game_moves


def draw(sol: int):
    if sol == 1:
        return lambda curr_game_moves: curr_game_moves in [
            f"{OPP_ROCK} {ME_ROCK}",
            f"{OPP_PAPER} {ME_PAPER}",
            f"{OPP_SCISSOR} {ME_SCISSOR}",
        ]
    if sol == 2:
        return lambda curr_game_moves: ME_DRAW in curr_game_moves

def points(sol: int) -> int:
    if sol == 1:
        return (
            lambda curr_game_moves: (POINTS_WIN + points_per_symbol_1(curr_game_moves))
            if win_1(curr_game_moves)
            else (
                POINTS_DRAW + points_per_symbol_1(curr_game_moves)
                if draw_1(curr_game_moves)
                else POINTS_LOSE + points_per_symbol_1(curr_game_moves)
            )
        )
    if sol == 2:
        return (
            lambda curr_game_moves: (POINTS_WIN + points_per_symbol_2(curr_game_moves))
            if win_2(curr_game_moves)
            else (
                POINTS_DRAW + points_per_symbol_2(curr_game_moves)
                if draw_2(curr_game_moves)
                else POINTS_LOSE + points_per_symbol_2(curr_game_moves)
            )
        )

win_1 = win(1)
draw_1 = draw(1)
points_per_symbol_1 = points_per_symbol(1)

win_2 = win(2)
draw_2 = draw(2)
points_per_symbol_2 = points_per_symbol(2)
points_1 = points(1)
points_2 = points(2)

data: list = [x for x in open("day2.txt", "r").read().split("\n") if x]
solution: dict = {
    "solution_1": sum([points_1(y) for y in data]),
    "solution_2": sum([points_2(y) for y in data]),
}
print(f"solution 1: {solution['solution_1']}")
print(f"solution 2: {solution['solution_2']}")

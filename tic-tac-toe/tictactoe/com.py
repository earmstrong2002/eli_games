from globals import *
import logic
from random import choice


def move(player: str):
    regs = logic.registers()

    winning_spot = find_win(regs, player)
    if winning_spot is not None:
        return winning_spot

    blocking_spot = find_block(regs, player)
    if blocking_spot is not None:
        return blocking_spot

    threatening_moves = find_threatening_moves(regs, player)
    if len(threatening_moves) > 0:
        return max(threatening_moves, key=lambda a: threatening_moves.count(a))

    middle_spot = 4
    if board[middle_spot] == blank:
        return middle_spot

    corners = logic.corners()
    if blank in corners:
        return corner_indices[corners.index(blank)]

    return choice(logic.valid_moves())


def find_win(regs: tuple, player: str) -> int:
    for i in range(len(regs)):
        if regs[i].count(player) == 2 and blank in regs[i]:
            return reg_indices[i][regs[i].index(blank)]

    return None


def find_block(regs: tuple, player: str) -> int:
    for i in range(len(regs)):
        if player not in regs[i] and regs[i].count(blank) == 1:
            return reg_indices[i][regs[i].index(blank)]

    return None


def find_threatening_moves(regs: tuple, player: str) -> int:
    threatening_moves = []
    for i in range(len(regs)):
        if player in regs[i] and regs[i].count(blank) == 2:
            threatening_moves.append(reg_indices[i][regs[i].index(blank)])

    return tuple(threatening_moves)

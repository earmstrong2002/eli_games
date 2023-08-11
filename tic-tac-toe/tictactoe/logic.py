from globals import *


def evaluate() -> str:
    winner = find_winner()
    if winner:
        return winner

    if is_full():
        return "draw"

    return None


def find_winner():
    for reg in registers():
        reg_winner = read_reg_winner(reg)
        if reg_winner:
            return reg_winner

    return None


def registers() -> tuple:
    return (*rows(), *columns(), *diagonals())


def rows():
    rows = []
    for row_index in range(side_length):
        row = []
        for column_index in range(side_length):
            index = row_index * side_length + column_index
            row.append(board[index])

        rows.append(tuple(row))

    return tuple(rows)


def columns():
    columns = []
    for column_index in range(side_length):
        column = []
        for row_index in range(side_length):
            index = column_index + row_index * side_length
            column.append(board[index])

        columns.append(tuple(column))

    return tuple(columns)


def diagonals():
    nwse_diag = []
    nesw_diag = []
    for i in range(side_length):
        nwse_diag.append(board[(side_length + 1) * i])
        nesw_diag.append(board[(side_length - 1) * i])

    return (tuple(nwse_diag), tuple(nesw_diag))


def valid_moves():
    valid_moves = []
    for i in range(len(board)):
        if board[i] == " ":
            valid_moves.append(i)

    return valid_moves


def read_reg_winner(reg: tuple) -> str:
    first = reg[0]
    if first == " ":
        return False

    for spot in reg[1:]:
        if spot != first:
            return False

    return first


def is_full() -> bool:
    return " " not in board

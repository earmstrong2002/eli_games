from globals import *


def move(player) -> int:
    while True:
        read = input(f"{player} to move: ").casefold()
        if not is_valid_input(read):
            # TODO write better error messages for this
            print("Could not parse input.")
            print("Please enter a letter/number pair (e.g. A3 or B1)")
            continue

        move = parse_input(read)
        if not is_valid_move(move):
            print("Invalid move.")
            continue

        break

    return move


def gamemode() -> str:
    print("Choose your gamemode:")
    print("    1.) Single-player (against computer)")
    print("    2.) Two-player")

    while True:
        match input("> "):
            case "1":
                return "1p"
            case "2":
                return "2p"
            case _:
                print("Invalid input. Please enter 1 or 2.")


def is_valid_input(input: str) -> bool:
    if len(input) != 2:
        return False

    for char in input:
        if char not in "abc123":
            return False

    return True


def parse_input(input: str) -> int:
    parser = {"a": 0, "b": 1, "c": 2, "1": 0, "2": 3, "3": 6}
    spot_index = 0

    for char in input:
        spot_index += parser[char]

    return spot_index


def is_valid_move(move: int) -> bool:
    return board[move] == blank

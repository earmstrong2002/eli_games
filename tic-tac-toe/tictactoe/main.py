from globals import *
import get
import logic
import com
from random import randint


def main():
    gamemode = get.gamemode()

    match gamemode:
        case "1p":
            single_player_game()
        case "2p":
            two_player_game()


def single_player_game():
    coin_toss = randint(0, 1)
    player = players[coin_toss]
    computer = players[not coin_toss]

    while True:
        winner = player_turn(player)
        if winner is not None:
            break

        winner = com_turn(computer)
        if winner is not None:
            break

    draw_board()


def two_player_game():
    coin_toss = randint(0, 1)
    player_1 = players[coin_toss]
    player_2 = players[not coin_toss]

    while True:
        winner = player_turn(player_1)
        if winner is not None:
            break

        winner = player_turn(player_2)
        if winner is not None:
            break

    draw_board()


def player_turn(player: str) -> str:
    draw_board()

    move = get.move(player)
    board[move] = player

    return logic.evaluate()


def com_turn(player: str) -> str:
    draw_board()

    move = com.move(player)
    board[move] = player

    return logic.evaluate()


def draw_board():
    print("{}{}{}\n{}{}{}\n{}{}{}".format(*board))


if __name__ == "__main__":
    main()

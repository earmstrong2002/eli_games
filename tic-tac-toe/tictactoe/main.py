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

        draw_board()

        move = com.move()
        board[move] = computer

        winner = logic.evaluate()
        if winner is not None:
            break

    draw_board()


def two_player_game():
    turn = 0
    coin_toss = randint(0, 1)
    is_over = False

    while True:
        active_player = players[(turn + coin_toss) % 2]
        turn += 1
        winner = player_turn(active_player)
        if winner is not None:
            break

    draw_board()


def player_turn(player: str) -> str:
    draw_board()

    move = get.move(player)
    board[move] = player

    winner = logic.evaluate()

    return winner


def draw_board():
    print("{}{}{}\n{}{}{}\n{}{}{}".format(*board))


if __name__ == "__main__":
    main()

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
    is_over = False

    while not is_over:
        draw_board()

        move = get.move(player)
        board[move] = player

        winner = logic.evaluate()
        is_over = winner
        if is_over:
            break

        draw_board()

        move = com.move()
        board[move] = computer

        winner = logic.evaluate()
        is_over = winner

    draw_board()


def two_player_game():
    turn = 0
    coin_toss = randint(0, 1)
    is_over = False

    while not is_over:
        draw_board()

        active_player = players[(turn + coin_toss) % 2]
        turn += 1
        move = get.move(active_player)
        board[move] = active_player

        winner = logic.evaluate()
        is_over = winner

    draw_board()


def draw_board():
    print("{}{}{}\n{}{}{}\n{}{}{}".format(*board))


if __name__ == "__main__":
    main()

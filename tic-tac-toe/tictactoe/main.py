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
    
    if computer == X:
        winner = com_turn(computer)

    while winner is None:
        winner = player_turn(player)
        if winner is not None:
            break

        winner = com_turn(computer)

    draw_board()


def two_player_game():
    player_1 = X
    player_2 = O

    while winner is None:
        winner = player_turn(player_1)
        if winner is not None:
            break

        winner = player_turn(player_2)

    draw_board()


def player_turn(player: str) -> str:
    draw_board()
    print(f"{player} to move. (Enter move)")

    move = get.move(player)
    board[move] = player

    return logic.evaluate()


def com_turn(player: str) -> str:
    draw_board()
    print(f"{player} to move (Computer's move. Press enter.)")
    input()

    move = com.move(player)
    board[move] = player

    return logic.evaluate()


def draw_board():
    board_ascii = "  A B C\n"
    board_ascii += "1 {}|{}|{}\n"
    board_ascii += "  -+-+-\n"
    board_ascii += "2 {}|{}|{}\n"
    board_ascii += "  -+-+-\n"
    board_ascii += "3 {}|{}|{}\n"
    print(board_ascii.format(*board))


if __name__ == "__main__":
    main()

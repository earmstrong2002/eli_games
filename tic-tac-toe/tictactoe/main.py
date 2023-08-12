from globals import *
import get
import logic
import com
from random import randint


def main():
    gamemode = get.gamemode()
    board = [blank] * side_length**2

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
        com_turn(computer)

    while True:
        winner = player_turn(player)
        if winner is not None:
            break

        winner = com_turn(computer)
        if winner is not None:
            break

    game_over(winner)


def two_player_game():
    player_1 = X
    player_2 = O

    while True:
        winner = player_turn(player_1)
        if winner is not None:
            break

        winner = player_turn(player_2)
        if winner is not None:
            break

    game_over(winner)


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


def game_over(winner: str) -> None:
    draw_board()
    match winner:
        case "draw":
            print("Tie game! Well played.")
        case "X":
            print("Xtra Xtra, read all about it! X wins!")
        case "O":
            print("O my gosh, O wins!")
            
    if get.play_again():
        main()


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

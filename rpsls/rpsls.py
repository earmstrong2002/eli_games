import random as rand
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
from sys import platform


class Move:
    def __init__(self, title, beats=None, actions=None, texture=None):
        self.beats = beats
        self.title = title
        self.actions = actions
        self.texture = texture

    def __str__(self):
        return self.title


# instantiates Move objects
def initialize_moves():
    """
    Instantiates all attributes of each of the five instances
    of the Move dataclass.
    """
    global ROCK
    global PAPER
    global SCISSORS
    global LIZARD
    global SPOCK
    global MOVES

    ROCK = Move("rock")
    PAPER = Move("paper")
    SCISSORS = Move("scissors")
    LIZARD = Move("lizard")
    SPOCK = Move("spock")

    # list for iterating through all moves
    MOVES = [ROCK, PAPER, SCISSORS, LIZARD, SPOCK]

    # defining which moves each move beats
    ROCK.beats = (SCISSORS, LIZARD)
    PAPER.beats = (ROCK, SPOCK)
    SCISSORS.beats = (PAPER, LIZARD)
    LIZARD.beats = (PAPER, SPOCK)
    SPOCK.beats = (ROCK, SCISSORS)

    # defining what verb to use when each move beats each other move
    ROCK.actions = ("crushes", "crushes")
    PAPER.actions = ("covers", "disproves")
    SCISSORS.actions = ("cuts", "decapitates")
    LIZARD.actions = ("eats", "poisons")
    SPOCK.actions = ("vaporizes", "smashes")

    # get file directories for associated move textures
    pths_textures = list(Path("rpsls/textures/").glob("*"))
    strs_textures = []
    for pth in pths_textures:  # convert path objects to strings for processing
        strs_textures.append(str(pth))
    if platform.startswith("win"):  # replace \ with / for compatability
        for i in range(len(strs_textures)):
            strs_textures[i] = strs_textures[i].replace("\\", "/")

    filenames_textures = []
    for pth in strs_textures:  # isolate file name, without extension
        im_name = pth.split("/")[-1][:-4]
        filenames_textures.append(im_name)

    # assign textures to appropriate move objects
    for move in MOVES:
        index = filenames_textures.index(move.title)
        move.texture = Image.open(pths_textures[index])


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.geometry('600x360')
        self.title("Play R.P.S.L.S.")
        self.resizable(0, 0)  # not resizeable, for simplicity
        # TODO add GRAPHICS
        self.make_widgets()

    def make_widgets(self):
        '''Defines and places all widgets'''
        # configure primary frame
        self.frm_main = ttk.Frame(self)
        self.frm_main.columnconfigure(0, weight=1)
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.rowconfigure(1, weight=0, minsize=60)
        self.frm_main.pack(fill="both", expand=True)

        # populate with elements
        self.make_display()
        self.make_move_picker()

    def make_display(self):
        '''Defines and places all widgets concerning the display'''
        # configure frame for display
        self.frm_display = ttk.Frame(self.frm_main)
        self.frm_display.columnconfigure(
            (0, 1, 2), weight=1, pad=5, minsize=250
        )
        self.frm_display.rowconfigure(0, weight=0, minsize=40, pad=5)
        self.frm_display.rowconfigure(1, weight=1, minsize=250)
        self.frm_display.grid(
            column=0,
            row=0,
            sticky="nsew",
        )

        # scoreboard
        self.scoreboard = tk.StringVar(
            value=f"{rps.player_wins} -- {rps.draws} -- {rps.com_wins}"
        )
        self.lbl_scoreboard = ttk.Label(
            self.frm_display, textvariable=self.scoreboard, anchor="center"
        )
        self.lbl_scoreboard.grid(column=1, row=0)

        # player label
        self.lbl_player = ttk.Label(self.frm_display, text="Player")
        self.lbl_player.grid(column=0, row=0, sticky="e")

        # computer label
        self.lbl_com = ttk.Label(self.frm_display, text="Computer")
        self.lbl_com.grid(column=2, row=0, sticky="w")

        # outcome message
        self.outcome_message = tk.StringVar()
        self.lbl_outcome = ttk.Label(
            self.frm_display,
            textvariable=self.outcome_message,
            anchor="center",
            width=43,
        )
        self.lbl_outcome.grid(column=1, row=1, sticky="nsew")
        self.make_graphics()

    # Display appropriate images for player and com moves
    def make_graphics(self):
        '''Defines and places all widgets concerning image graphics'''
        # label for player move
        self.lbl_player_move = ttk.Label(self.frm_display)
        self.lbl_player_move.grid(column=0, row=1)

        # label for com move
        self.lbl_com_move = ttk.Label(self.frm_display)
        self.lbl_com_move.grid(column=2, row=1)

    def update_display(
        self, player_wins, draws, com_wins, victor, player_move, com_move, verb
    ) -> None:
        '''Update all variable elements of the GUI'''
        self.update_scoreboard(player_wins, draws, com_wins)
        self.display_outcome_message(victor, player_move, com_move, verb)
        self.display_move_textures(player_move, com_move)

    def update_scoreboard(self, player_wins, draws, com_wins):
        self.scoreboard.set(f"{player_wins} -- {draws} -- {com_wins}")

    def display_outcome_message(
        self, victor, player_move, com_move, verb
    ) -> None:
        '''Sets self.outcome_message depending on how the round played out'''
        message = ""
        match victor:
            case "draw":
                message = "It's a draw!"
            case "player":
                message = f"Player wins! {player_move.title.capitalize()} "
                message += f"{verb} {com_move.title.capitalize()}"
            case "com":
                message = f"Computer wins! {com_move.title.capitalize()} "
                message += f"{verb} {player_move.title.capitalize()}"
            case _:  # something is terribly wrong
                raise ValueError()
        self.outcome_message.set(message)

    def display_move_textures(self, player_move, com_move) -> None:
        '''Draws appropriate textures onto lbl_player_move and lbl_com_move'''
        # set texture for player move
        img_player_move = ImageTk.PhotoImage(player_move.texture)
        self.lbl_player_move.configure(image=img_player_move)
        self.lbl_player_move.image = img_player_move

        # set texture for com move
        img_com_move = ImageTk.PhotoImage(com_move.texture)
        self.lbl_com_move.configure(image=img_com_move)
        self.lbl_com_move.image = img_com_move
        
    def make_move_picker(self):
        '''Defines and draws all widgets concerning move selection'''
        # configure frame for move picker
        self.frm_move_picker = ttk.LabelFrame(
            self.frm_main, text="Pick Your Move", labelanchor="n"
        )
        self.frm_move_picker.rowconfigure(0, weight=1, pad=5)
        self.frm_move_picker.columnconfigure((0, 1, 2, 3, 4), weight=1, pad=5)
        self.frm_move_picker.grid(column=0, row=1, sticky="nsew")

        # populate move picker
        # TODO make move button constructor modular
        btn_rock = ttk.Button(
            self.frm_move_picker,
            text="ROCK",
            command=lambda: rps.run_game(ROCK),
        )
        btn_rock.grid(column=0, row=0, sticky="nsew")
        btn_paper = ttk.Button(
            self.frm_move_picker,
            text="PAPER",
            command=lambda: rps.run_game(PAPER),
        )
        btn_paper.grid(column=1, row=0, sticky="nsew")
        btn_scissors = ttk.Button(
            self.frm_move_picker,
            text="SCISSORS",
            command=lambda: rps.run_game(SCISSORS),
        )
        btn_scissors.grid(column=2, row=0, sticky="nsew")
        btn_lizard = ttk.Button(
            self.frm_move_picker,
            text="LIZARD",
            command=lambda: rps.run_game(LIZARD),
        )
        btn_lizard.grid(column=3, row=0, sticky="nsew")
        btn_spock = ttk.Button(
            self.frm_move_picker,
            text="SPOCK",
            command=lambda: rps.run_game(SPOCK),
        )
        btn_spock.grid(column=4, row=0, sticky="nsew")


class Rps:
    '''
    A semi-modular class for playing rock-paper-scissors variants.
    Future versions will be fully modular such that any simple variation of
    rock-paper-scissors can be played with this module.
    i.e. Any number of moves will be supported and configurable, from
    ordinary rock-paper-scissors, to the legendary RPS-15
    '''
    def __init__(self):
        self.player_history = {
            ROCK: 1,
            PAPER: 1,
            SCISSORS: 1,
            LIZARD: 1,
            SPOCK: 1
        }
        self.player_wins = 0
        self.draws = 0
        self.com_wins = 0

    # TODO refactor Rps.com_decide
    # rather than rebuilding confidence list every round,
    # store confidence list as class attribute and adjust it
    # each round according to player's most recent move
    def com_decide(self) -> Move:
        '''
        com_decide's algorithm takes into account all the moves the player
        has chosen in the current session.
        We loop through each move and look up how many times the player
        has played moves that are in move.beats (i.e. moves that beat
        the move we're looking into in the current iteration of the loop)
        We store that sum in play_count, then append it to the confidence list.
        At the end of that, confidence is a list containing integers
        representing how confident the algorithm is that
        playing the move with the corresponding index would
        result in a win, assuming the player continues to
        favor whichever moves they have been favoring so far.
        We square each value in the confidence list in order to increase
        increase the contrast between more and less favorable moves.
        Finally, we return a random selection from the move list, weighted
        by our confidence list, such that the computer is more likely
        to choose a move that is more likely to win.
        
        In practice, this algorithm does very little to make the computer win
        more and I likely won't include it in the final build.
        '''
        # build map of best options stored in confidence
        confidence = []
        for move in MOVES:
            play_count = 0
            for i in move.beats:
                # increment play_count for move by number of times
                # player has played move in move.beats
                play_count += self.player_history[i]
            confidence.append(play_count)
        for i in range(len(confidence)):
            confidence[i] = confidence[i] ** 2
        # randomly choose an option, weighted by play quality
        return rand.choices(MOVES, weights=confidence, k=1)[0]

    def evaluate_victor(self, player_move, com_move):
        '''Compares player_move and com_move and determines who wins and what
        verb to use in the outcome message'''
        if com_move is player_move:
            action = None
            victor = "draw"
        elif com_move in player_move.beats:
            action = player_move.actions[player_move.beats.index(com_move)]
            victor = "player"
        else:  # computer wins
            action = com_move.actions[com_move.beats.index(player_move)]
            victor = "com"
        return victor, action

    def increment_scoreboard(self, player_move, victor) -> None:
        '''Increments values concerning scorekeeping'''
        self.player_history[player_move] += 1
        match victor[0][0]:
            case "p":
                self.player_wins += 1
            case "c":
                self.com_wins += 1
            case "d":
                self.draws += 1

    def run_game(self, player_move):
        '''Controls flow of the program to execute a full round of rpsls'''
        print(f"player_move = {player_move}")
        com_move = self.com_decide()
        print(f"com_move = {com_move}")
        victor, verb = self.evaluate_victor(player_move, com_move)
        print(f"victor = {victor}")
        print(f"verb = {verb}")
        self.increment_scoreboard(player_move, victor)
        root.update_display(
            self.player_wins,
            self.draws,
            self.com_wins,
            victor,
            player_move,
            com_move,
            verb
        )


def main():
    initialize_moves()
    for move in MOVES:
        print(move.texture.filename)
    global rps
    global root
    rps = Rps()
    root = App()
    root.mainloop()


if __name__ == "__main__":
    main()

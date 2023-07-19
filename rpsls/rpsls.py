import random as rand
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import Path
import json


class Move:
    def __init__(self, title, beats=None, texture=None):
        self.beats = beats
        self.title = title
        self.texture = texture

    def __str__(self):
        return self.title


# instantiates Move objects
def initialize_moves() -> None:
    """Instantiates all attributes of all moves from move_config.json"""

    # read move properties form move_config.json
    with open("rpsls/move_config.json", "r") as cfg:
        big_dict = json.load(cfg)
        print("Gamemode options:")
        gamemode_list = list(big_dict.keys())
        print(gamemode_list)
        gamemode = input("Select gamemode: ")
        move_dict = big_dict[gamemode]

    global MOVES  # list of Move objects for global access
    MOVES = instantiate_moves(list(move_dict.keys())[1:])
    move_key = build_move_key(MOVES)

    # populate move.beats attributes
    for move in MOVES:
        move.beats = generate_beats_dict(move, move_dict[move.title], move_key)

    # populate move.texture attributes
    if move_dict["has_textures"] == True:
        textures = fetch_textures(move_key, gamemode)
        for move in MOVES:
            move.texture = textures[move]


def fetch_textures(move_key: dict, gamemode: str) -> dict:
    """Searches dir for textures for all moves,
    creates Image object of each texture,
    returns dict; keys are Move objects, values are Image objects.
    """
    pths_textures = list(Path(f"rpsls/textures/{gamemode}").glob("*.png"))
    textures = {}
    for path in pths_textures:
        # generate Image object with path
        img = Image.open(path)
        # add corresponding move object to textures with Image object as value
        textures[move_key[path.stem]] = img

    return textures


def generate_beats_dict(
    move: Move, str_dict_beats: dict, move_key: dict
) -> dict:
    """str_dict keys are move titles as str.
    This function replaces the str with appropriate move object"""
    beats = {}
    for item in str_dict_beats.items():
        obj = move_key[item[0]]
        beats[obj] = item[1]

    return beats


def build_move_key(moves: list) -> dict:
    """Returns dict; keys are move titles as str, values are Move objects."""
    move_key = {}
    for move in moves:
        move_key[move.title] = move

    return move_key


def instantiate_moves(move_strs: list) -> list:
    """Returns list of move objects for all moves in move_strs"""
    moves = []
    for move in move_strs:
        exec(f"{move} = Move(title='{move}')")
        exec(f"moves.append({move})")

    return moves


class App(tk.Tk):
    # TODO once modularization is complete, add gamemode menu
    def __init__(self):
        super().__init__()
        # self.geometry('600x360')
        self.title("Play R.P.S.L.S.")
        self.resizable(0, 0)  # not resizeable, for simplicity
        self.make_widgets()

    def make_widgets(self) -> None:
        """Defines and places all widgets"""
        # configure primary frame
        self.frm_main = ttk.Frame(self)
        self.frm_main.columnconfigure(0, weight=1)
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.rowconfigure(1, weight=0, minsize=60)
        self.frm_main.pack(fill="both", expand=True)

        # populate with elements
        self.make_display()
        self.make_move_picker()

    def make_display(self) -> None:
        """Defines and places all widgets concerning the display"""
        # configure frame for display
        self.frm_display = ttk.Frame(self.frm_main)
        self.frm_display.columnconfigure(
            (0, 1, 2), weight=1, pad=5, minsize=260
        )
        self.frm_display.rowconfigure(0, weight=0, minsize=40, pad=5)
        self.frm_display.rowconfigure(1, weight=1, minsize=260)
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
        """Defines and places all widgets concerning image graphics"""
        # label for player move
        self.lbl_player_move = ttk.Label(self.frm_display)
        self.lbl_player_move.grid(column=0, row=1)

        # label for com move
        self.lbl_com_move = ttk.Label(self.frm_display)
        self.lbl_com_move.grid(column=2, row=1)

    def update_display(
        self, player_wins, draws, com_wins, victor, player_move, com_move, verb
    ) -> None:
        """Update all variable elements of the GUI"""
        self.update_scoreboard(player_wins, draws, com_wins)
        self.outcome_message.set(
            self.message(victor, player_move, com_move, verb)
        )
        self.display_move_textures(player_move, com_move)

    def update_scoreboard(self, player_wins, draws, com_wins):
        self.scoreboard.set(f"{player_wins} -- {draws} -- {com_wins}")

    def message(self, victor, player_move, com_move, verb) -> None:
        """Sets self.outcome_message depending on how the round played out"""
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
        return message

    def display_move_textures(self, player_move, com_move) -> None:
        """Draws appropriate textures onto lbl_player_move and lbl_com_move"""
        # set texture for player move
        try:
            img_player_move = ImageTk.PhotoImage(player_move.texture)
            self.lbl_player_move.configure(image=img_player_move)
            self.lbl_player_move.image = img_player_move

            # set texture for com move
            img_com_move = ImageTk.PhotoImage(com_move.texture)
            self.lbl_com_move.configure(image=img_com_move)
            self.lbl_com_move.image = img_com_move
        except KeyError:
            pass  # swallow error to allow gamemodes with no textures

    def make_move_picker(self):
        """Defines and draws all widgets concerning move selection"""
        # configure frame for move picker
        self.frm_move_picker = ttk.LabelFrame(
            self.frm_main, text="Pick Your Move", labelanchor="n"
        )
        self.frm_move_picker.rowconfigure(0, weight=1, pad=5)
        self.frm_move_picker.grid(column=0, row=1, sticky="nsew")

        # populate move picker
        for move in MOVES:
            btn = f"btn_{move.title}"
            index = MOVES.index(move)
            self.frm_move_picker.columnconfigure(index, weight=1, pad=5)
            exec(f"{btn} = ttk.Button(self.frm_move_picker)")
            exec(f"{btn}['text'] = '{move.title.upper()}'")
            exec(f"{btn}['command'] = lambda: rps.run_game(MOVES[{index}])")
            exec(f"{btn}.grid(column = {index}, row=0, sticky='nsew')")


class Rps:
    """
    A semi-modular class for playing rock-paper-scissors variants.
    Future versions will be fully modular such that any simple variation of
    rock-paper-scissors can be played with this module.
    i.e. Any number of moves will be supported and configurable, from
    ordinary rock-paper-scissors, to the legendary RPS-15
    """

    def __init__(self):
        self.player_wins = 0
        self.draws = 0
        self.com_wins = 0
        self.com_confidence = {}  # used for deciding com move
        for move in MOVES:
            self.com_confidence[move] = 1

    def com_decide(self, player_move) -> Move:
        """
        Picks computer's move for the given round.
        self.com_confidence is a dict that for each possible move,
        stores ints representing abstractly how likely the key
        move is to win, if the player favors whatever moves
        they've been favoring thusfar in the session.
        More concretely, with each round, self.increment_scoreboard
        increments the com_confidence value of each move in
        player_move.beats by one.
        com_decide squares the values in com_confidence to
        accentuate the discrepancy between high and low values,
        then uses the new list, confidence, as weights for the random choice.
        """
        confidence = []  # for storing squared confidence values
        for i in self.com_confidence.values():
            confidence.append(1 / i**2)
        return rand.choices(MOVES, weights=confidence, k=1)[0]

    def evaluate_victor(self, player_move, com_move):
        """Compares player_move and com_move and determines who wins and what
        verb to use in the outcome message"""
        if com_move is player_move:
            action = None
            victor = "draw"
        elif com_move in player_move.beats:
            action = player_move.beats[com_move]
            victor = "player"
        else:  # computer wins
            action = com_move.beats[player_move]
            victor = "com"
        return victor, action

    def increment_scoreboard(self, victor, player_move) -> None:
        """Increments values concerning scorekeeping"""
        match victor:
            case "player":
                self.player_wins += 1
            case "com":
                self.com_wins += 1
            case "draw":
                self.draws += 1
            case _:  # something has gone horribly wrong
                raise ValueError()

        for move in player_move.beats:
            # increment confidence list with latest player move
            self.com_confidence[move] += 1

    def run_game(self, player_move):
        """Controls flow of the program to execute a full round of rpsls"""
        print(f"player_move = {player_move}")
        com_move = self.com_decide(player_move)
        print(f"com_move = {com_move}")
        victor, verb = self.evaluate_victor(player_move, com_move)
        print(f"victor = {victor}")
        print(f"verb = {verb}")
        self.increment_scoreboard(victor, player_move)
        root.update_display(
            self.player_wins,
            self.draws,
            self.com_wins,
            victor,
            player_move,
            com_move,
            verb,
        )


def main():
    # TODO gamemode picker
    # TODO gamemode maker
    initialize_moves()
    global rps
    global root
    rps = Rps()
    root = App()
    root.mainloop()


if __name__ == "__main__":
    main()

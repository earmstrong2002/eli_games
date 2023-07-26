import tkinter as tk
from tkinter import ttk
from random import choices as rand_choices
from PIL import ImageTk, Image
from pathlib import Path
from json import load as json_load
from os import rename
from math import sqrt


HERE = Path(__file__).parent.absolute()  # absolute path of current file


class Move:
    """
    Stores info relavent to Rps operations.
    - title stores move's name as str
    - beats stores dict[Move: str];
        - keys are moves that are beaten by self
        - values are the action that makes self beat the key
        - e.g. rock.beats == {scissors, "crushes"}  # rock crushes scissors
    - texture stores Image object with associated texture
        - note: move textures are to be stored with the following format:
        - directory: textures/relaventgamemode/
        - file name: movetitle.png
        - size: 250x250
    """

    def __init__(
        self, title: str, beats: dict | None = {}, texture=None
    ) -> None:
        self.title = title
        self.beats = beats
        self.texture = texture

    def __repr__(self):
        return self.title


class Rps:
    """A class that serves as a game engine
    for variants of rock, paper, scissors."""

    def __init__(self, gamemode: dict):
        self.gamemode = gamemode["title"]
        self.alias = gamemode["alias"]
        self.moves = self._initialize_moves(gamemode["moves"])
        self.wins = {"player": 0, "draw": 0, "com": 0}
        self.com_confidence = self._initialize_com_confidence()

    def __repr__(self):
        return self.gamemode

    def _initialize_com_confidence(self) -> dict[Move, int]:
        """Creates com_confidence dict. All values are initialized to 1."""
        com_confidence = {}
        for move in self.moves:
            com_confidence[move] = 1
        return com_confidence

    def _initialize_moves(self, move_dict: dict) -> list[Move]:
        """Creates and configures Move object for each move in move_list"""
        moves = self._instantiate_moves(move_dict)
        move_key = self._build_move_key(moves)
        # Populate Move object attributes
        moves = self._populate_beats(moves, move_key, move_dict)
        moves = self._populate_textures(moves, move_key)
        return moves

    def _instantiate_moves(self, move_list: dict) -> list[Move]:
        """
        Instantiates Move object for each move in move_list.
        Move objects are "naked" because they have only title. No other data.
        """
        naked_moves = []
        for move in move_list:
            exec(f"{move} = Move(title='{move}')")
            exec(f"naked_moves.append({move})")
        return naked_moves

    def _build_move_key(self, moves: list[Move]) -> dict[str, Move]:
        """Returns dict for locating Move object with given title"""
        move_key = {}
        for move in moves:
            move_key[move.title] = move
        return move_key

    def _populate_beats(
        self, moves: list[Move], move_key: dict[str, Move], move_dict: dict
    ) -> dict[str, Move]:
        """Assigns beats attribute to all moves in move_key."""
        for move in moves:
            beats = {}
            # locate relevant data in move_dict
            unformatted_beats = move_dict[move.title]
            for key in unformatted_beats:
                # locate Move corresponding Move object
                move_object = move_key[key]
                # add Move object and verb to beats
                beats[move_object] = unformatted_beats[key]
            move.beats = beats
        return moves

    def _populate_textures(
        self, moves: list[Move], move_key: dict[str, Move]
    ) -> dict[str, Move]:
        """
        Assigns texture attribute to Move objects.
        Note: All textures present in gamemode's texture folder
        will be processed, not necessarily every move
        in the gamemode.
        """
        pths_textures = list(
            Path(HERE / "textures" / self.gamemode).glob("*.png")
        )
        for path in pths_textures:
            # instantiate Image object with path
            img = Image.open(path)
            try:
                # locate corrisponding move
                current_move = move_key[path.stem]
            except KeyError:
                # texture file is either misnamed
                # or does not belong in current gamemode.
                # mark bad file invalid.
                rename(path.name, "INVALID__" + str(path.name))
            # assign img to move's texture attribute
            move_index = moves.index(current_move)
            moves[move_index].texture = img
        return moves

    def run_game(self, player_move: Move) -> None:
        """Controls the flow of game."""
        print("player_move.beats: " + str(player_move.beats))
        com_move = self._com_decide()
        print("com_move.beats: " + str(com_move.beats))
        victor = self._get_victor(player_move, com_move)
        print("victor: " + victor)
        outcome_message = self._get_outcome_message(
            player_move, com_move, victor
        )
        # update self.wins and self.com_confidence
        self._scorekeeping(player_move, victor)
        return com_move, outcome_message

    def _com_decide(self) -> Move:
        """
        Chooses computer's move.
        self.com_confidence stores Moves as keys and their values
        represent the number of times the player has played moves
        that beat the key move, initialized at 1 instead of 0
        to avoid division by 0. If the player favors some moves over
        other moves, the computer will pick up on that
        and punish them for it.
        """
        confidence = []  # storage for frobbed self.com_confidence values
        for i in self.com_confidence.values():
            # square values to emphasize disparity between high and low values.
            # take the reciprocal so that higher self.com_confidence values
            #   correspond to lower weights.
            confidence.append(1 / i**2)
        # randomly choose, weighted by squared confidence values.
        print("self.moves: " + str(self.moves))
        return rand_choices(self.moves, weights=confidence, k=1)[0]

    def _get_victor(self, player_move: Move, com_move: Move) -> str:
        """Determines round victor based on player and com moves."""
        if com_move is player_move:
            return "draw"
        if com_move in player_move.beats:
            return "player"
        else:  # computer wins
            return "com"

    def _get_outcome_message(
        self, player_move: Move, com_move: Move, victor
    ) -> str:
        """Generates outcome message e.g. "Scissors cuts Paper" """
        # determine which Move won
        match victor:
            case "draw":  # no need to generate message, return early.
                return "It's a draw!"
            case "player":
                winner = player_move
                loser = com_move
            case _:  # com_move won
                winner = com_move
                loser = player_move
        # determine verb to be used in message
        verb = winner.beats[loser]
        # format and return message
        return "{} wins! {} {} {}.".format(
            victor.capitalize(), winner.title.capitalize(), verb, loser.title
        )

    def _scorekeeping(self, player_move: Move, victor: str) -> None:
        """Updates self.wins and self.com_confidence with round outcome"""
        # increment self.wins
        self.wins[victor] += 1
        # increment self.com_confidence
        for move in player_move.beats.keys():
            self.com_confidence[move] += 1


class App(tk.Frame):
    """App dynamically generates a GUI based on the gamemode information
    stored in the Rps engine passed App's initializer."""

    def __init__(self, master) -> None:
        super().__init__()
        self.master = master
        self._vars_init()
        self._make_widgets()

    def _vars_init(self) -> None:
        """Initializes tk variables"""
        # scoreboard StringVar
        wins = rps.wins
        self.scoreboard = tk.StringVar(
            value="{} -- {} -- {}".format(
                wins["player"], wins["draw"], wins["com"]
            )
        )
        self.outcome_message = tk.StringVar()

    def _make_widgets(self) -> None:
        """Generates all widgets"""
        self._configure_frame()
        self._make_display()
        self._make_move_picker()

    def _configure_frame(self) -> None:
        """Configures and packs self to root"""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=2, minsize=60)
        self.pack(fill="both", expand=True)

    def _make_display(self) -> None:
        """Assembles frame containing widgets for displaying game info"""
        frm_display = self._make_frm_display()
        self._make_scoreboard(master=frm_display)
        self._make_player_labels(master=frm_display)
        self._make_message_label(master=frm_display)
        self._make_graphics(master=frm_display)

    def _make_frm_display(self) -> ttk.Frame:
        """Initializes and configures display frame"""
        frm_display = ttk.Frame(
            self,
        )
        frm_display.columnconfigure((0, 1, 2), weight=1, minsize=250)
        frm_display.rowconfigure(0, weight=0, minsize=40)
        frm_display.rowconfigure(1, weight=1, minsize=250)
        frm_display.grid(column=0, row=0, sticky="nsew")
        return frm_display

    def _make_scoreboard(self, master: tk.Frame) -> None:
        """Initializes and configures scoreboard"""
        lbl_scoreboard = ttk.Label(
            master, textvariable=self.scoreboard, anchor="center"
        )
        lbl_scoreboard.grid(column=1, row=0, sticky="nsew")

    def _make_player_labels(self, master) -> None:
        """Makes the "player" and "computer" labels"""
        # player label
        lbl_player = ttk.Label(master, text="PLAYER", anchor="center")
        lbl_player.grid(column=0, row=0, sticky="nsew")
        # computer label
        lbl_com = ttk.Label(
            master,
            text="COMPUTER",
            anchor="center",
        )
        lbl_com.grid(column=2, row=0, sticky="nsew")

    def _make_message_label(self, master) -> None:
        """Makes the label that displays the outcome message"""
        lbl_message = ttk.Label(
            master, textvariable=self.outcome_message, anchor="center"
        )
        lbl_message.grid(column=1, row=1, sticky="nsew")

    def _make_graphics(self, master: ttk.Label) -> None:
        """Makes the labels for move textures"""
        # player move image label
        self.lbl_player_move = ttk.Label(master)
        self.lbl_player_move.grid(column=0, row=1, sticky="nsew")

        # com move image label
        self.lbl_com_move = ttk.Label(master)
        self.lbl_com_move.grid(column=2, row=1, sticky="nsew")

    def _make_move_picker(self) -> None:
        """
        Dynamically makes move picker; button decoration, funcion, and layout
        determined by number of moves in current gamemode
        """
        layout = self._get_btn_layout()
        frm_buttons = self._make_frm_buttons(layout)
        self._make_buttons(frm_buttons, layout)

    def _get_btn_layout(self) -> dict:
        """Determines row length and count based on length of rps.move"""
        count = len(rps.moves)
        columns = int(sqrt(count)) + 1
        rows = count // columns
        if count % columns != 0:
            rows += 1
        return {"columns": columns, "rows": rows}

    def _make_frm_buttons(self, layout: dict[str, int]) -> None:
        """Instantiates and configures frame for move buttons"""
        frm_buttons = ttk.Frame(self)
        frm_buttons.rowconfigure(to_range(layout["rows"]), weight=1)
        frm_buttons.columnconfigure(0, weight=1)
        frm_buttons.grid(column=0, row=1, sticky="nsew")
        return frm_buttons

    def _make_buttons(self, master, layout) -> None:
        """Dynamically creates ttk.Button objects based on rps.moves"""
        moves = rps.moves
        move_index = 0
        for row in range(layout["rows"]):
            # configure sub-frame
            frm_row = ttk.Frame(master, name=f"frm_row_{row}")
            for column in range(layout["columns"]):
                if move_index < len(moves):
                    frm_row.columnconfigure(
                        column,
                        weight=1,
                        minsize=750 // layout["columns"],
                    )
                    self._make_button(
                        master=frm_row,
                        move=moves[move_index],
                        column=column,
                        row=row,
                    )
                else:
                    break
                move_index += 1
            frm_row.grid(column=0, row=row, sticky="nsew")

    def _make_button(self, master, move, column, row) -> None:
        """Creates button object with the given move, grids to given spot."""
        btn_move = ttk.Button(
            master,
            name=f"btn_{move.title}",
            text=f"{move.title.upper()}",
            command=lambda: self._handle_move_button(move),
        )
        btn_move.grid(column=column, row=row, sticky="nsew")

    def _handle_move_button(self, player_move):
        """Runs game of rps and updates display accordingly"""
        # run game and retrieve data
        com_move, outcome_message = rps.run_game(player_move)

        self._show_move_textures(player_move, com_move)
        self.outcome_message.set(outcome_message)
        self.scoreboard.set(
            "{} -- {} -- {}".format(
                rps.wins["player"], rps.wins["draw"], rps.wins["com"]
            )
        )

    def _show_move_textures(self, player_move, com_move):
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


def _make_root(default_gamemode: str) -> None:
    """Instantiates and configures root window with menu bar."""
    global root
    root = tk.Tk()
    root.minsize(750, 400)
    root.style = ttk.Style()
    root.style.theme_use("clam")

    configure_root_window(default_gamemode)
    _make_menu_bar(MOVE_CONFIG["gamemodes"])


def _make_menu_bar(gamemodes: str) -> None:
    """Creates menu bar slaved to root."""
    menu_bar = tk.Menu(root)
    mnu_options = tk.Menu(menu_bar, tearoff=0)
    mnu_gamemodes = _make_mnu_gamemodes(mnu_options, gamemodes)

    mnu_options.add_cascade(label="Select Gamemode", menu=mnu_gamemodes)
    menu_bar.add_cascade(label="Options", menu=mnu_options)
    root.config(menu=menu_bar)


def _make_mnu_gamemodes(master, gamemodes: list) -> tk.Menu:
    """
    Creates tkinter menu for switching gamemodes.
    The returned menu has one command per gamemode in gamemodes;
    each command calls change_gammeode and passes it
    the appropriate gamemode.
    """
    mnu_gamemodes = tk.Menu(master, tearoff=0)
    for gamemode in gamemodes.items():
        # add command to switch to gamemode
        command = "mnu_gamemodes.add_command(label='{}', command={})"
        command = command.format(
            gamemode[1]["alias"], f"lambda: change_gamemode('{gamemode[0]}')"
        )
        print(command)
        exec(command, globals(), locals())
        # mnu_gamemodes.add_command(
        #     label=gamemode[1]["alias"],
        #     command=lambda: change_gamemode(gamemode[0]),
        # )
    return mnu_gamemodes


def configure_root_window(gamemode) -> None:
    """Configures geometry, title, and icon of root window."""
    active_gamemode_alias = gamemode["alias"]
    root.title(f"Play {active_gamemode_alias}")
    with Image.open(HERE / "icon.png") as open_img:
        open_img.resize((16, 16))
        icon = ImageTk.PhotoImage(open_img)
    root.wm_iconphoto(True, icon)


def _start_game(gamemode: str) -> None:
    """Instantiates Rps engine and App frame with given gamemode."""
    global rps
    global app
    rps = Rps(gamemode)
    app = App(root)


def to_range(num: int) -> tuple:
    range_list = []
    for i in range(num):
        range_list.append(i)
    return tuple(range_list)


def change_gamemode(gamemode: str) -> None:
    """
    Changes gamemode by destroying currently active instances of
    Rps and App and reinstantiating them with the given gamemode.
    """
    global rps
    global app
    # destroy packed widgets
    app.pack_forget()
    # destroy class instances
    del rps
    del app
    print(gamemode)
    _start_game(_get_gamemode(gamemode))


def _get_move_config() -> dict:
    """Reads move_config.json and returns dict with the info"""
    global MOVE_CONFIG
    with open(HERE / "move_config.json") as cfg:
        MOVE_CONFIG = json_load(cfg)


def _get_gamemode(gamemode: str) -> dict:
    """Separates gamemode info from greater MOVE_CONFIG dict."""
    return MOVE_CONFIG["gamemodes"][gamemode]


def main():
    # TODO add gamemode maker
    # TODO add rules view
    _get_move_config()
    default_gamemode = _get_gamemode(MOVE_CONFIG["default_gamemode"])
    _make_root(default_gamemode)
    _start_game(default_gamemode)
    root.mainloop()


if __name__ == "__main__":
    main()

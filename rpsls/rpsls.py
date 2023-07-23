"""
Intended Structure:
- main
    - loads move_config.json
    - calls helper function to create root window with gamemodes
    - calls start_game with default gamemode
        - calls helper function to instantiate global Rps with default gamemode
        - instantiates global App, which inherits from Rps and makes frame
            slaved to root
    - initiates root.mainloop()
    
- change_gamemode
    - accepts target_gamemode,
    - kills existing Rps and App
    - calls configure_root_window with target_gamemode
    - calls start_game with target_gamemode
"""


import tkinter as tk
from tkinter import ttk
from random import choices as rand_choices
from PIL import ImageTk, Image
from pathlib import Path
from json import load as json_load
from os import rename


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


class Rps:
    """A class that serves as a game engine
    for variants of rock, paper, scissors."""

    def __init__(self, gamemode: dict):
        self.gamemode = gamemode["title"]
        self.alias = gamemode["alias"]
        self.moves = self._initialize_moves(gamemode["moves"])
        self.wins = {"player": 0, "draw": 0, "com": 0}
        self.com_confidence = self._initialize_com_confidence()

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
                move = move_key[key]
                # add Move object and verb to beats
                beats[move] = unformatted_beats[key]
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
        com_move = self._com_decide()
        victor = self._get_victor(player_move, com_move)
        outcome_message = self._get_outcome_message(
            player_move, com_move, victor
        )
        # update self.wins and self.com_confidence
        self._scorekeeping(player_move, victor)

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
        return rand.choices(self.moves, weights=confidence, k=1)[0]

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
        return "{} wins! {}{}{}.".format(
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

    def __init__(self, master, rps: Rps) -> None:
        super().__init__()
        self.master = master
        self.rps = rps
        self._make_widgets()

    def _make_widgets(self) -> None:
        """Generates all widgets"""
        self._configure_frame()
        self._make_display()
        self._make_move_picker()

    def _configure_frame(self) -> None:
        """Configures and packs self to root"""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0, minsize=60)
        self.pack(fill="both", expand=True)

    def _make_display(self) -> None:
        """Assembles frame containing widgets for displaying game info"""
        frm_display = self._make_frm_display()

    def _make_frm_display(self) -> ttk.Frame:
        """Initializes and configures display frame"""
        frm_display = ttk.Frame(self)
        frm_display.columnconfigure((0, 1, 2), weight=1, pad=5, minsize=260)
        frm_display.rowconfigure(0, weight=0, minsize=40, pad=5)
        frm_display.rowconfigure(1, weight=1, minsize=260)
        frm_display.grid(
            column=0,
            row=0,
            sticky="nsew",
        )
        return frm_display

    def _make_scoreboard(self, master: tk.Frame) -> None:
        """Initializes and configures scoreboard"""
        # TODO write _make_scoreboard
        # Note: gonna have to fiddle with tkvars, probs edit Rps.run_game to
        # return values for updating display elements
        # move picker button command will link to App function that
        # calls Rps.run_game and updates the display

    def _make_move_picker():
        # TODO write _make_move_picker
        pass


def _make_root(default_gamemode: str) -> None:
    """Instantiates and configures root window with menu bar."""
    global root
    root = tk.Tk()

    configure_root_window(default_gamemode)
    make_menu_bar(move_config["gamemodes"])


def make_menu_bar(gamemodes: str) -> None:
    """Creates menu bar slaved to root."""
    menu_bar = tk.Menu(root)
    mnu_options = tk.Menu(menu_bar, tearoff=0)
    mnu_gamemodes = make_mnu_gamemodes(mnu_options, gamemodes)

    mnu_options.add_cascade(label="Select Gamemode", menu=mnu_gamemodes)
    menu_bar.add_cascade(label="Options", menu=mnu_options)
    root.config(menu=menu_bar)


def make_mnu_gamemodes(master, gamemodes: list) -> tk.Menu:
    """
    Creates tkinter menu for switching gamemodes.
    The returned menu has one command per gamemode in gamemodes;
    each command calls change_gammeode and passes it
    the appropriate gamemode.
    """
    mnu_gamemodes = tk.Menu(master, tearoff=0)
    for gamemode in gamemodes.items():
        mnu_gamemodes.add_command(
            label=gamemode[1]["alias"],
            command=lambda: change_gamemode(gamemode),
        )
    return mnu_gamemodes


def configure_root_window(gamemode) -> None:
    """Configures geometry, title, and icon of root window."""
    root.geometry("640x480")
    active_gamemode_alias = gamemode["alias"]
    root.title(f"Play {active_gamemode_alias}")
    with Image.open(HERE / "icon.png") as open_img:
        open_img.resize((16, 16))
        icon = ImageTk.PhotoImage(open_img)
    root.wm_iconphoto(True, icon)


def _start_game(gamemode: str) -> None:
    """Instantiates Rps engine and App frame with given gamemode."""
    rps = Rps(gamemode)
    app = App(root, rps)


def change_gamemode(gamemode: str) -> None:
    """
    Changes gamemode by destroying currently active instances of
    Rps and App and reinstantiating them with the given gamemode.
    """


def _get_move_config() -> dict:
    """Reads move_config.json and returns dict with the info"""
    with open(HERE / "move_config.json") as cfg:
        return json.load(cfg)


def _get_gamemode(move_config: dict, gamemode: str) -> dict:
    """Separates gamemode info from greater move_config dict."""
    return move_config["gamemodes"][gamemode]


def main():
    global move_config
    move_config = _get_move_config()
    default_gamemode = _get_gamemode(
        move_config, move_config["default_gamemode"]
    )
    print(default_gamemode)
    _make_root(default_gamemode)
    _start_game(default_gamemode)
    root.mainloop()


if __name__ == "__main__":
    main()
